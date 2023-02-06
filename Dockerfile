FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy and install dependencies seperatelly to cache step
COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy development directory contents to container working dir
COPY . /app

CMD ["python", "run.py"]