FROM python:3.9

# Set the working directory in the container
WORKDIR /app
RUN mkdir /app/data

# Copy the script and requirements file to the container
COPY scraper.py requirements.txt .env /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install cron package
RUN apt-get update && apt-get -y install cron

# Copy the cron job file to the container
COPY cronjob /etc/cron.d/scraper-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scraper-cron

# Apply the cron job
RUN crontab /etc/cron.d/scraper-cron

# Create log file and give permission
RUN touch /var/log/cron.log
RUN chmod 777 /var/log/cron.log

# Run the cron process in the foreground
CMD ["cron", "-f"]
