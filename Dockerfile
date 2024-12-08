FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install cron and tzdata for time zone configuration
RUN apt-get update && apt-get install -y cron tzdata

# Set the time zone to Warsaw
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy the cron job file
COPY arxiv_cron /etc/cron.d/arxiv_cron

# Set permissions for the cron job
RUN chmod 0644 /etc/cron.d/arxiv_cron

# Apply the cron job
RUN crontab /etc/cron.d/arxiv_cron

# Run cron in the foreground
CMD ["cron", "-f"]
