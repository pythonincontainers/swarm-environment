FROM python:3.7.3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "swarm-env.py"]
HEALTHCHECK --interval=10s --timeout=3s --retries=2 \
  CMD curl -f -s http://127.0.0.1:5000/healthcheck || exit 1
