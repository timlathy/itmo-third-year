## Prerequisites

* Python 3.7
* Nightly Rust toolchain

## Setup

```sh
pip install virtualenv
virtualenv applied-maths-lab1
source applied-maths-lab1/bin/activate
pip install maturin ipykernel
ipython kernel install --user --name=applied-maths-lab1
```

## Development

Building the native extension:

```sh
cd entropy
maturin develop
```

Running the notebook:

```sh
jupyter notebook
```

