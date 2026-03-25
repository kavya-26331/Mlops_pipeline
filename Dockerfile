
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install pandas numpy pyyaml
CMD ["python", "run.py", "--input", "/app/data.csv", "--config", "/app/config.yaml", "--output", "/app/metrics.json", "--log-file", "/app/run.log"]
