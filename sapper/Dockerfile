ARG BASE_IMAGE=python:3.9-slim-buster
FROM $BASE_IMAGE

# Set the working directory to /app
WORKDIR /app

# system update & package install
RUN apt-get update && \
    apt-get install -y python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copied requirements.txt file to the current image directory
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
# requirements
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy all files from the current directory (where the Dockerfile is located) to /app in the image
COPY . .

RUN python manage.py makemigrations && python manage.py migrate

# Creating an administrator
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell

# Execute
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]