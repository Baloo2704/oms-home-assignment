FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies first (better for caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the server
CMD ["uvicorn", "mock_services.mock_api_server:app", "--host", "0.0.0.0", "--port", "8000"]