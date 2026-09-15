# Astro Data Challenge

[![CI](https://github.com/jzoubian/software-development_data-challenge/actions/workflows/ci.yml/badge.svg)](https://github.com/jzoubian/software-development_data-challenge/actions/workflows/ci.yml)

Build a tiny astro-image pipeline, together, as a team, over one evening
and one morning.

**Mission**: turn 5 noisy exposures of the same star field into one clean,
nice-looking composite image, with a table of the brightness of every
star found along the way.

```
load frames → stack/denoise → detect sources → measure photometry → composite
```

## Status: foundation layer only, on purpose

This repo currently contains just enough to load the sample frames and
watch the pipeline stop at the first unimplemented step. That's
intentional: there's no environment spec, no CI, no docs, no tests, and
most of the actual pipeline is missing. Those gaps are the workshop
backlog — see the course repo's `5-data-challenge/README.md` for the full
task list, team workflow, and schedule.

## Quickstart


Create the Conda environment:

```sh
conda env create -f environment.yml
conda activate astrolab-env
python -m astrolab.pipeline
```

The `astroquery` package is optional and is only needed for the real-data
bonus feature in `astrolab/realdata.py`. To use that feature, install it
separately:

```sh
conda install -c conda-forge astroquery
```

You should see it load the 5 sample frames and then stop with:

```text
NotImplementedError: stack_frames: implement frame stacking
```

That's expected — you've just reached backlog item #1.

To poke at the raw frames first (e.g. plot them before diving into the
pipeline code), see [`notebooks/explore_frames.ipynb`](notebooks/explore_frames.ipynb).

## Code layout

- `astrolab/synth.py` — deterministic synthetic star-field generator
  (no download needed; same seed always produces the same data).
- `astrolab/io.py` — loading/saving frames (`.npy` files, numpy arrays).
- `astrolab/pipeline.py` — orchestrates the processing steps. Most of
  them (`stack_frames`, `detect_sources`, `measure_photometry`,
  `compose_image`) are stubs — this file is the shared entry point every
  team's work plugs into, so expect it to be a frequent source of merge
  conflicts during integration. That's by design.
- `data/frames/*.npy` — 5 synthetic, noisy exposures of the same field
  (128×128 pixels, 25 stars), generated with `astrolab.synth`, seed 42.
  Gitignored — generated, not committed. `astrolab.pipeline.run()`
  regenerates it automatically the first time it's missing, so a fresh
  clone/fork just works; run `python -m astrolab.synth` directly if you
  want the frames without running the pipeline (e.g. for the notebook).
  Output is byte-identical every time.
- `astrolab/realdata.py` — **bonus feature, stubbed**: fetch a real
  telescope image (e.g. the Orion Nebula) live from a public sky-survey
  archive via `astroquery`, instead of a synthetic frame, for a genuine
  "real astro image" payoff. Not required for the core pipeline — the
  rest of the pipeline stays deterministic and offline by design.
- `notebooks/explore_frames.ipynb` — loads and plots the sample frames,
  for a quick look at the input data before touching `pipeline.py`.

## Continuous integration

The GitHub Actions CI workflow runs on every push and pull request using
Python 3.11. It installs the project dependencies, generates the sample
frames, runs an I/O smoke check, and runs the pytest suite when test files
are available.

## License

GPLv3 — see `LICENSE`.
