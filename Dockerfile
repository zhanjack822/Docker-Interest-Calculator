FROM python:3.13.2-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependencies file first (leverages Docker cache)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variables
ENV FLASK_APP=app.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose the port Flask will run on
EXPOSE 5000

# Default command to start the Flask app
CMD ["flask", "run"]
