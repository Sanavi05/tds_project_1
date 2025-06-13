# # Use a slim official Python image
# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Copy only requirements first to leverage caching
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the code
# COPY . .

# # Expose port (FastAPI default)
# EXPOSE 8000

# # Command to run the app
# CMD ["uvicorn", "backend.api.qa_api:app", "--host", "0.0.0.0", "--port", "8000"]


# Use lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Create working directory
WORKDIR /app

# Copy only requirements to leverage cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "backend.api.qa_api:app", "--host", "0.0.0.0", "--port", "8000"]
