# Use the latest Python 3.8 image from the official Python Docker Hub repository
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Clone the GitHub repository
RUN git clone -b main https://github.com/caribeedu/Google-Image-Scraper .

# Create output folder
RUN mkdir ./output

# Install the requirements
RUN pip install -r requirements.txt

# Add Debian source
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list

# Install Firefox for Selenium usage
RUN apt-get update && apt-get install -y --no-install-recommends firefox