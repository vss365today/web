FROM python:alpine3.7

# Set any env values we need
ENV PYTHONPATH=/app

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# Install required deps
RUN pip3 install --no-cache-dir toml && \
    python3 ./get_requirements.py && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm ./requirements.txt && \
    chmod +x ./run-app.sh

# Start the gunicorn service to run the app
ENTRYPOINT ["sh", "./run-app.sh" ]