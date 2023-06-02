# Use the tiangolo/uvicorn-gunicorn-fastapi base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV MODULE_NAME "kaffepause.main"

# Copy the requirements file to the working directory
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

# Copy the application code to the working directory
COPY . /app
