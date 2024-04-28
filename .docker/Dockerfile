FROM python:3.10-slim-bullseye

# Label for image metadata
LABEL maintainer="slavasg"

# Install system dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc curl procps net-tools tini \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install gunicorn

# Install Poetry
ENV POETRY_HOME=/tmp/poetry
RUN curl -sSL https://install.python-poetry.org/ | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Poetry configuration and package installation
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Expose port 8000 for the application
EXPOSE 8000

# Run the application using Tini as the init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# By default, run gunicorn on port 8000, adjust the command as necessary for your app
CMD ["gunicorn", "your_application_module:app", "--bind", "0.0.0.0:8000"]
