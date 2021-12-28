FROM python:3.8-slim-buster

COPY . .

WORKDIR /

# Install pipenv and compilation dependencies
RUN pip install pipenv && apt-get update && apt-get install -y --no-install-recommends gcc
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000

CMD [ "uvicorn", "services.api.main:app", "--host", "0.0.0.0"]
