# JaxHelper

/home/lucas/PycharmProjects/jaxtools/setup.py

## Getting Started

### Installation

```BASH
python3 -m pip install jaxhelper
```

### Explanation

This repository contains basic helper functions I use every day.\
Here are some highlights:

* **remat**: function decorator to rematerialize ("activation checkpointing") hidden states during backward pass
* **softmax**:
    * exp in fp32 and matmul in bf16 (-> improved convergence and speed)
    * fewer stored intermediates yet faster gradient
* **attention**:
    * recomputation of hidden states
    * memory of O(K * N) rather than O(N^2) thanks
      to [Self-attention Does Not Need O(n2) Memory](https://arxiv.org/abs/2112.05682). (No slowdown)
