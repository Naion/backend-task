# Use Python base image
FROM python:3.11.3

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Clone the backend repository from GitHub
RUN git clone https://github.com/Naion/backend-task.git .

# Copy the Python requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Copy the Flask app code to the container
COPY ./main.py .

# Expose port 5000 for Flask
EXPOSE 5000

# Define environment variable (optional)
ENV FLASK_APP=main.py

# Run the Flask app
CMD ["flask", "run", "--host=172.17.0.2"]