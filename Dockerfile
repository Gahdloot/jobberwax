FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE TRUE
ENV PYTHONUNBUFFERED TRUE

COPY requirements.txt /propelafrica/requirements.txt

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /propelafrica


ENTRYPOINT /propelafrica/entrypoint.sh