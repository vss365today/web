FROM python:alpine3.6

# Set any env values we need
EXPOSE 5000

# Copy the app files into the container
COPY . ./

# Install any tools we need
RUN apk update && apk install curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
RUN poetry install

# Start the gunicorn service to run the app
COPY run-gunicorn.sh /run-gunicorn.sh
RUN chmod +x /run-gunicorn.sh
ENTRYPOINT ["sh", "/run-app.sh" ]
