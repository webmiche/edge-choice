# Optimizing Edge Choices for Optimal Inlining

This repo contains my work on optimizing the choice of edges in the [optimal inling](https://dl.acm.org/doi/pdf/10.1145/3503222.3507744) algorithm.

## How To

```bash
clang -S -emit-llvm example.c -o ex.ll
opt -passes=dot-callgraph
dot -Tpng -ocallgraph.png ex.ll.callgraph.dot

python3 main.py
```
