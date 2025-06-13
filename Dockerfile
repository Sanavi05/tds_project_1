# Use a slim official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "backend.api.qa_api:app", "--host", "0.0.0.0", "--port", "8000"]
