FROM python:3.10-slim

# Install system dependencies for building packages and nginx
RUN apt-get update && apt-get install -y build-essential gcc nginx && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . /app/

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for nginx
EXPOSE 80

# Make start_app.sh executable
RUN chmod +x start_app.sh

# Start the app using start_app.sh
CMD ["./start_app.sh"]
