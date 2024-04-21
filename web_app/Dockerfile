# Use an official Python runtime as a parent image
FROM python:3.11 

# Set the working directory in the container to /web_app
WORKDIR /web_app

# Add the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /web_app
COPY . /web_app

# Make port 8080 available to the world outside this container
EXPOSE 8080

