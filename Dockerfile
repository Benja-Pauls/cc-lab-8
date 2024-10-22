# Use the full official Python image to avoid missing dependencies
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app directly
CMD ["python", "app.py"]

