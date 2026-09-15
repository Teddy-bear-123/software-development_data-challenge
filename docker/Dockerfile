FROM python:3.11-slim

RUN pip install numpy matplotlib

COPY . /app

WORKDIR /app

CMD ["python", "-m", "astrolab.pipeline"]