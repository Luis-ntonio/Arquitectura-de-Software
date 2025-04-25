FROM python:3.11-slim

# Update the base image to ensure all packages are up-to-date
RUN apt-get update && apt-get upgrade -y && apt-get clean
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt