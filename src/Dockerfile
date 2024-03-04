# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
COPY . /app/

# Set work directory
WORKDIR /app/src

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# Add and set permissions for the scripts
RUN chmod +x entrypoint.sh migrate.sh collectstatic.sh

# Expose the port the app runs in
EXPOSE 8000:8002

# Define the command to start the container
CMD ["./entrypoint.sh"]