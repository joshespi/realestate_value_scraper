FROM python:3.9

# Set the working directory in the container
WORKDIR /app
RUN mkdir /app/data
# Copy the script and requirements file to the container
COPY scraper.py requirements.txt .env /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "scraper.py"]
