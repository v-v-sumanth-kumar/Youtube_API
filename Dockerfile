# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set the PYTHONPATH so Python can find the "app" module
ENV PYTHONPATH=/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to start the FastAPI app
#CMD ["uvicorn", "app.api.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


