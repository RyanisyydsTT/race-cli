# race-cli

[![PyPI version](https://img.shields.io/pypi/v/race-cli.svg)](https://pypi.org/project/race-cli/)

Race CLI is a powerful tool to measure executive efficiency!

# Installation
## Install through PyPI:
```bash
pip install race-cli
```

## Build from Source Code:
```bash
git clone https://github.com/RyanisyydsTT/race-cli.git
cd race-cli
pip install -e .
```

# Usage
## Single-Run Mode
```bash
race 'echo hello' 'echo bye'
```

## Multi-Run Mode
```bash
race 'echo hello' 'echo bye' --runs 10
```
> This Mode will display execute time elapsed in min/max/avg format. Compared using average value of them.

# LICENSE
This repository uses MIT LICENSE.

# Contributing
Feel free to open a pull request, thank you!

