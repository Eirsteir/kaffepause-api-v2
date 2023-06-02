# Use the tiangolo/uvicorn-gunicorn-fastapi base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Copy the requirements file to the working directory
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Copy the application code to the working directory
COPY ./kaffepause /app

ENTRYPOINT ["/entrypoint"]
