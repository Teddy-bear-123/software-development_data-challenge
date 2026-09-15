# Test Suite

This folder contains the automated tests for the `astrolab` package.
The tests are written with [pytest](https://docs.pytest.org/) and use
[numpy](https://numpy.org/) for array assertions.

## Layout

```text
tests/
├── __init__.py # makes this folder a Python package
├── README.md # this file
└── test_synth.py # tests for astrolab.synth (issue #3)
```

## How to Run

From the **project root** (the folder that contains `astrolab/` and `tests/`):

```bash
python -m pytest tests/ -v
```

Run a single file:

```bash
python -m pytest tests/test_synth.py -v
```

Run a single test by name:

```bash
python -m pytest tests/test_synth.py::test_same_seed_produces_identical_frames -v
```

## Test Count and Runtime

**37 tests**

~6 seconds on a typical laptop (dominated by the 256×256
statistical tests in Slice C)
