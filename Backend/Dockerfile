# Backend/Dockerfile
#
# Builds the actual FastAPI backend (previously the repo's only Dockerfile
# built an unrelated Node.js prototype instead -- this replaces that).

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (separate layer so `docker build` doesn't
# reinstall everything just because application code changed)
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Now copy the actual application code
COPY . .

EXPOSE 8000

# Run without --reload in production -- --reload is a dev-only convenience
# that watches files for changes, which isn't needed (and adds overhead)
# in a container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
