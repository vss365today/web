FROM python:alpine3.6

# Set any env values we need
EXPOSE 5001
ENV PYTHONPATH=/app

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# Install any tools we need
RUN apk update && apk install curl nano
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
RUN poetry install

# Start the gunicorn service to run the app
RUN chmod +x ./run-app.sh
ENTRYPOINT ["sh", "./run-app.sh" ]