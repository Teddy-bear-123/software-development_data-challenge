# Running the Astro Data Challenge with Docker

This directory contains the Dockerfile for the Astro Data Challenge project.
The image uses Python 3.11, installs NumPy and Matplotlib, copies the project
into `/app`, and runs the pipeline when the container starts.

## Prerequisites

- Docker Desktop or another Docker installation
- A clone of this repository

## Build the image

Run this command from the project root, the directory that contains both
`astrolab/` and `docker/`:

```sh
docker build -f docker/Dockerfile -t astro-data-challenge .
```

The final `.` is important: the Dockerfile copies the project from the build
context into the image.

## Run the pipeline

```sh
docker run --rm astro-data-challenge
```

The container runs:

```sh
python -m astrolab.pipeline
```

Generated files remain inside the container and are removed when the container
exits. To keep generated output on the host, mount a local directory at
`/app/data`:

```sh
docker run --rm \
	-v "${PWD}/data:/app/data" \
	astro-data-challenge
```

On Windows PowerShell, use:

```powershell
docker run --rm -v "${PWD}/data:/app/data" astro-data-challenge
```

## Current expected behavior

The project is currently the foundation layer of the data challenge. The
pipeline generates or loads the five sample frames and then stops at the first
unimplemented processing step with:

```text
NotImplementedError: stack_frames: implement frame stacking
```

That error is expected until the pipeline implementation is completed.

## Rebuild after code changes

Rebuild the image whenever project files or dependencies change:

```sh
docker build --no-cache -f docker/Dockerfile -t astro-data-challenge .
```

Use `--no-cache` only when you need to force every Dockerfile layer to run
again. A normal build is faster:

```sh
docker build -f docker/Dockerfile -t astro-data-challenge .
```

## Troubleshooting

If Docker cannot find `astrolab.pipeline`, check that the image was built from
the project root rather than from inside the `docker/` directory. The correct
command is:

```sh
docker build -f docker/Dockerfile -t astro-data-challenge .
```
