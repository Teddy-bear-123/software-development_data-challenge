# Astro Data Challenge Docker Setup

The image uses Python 3.11 and includes:

- **NumPy** for numerical and array operations
- **Matplotlib** for plotting and visualization

Build the image from the project root:

```sh
docker build -f docker/Dockerfile -t astro-data-challenge .
```


Run the pipeline:

```sh
docker run --rm astro-data-challenge
```

