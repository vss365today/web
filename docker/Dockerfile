FROM python:alpine3.7

# Set any env values we need
ENV PYTHONPATH=/app

# Copy the app files into the container
RUN mkdir -p /app
COPY ./docker /app/docker
COPY [ "get-requirements.py", "poetry.lock", "pyproject.toml", "run-flask.sh", "run-listener.sh", "/app/" ]
WORKDIR /app

# Install supervisor for service restarting
RUN apk update && apk add supervisor && rm -rf /var/cache/apk/*

# Install required deps
RUN pip3 install --no-cache-dir toml && \
    python3 ./get-requirements.py && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm ./requirements.txt && \
    chmod +x ./run-listener.sh && \
    chmod +x ./run-flask.sh && \
    mkdir -p /var/log/supervisor && \
    cp ./docker/supervisord.conf /etc/supervisord.conf
