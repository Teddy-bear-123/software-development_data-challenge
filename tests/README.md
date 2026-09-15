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

New test files for other modules (`astrolab.io`, `astrolab.pipeline`, ...)
should follow the same naming convention: `test_<module>.py`.

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

### Useful flags

| Flag | Meaning |
|---|---|
| `-v` | Verbose — one line per test |
| `-q` | Quiet — summary only |
| `-x` | Stop at the first failure |
| `--lf` | Run only the tests that failed last time |
| `-k <pattern>` | Run only tests whose name matches `<pattern>` |

Example: run only the determinism tests.

```bash
python -m pytest tests/test_synth.py -k determinism -v
```

## What `test_synth.py` Covers

The module under test is `astrolab/synth.py`, which generates
deterministic synthetic star-field frames. The tests are organized
into three slices, matching the three responsibilities laid out in
issue #3.

### Slice A — Determinism

**Question:** Does the module deliver on its docstring promise that
"the same seed always produces the same frame"?

- Same seed → byte-identical arrays (`np.testing.assert_array_equal`)
- Different seeds → different output
- Default seed (no argument) is also deterministic
- Reproducibility holds across many seeds (0, 1, 17, 99, 12345, 99999)
- `generate_frame_set(seed=s)` is deterministic frame-by-frame

### Slice B — Shape and parameter edge cases

**Question:** Does the function respect its inputs at the boundaries?

- Parametrized shapes: (1, 1), (2, 3), (3, 2), (16, 16),
  (32, 64), (64, 32), (128, 128)
- Default shape falls back to the module constant `FRAME_SHAPE`
- `n_stars=0` with `noise_sigma=0` produces a frame where every pixel
  equals background exactly (no noise, no stars)
- A single star runs without error and creates a bright peak above the
  background
- Non-square shapes are preserved (tall and wide tested separately)
- A custom background is honoured
- More stars → greater total brightness (with zero noise)
- The return type is a numpy array of floating dtype

### Slice C — Statistical sanity checks on `generate_frame_set`

**Question:** Does the frame-set generator produce something that
behaves like real astronomy data?

- Returns a Python list
- The number of frames matches the argument (0, 1, 2, 5, 10)
- The default is 5 frames
- `n_frames=0` returns an empty list
- Every frame has the requested shape and a floating dtype
- With `n_stars=0`, the mean of each frame is close to background
  (noise has zero mean)
- With a large frame, the empirical stddev of pixels matches
  `noise_sigma`
- Frames within a set are not identical — each uses an independent
  noise draw
- Averaging frames reduces the standard deviation below a single
  frame's (the whole point of stacking)
- With `noise_sigma=0`, all frames are identical because the only
  signal (the stars) is shared across frames

### Constants sanity

A few small guards against accidental renames or value changes:

- `FRAME_SHAPE` is a 2-tuple of positive integers
- `DEFAULT_N_STARS`, `DEFAULT_NOISE_SIGMA`, `DEFAULT_BACKGROUND` are
  in expected ranges
- `SAMPLE_SEED` is an integer; `SAMPLE_N_FRAMES` is positive

## Test Count and Runtime

**37 tests**

~6 seconds on a typical laptop (dominated by the 256×256
statistical tests in Slice C)

## Design Notes

### Why `np.testing.assert_array_equal`?

`np.array_equal` returns a boolean and loses all detail on failure.
`np.testing.assert_array_equal` raises an `AssertionError` that shows
exactly which elements differ — invaluable when diagnosing a failure.

### Why statistical tolerances instead of exact equality?

Slice C tests the statistics of a random process. Two different seeds
produce different noise, so the assertion must allow for sampling
variance. The tolerances (< 0.5 for the mean, < 0.5 for the stddev on
a 256×256 frame) are chosen to be loose enough to avoid false positives
but tight enough to catch real regressions.

### Why parametrized tests?

`@pytest.mark.parametrize` creates separate test cases that pytest
reports individually. When a specific shape or count fails, the failure
message names the exact case — much better than a single loop that
fails silently.

### Why no test of `regenerate_sample_data`?

That function writes files to `data/frames/`. A full test would use
pytest's `tmp_path` fixture to redirect writes to a temporary
directory. This is a good follow-up if the sample data path becomes
configurable in the future.

## Contributing

When adding tests:

- Name the file `test_<module>.py`.
- Name functions `test_<behavior>` — start with `test_`, describe
  what is being tested in the reader's language.
- One assertion per behavior. If a test needs "and", split it.
- Use `pytest.mark.parametrize` for multiple inputs of the same
  behavior.
- Prefer exact assertions where possible; use statistical tolerances
  only for genuinely random quantities.
- Use `np.testing.assert_array_equal` for numpy arrays, not `==`
  or `np.array_equal`.

## References

- pytest documentation: [https://docs.pytest.org/](https://docs.pytest.org/)
- numpy testing utilities: [https://numpy.org/doc/stable/reference/routines.testing.html](https://numpy.org/doc/stable/reference/routines.testing.html)
- Issue #3 (this suite): Add a pytest suite for `astrolab.synth`
- Course module: Module 3 — Documentation & Testing
