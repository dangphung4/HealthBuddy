FROM python:3.12


# Install the libsndfile library
RUN apt-get update && apt-get install -y libsndfile1

WORKDIR /app


# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip

RUN pip install openai

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure openai is installed
RUN pip install openai

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
