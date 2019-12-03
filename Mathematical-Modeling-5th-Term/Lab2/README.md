# Lab2

## Running Simulations

It is highly recommended that you use [PyPy](https://pypy.org/download.html)
as it provides up to a 5x speedup over CPython.
(Believe me, this is very noticeable: it takes _over a minute_ to
simulate 1 million customers if you don't use it).

```
pypy3 -m ensurepip
pypy3 -m pip install --user ciw simplejson
pypy3 simulate.py
```
