# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Pinecone
RUN pip install --extra-index-url https://pypi.pinecone.io/ --trusted-host pypi.pinecone.io pinecone-client

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World
ENV PORT 8080

# Run Uvicorn with FastAPI application
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8080"]