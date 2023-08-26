FROM python:3.11-slim

# Set any env values we need
ENV PYTHONPATH=/app

# Copy the app files into the container
RUN mkdir -p /app
COPY [ "get-requirements.py", "poetry.lock", "pyproject.toml", "run-app.sh", "/app/" ]
WORKDIR /app

# Install required deps and run the app
RUN python3 -m pip install pip --upgrade && \
    python3 ./get-requirements.py && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm ./requirements.txt && \
    chmod u+x ./run-app.sh

# Start the app
ENTRYPOINT [ "sh", "./run-app.sh" ]
