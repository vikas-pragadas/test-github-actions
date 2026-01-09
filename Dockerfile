FROM python:3.12-slim

WORKDIR /code

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run with correct app path (adjust 'app.main:app' to match your main FastAPI file)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
