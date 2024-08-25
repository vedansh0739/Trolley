# Use an official Python runtime as a base image
FROM python:3.9.18-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y \
    curl \
    git
# Set the working directory inside the container
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
