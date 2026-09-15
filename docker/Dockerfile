FROM python:3.11-slim

# Avoid storing pip's package cache in the image; used to be numpy
RUN pip install --no-cache-dir numpy matplotlib

COPY . /app

WORKDIR /app

CMD ["python", "-m", "astrolab.pipeline"]