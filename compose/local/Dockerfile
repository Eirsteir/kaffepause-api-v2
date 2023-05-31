# USE https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker FOR PRODUCTION

# Use the official Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./requirements /requirements

# Install the required dependencies
RUN pip install --upgrade pip
RUN pip install -r /requirements/local.txt

# Copy the application code to the working directory
COPY ../.. .

# Set the command to run the application with live reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
