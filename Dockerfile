FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE TRUE
ENV PYTHONUNBUFFERED TRUE

COPY requirements.txt /app/requirements.txt

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/


CMD ["python", "manage.py", "runserver", "0.0.0.0:8008"]