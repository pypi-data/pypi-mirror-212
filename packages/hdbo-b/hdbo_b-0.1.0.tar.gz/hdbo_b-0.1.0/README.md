<!--
 * @Author         : yiyuiii
 * @Date           : 2023-06-03 20:00:00
 * @LastEditors    : yiyuiii
 * @LastEditTime   : 2023-06-03 20:00:00
 * @Description    : None
 * @GitHub         : https://github.com/yiyuiii/HDBO-B
-->

<!-- markdownlint-disable MD033 MD036 MD041 -->

<div align="center">

# HDBO-B: High Dimensional Bayesian Optimization Benchmark

</div>

<p align="center">
<a href="https://raw.githubusercontent.com/Yiyuiii/HDBO-B/master/LICENSE"><img src="https://img.shields.io/github/license/Yiyuiii/HDBO-B.svg" alt="license"></a>
<a href="https://pypi.python.org/pypi/HDBO-B"><img src="https://img.shields.io/pypi/v/HDBO-B.svg" alt="pypi"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

**HDBO-B**, a generalized and unified benchmark for High Dimensional Bayesian Optimization, including testing functions, example algorithms and more examples. 

## :gear: Installation

We recommend using [CONDA](https://www.anaconda.com/) to isolate Python environments and their packages, this protects you from potential package version conflicts.

To install HDBO-B package, choose one below:
- `pip install hdbo-b`
- `git clone https://github.com/yiyuiii/HDBO-B && cd HDBO-B && pip install -e .`

In case we use HEBO 0.3.5 for experiments and there is 0.3.2 on PyPI currently, user should manually install:
- `git clone https://github.com/huawei-noah/HEBO && cd HEBO/HEBO && pip install -e .`

## :rocket: Quick Start

Uncomment lines in 'test.py', and run 'python test.py'.

User may also check codes in folder ‘./example’.

## :wrench: Details

Import hand-designed 30 test functions: 

```python
from HDBOBenchmark import TestFuncs as func_list
```

We have designed a stricter framework for functions and algorithms, 
This brings a lot of convenience to scaling, while there are a bit more difficulties in getting started.
Check them out in
- './HDBOBenchmark/base/FunctionBase.py'
- './HDBOBenchmark/AdditiveFunction.py'
- './example/wrapper/hebo_wrapper.py'

Optimizing algorithms under './examples' will save histories in folder './result', which are automatically read by './example/plot_result.py'.

## :speech_balloon: Common Issues

## TODO List

-[ ] Introducing more realistic test functions

-[ ] Introducing VAE-based algorithms and related datasets needed

## Cite Us

## :clipboard: Changelog

#### 2023.06.03 > v0.1.0 :fire:
- Initialization.
