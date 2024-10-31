# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary libraries specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8050 for the dashboard
EXPOSE 8050

# Run the app
CMD ["python", "app.py"]
