# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /src

# Copy the requirements file into the container at /app
COPY ./src/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src/ .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]
