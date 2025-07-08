FROM python:3.10-alpine

# Install git
RUN apk add --no-cache git

# Clone the repo
RUN git clone https://github.com/Ranjan-Shettigar/Quanta.git /app

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
