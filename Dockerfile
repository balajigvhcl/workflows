#FROM python:3.11-slim
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#CMD ["python", "app.py"]
# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements (create requirements.txt with Flask + SQLAlchemy)
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
#COPY ../models.py .
#COPY ../shift_logic ./shift_logic
#COPY ../flask_backend ./flask_backend
##COPY ../frontend ./frontend

#COPY ./../models.py .
#COPY ./../shift_logic ./shift_logic
#COPY ./../flask_backend ./flask_backend
#COPY ./../frontend ./frontend
COPY models.py .
COPY shift_logic ./shift_logic
COPY flask_backend ./flask_backend
COPY frontend ./frontend


# Expose Flask port
EXPOSE 5000

# Run Flask app
ENV PYTHONPATH="/app"
CMD ["python", "-m", "flask_backend.app"]
