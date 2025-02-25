# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Expose port 8080 (used by Azure Container Apps)
EXPOSE 8080

# Start the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]