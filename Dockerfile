FROM python:alpine3.7

# Set any env values we need
ENV PYTHONPATH=/app

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# Install required deps
RUN apk update && apk add curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

# Disable poetry's virtualenvs before installing the app
RUN $HOME/.poetry/bin/poetry config settings.virtualenvs.create false
RUN $HOME/.poetry/bin/poetry install --no-dev

# Start the gunicorn service to run the app
RUN chmod +x ./run-app.sh
ENTRYPOINT ["sh", "./run-app.sh" ]