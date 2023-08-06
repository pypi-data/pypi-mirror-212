import contextlib
import typing
from typing import Callable, Tuple

import jax
from jax import lax, numpy as jnp

_GLOBAL_FLAGS = {}


def map_fn(fn):
    def _fn(x, *args, **kwargs):
        return jax.tree_util.tree_map(lambda k: fn(k, *args, **kwargs), x)

    return _fn


def remat(fn: Callable) -> Callable:
    @jax.custom_gradient
    def _fn(*args):
        def _grad(*d):
            return jax.vjp(fn, *args)[1](*d)

        return fn(*args), _grad

    return _fn


def identity(*args, **kwargs):
    if args:
        return args[0]
    if kwargs:
        return next(iter(kwargs.values()))
    return None


def if_flag(flag: str, baseline=identity):
    def _outer(fn):
        def _fn(*args, **kwargs):
            if not _GLOBAL_FLAGS.get(flag, False):
                return baseline(*args, **kwargs)
            return fn(*args, **kwargs)

        return _fn

    return _outer


@contextlib.contextmanager
def set_flag(flag: str):
    original = _GLOBAL_FLAGS.get(flag, False)
    try:
        _GLOBAL_FLAGS[flag] = True
        yield
    finally:
        _GLOBAL_FLAGS[flag] = original


def select(predicate, xs):
    def _fn(*args):
        return lax.select_n(predicate, *args)

    return jax.tree_util.tree_map(_fn, *xs)


@map_fn
def cast(inp, dtype):
    return inp.astype(dtype)


def cast_tree(tree0, tree1):
    return jax.tree_util.tree_map(lambda x, y: x.astype(y.dtype), tree0, tree1)


def shift(x, offset: int, axis: str):
    return lax.ppermute(x, axis, [(j, (j + offset) % jax.device_count()) for j in range(jax.device_count())])


def tree_dtype(tree):
    x, _structure = jax.tree_util.tree_flatten(tree)
    return x[0].dtype


@map_fn
def index(x, index: typing.Optional[int] = None):
    if index is None:
        return map_fn(lambda k: k[x])  # x is index, we simply curried
    return x[index]


@map_fn
def nan_default(x, default):
    return jnp.where(jnp.isfinite(x), x, default)  # True, False | x in (NaN, Inf, -Inf)


def dot(x, w):
    return lax.dot_general(x, w, (((x.ndim - 1,), (0,)), ((), ())), precision="fastest")


def softmax(q: jax.Array, k: jax.Array, ctx_dims: str, scale: float) -> jax.Array:
    @jax.custom_gradient
    def _fn(q: jax.Array, k: jax.Array) -> jax.Array:
        lgt = jnp.einsum(f"bshf,{ctx_dims}->bhsz", q, k, precision="fastest")
        lgt = lgt.astype(jnp.float32)
        lgt *= scale
        lgt = jnp.exp(lgt - lgt.max(-1, keepdims=True))
        lgt /= lgt.sum(-1, keepdims=True)
        lgt = lgt.astype(q.dtype)

        def _grad(dy):
            inner_lgt = lgt.astype(jnp.float32)
            prod = inner_lgt * dy.astype(jnp.float32)
            dlgt = prod - prod.sum(-1, keepdims=True) * inner_lgt
            dlgt *= scale
            dlgt = dlgt.astype(q.dtype)
            return (jnp.einsum(f"bhsz,{ctx_dims}->bshf", dlgt, k, precision="fastest"),
                    jnp.einsum(f"bhsz,bshf->{ctx_dims}", dlgt, q, precision="fastest"))

        return lgt, _grad

    return _fn(q, k)


def to_host(k, index_fn: Callable[[jax.Array], jax.Array] = index(0)):
    return jax.device_get(map_fn(index_fn)(k))


@map_fn
def promote(inp: jax.Array, dtype=jnp.float64) -> jax.Array:
    return jnp.asarray(inp, jnp.promote_types(dtype, jnp.result_type(inp)))


def multi_dot(*inputs: Tuple[jax.Array, jax.Array]):
    return [dot(x, w) for x, w in inputs]


def clip_norm(val: jax.Array, min_norm: float) -> jax.Array:
    return jnp.maximum(jnp.sqrt(lax.square(val).sum()), min_norm)


def ema(old, new, beta, step):
    out = (1 - beta) * old + beta * new
    return out / (1 - beta ** step), out


def attention(hidden_states, context, qk, kk, vk, pk, pb, scale: float, heads: int, chunk: int = 1024,
              dot_fn: Callable = multi_dot):
    ctx_dims = f'{"b" * (context.ndim > 2)}zhf'

    @remat
    def _fn(h, c, qk, kk, vk, pk, pb):

        q, k, v = [x.reshape(*x.shape[:-1], heads, -1).astype(jnp.bfloat16)  #
                   for x in multi_dot((h, qk), (c, vk), (c, kk))]

        def _attn(carry: jax.Array, idx: jax.Array) -> Tuple[jax.Array, None]:
            lq = lax.dynamic_slice_in_dim(q, idx * chunk, chunk, q.ndim - 3)
            tmp = jnp.einsum(f"bhsz,{ctx_dims}->bshf", softmax(lq, k, ctx_dims, scale), v, precision="fastest")
            carry = lax.dynamic_update_slice_in_dim(carry, tmp, idx * chunk, 1)
            return carry, None

        if q.shape[-3] // chunk:
            carry = jnp.zeros((*q.shape[:-1], v.shape[-1]), dtype=jnp.bfloat16)
            out, _ = lax.scan(_attn, carry, jnp.arange(q.shape[-3] // chunk))
        else:
            out = None

        if q.shape[-3] % chunk:
            start = q.shape[-3] // chunk * chunk
            lq = lax.slice_in_dim(q, start, limit_index=None, axis=q.ndim - 3)
            out2 = jnp.einsum(f"bhsz,{ctx_dims}->bshf", softmax(lq, k, ctx_dims, scale), v, precision="fastest")

            if out is None:
                out = out2
            else:
                out = jnp.concatenate([out, out2], -3)
        else:
            assert out is not None

        return dot_fn((out.reshape(*out.shape[:-2], -1), pk))[0].astype(h.dtype) + pb

    return _fn(hidden_states, context, qk, kk, vk, pk, pb)
