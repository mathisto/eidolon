# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8080 to the outside world
EXPOSE 8080

# Run the application with uvicorn
CMD ["uvicorn", "eidolon.app:app", "--host", "0.0.0.0", "--port", "8080"]
