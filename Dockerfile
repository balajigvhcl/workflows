# Use official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY models.py .
COPY shift_logic ./shift_logic
COPY flask_backend ./flask_backend
COPY frontend ./frontend

# Expose Flask port
EXPOSE 5000

# Environment variable so Flask can find your app
ENV PYTHONPATH="/app"

# Run Flask app (development mode)
CMD ["python", "flask_backend/app.py"]

# For production, you can replace the CMD with Gunicorn:
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_backend.app:app"]