FROM python:3.12

# Install the libsndfile library
RUN apt-get update && apt-get install -y libsndfile1

WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the Speech2t.json file from the Cloud Build context
COPY Speech2t.json /app/Speech2t.json

# Expose the port that Cloud Run will use
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
