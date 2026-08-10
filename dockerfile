FROM python:3.11-slim

# Working directory inside container
WORKDIR /app

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project into container
COPY . .

# FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]