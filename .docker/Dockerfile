# Use a specific version of python:3.10-slim-bullseye
FROM python:3.10-slim-bullseye

# Label for image metadata
LABEL maintainer="slavasg"

# Install Rust compiler and other system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc curl procps net-tools tini \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . $HOME/.cargo/env \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable to avoid the cargo/rustc not found errors
ENV PATH=/root/.cargo/bin:$PATH

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

# Disable the creation of virtual environments by Poetry
# as dependencies are installed system-wide
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Expose port 8000 for the application
EXPOSE 8000

# Use Tini as the init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start gunicorn with the application module, replace 'your_application_module' accordingly
CMD ["gunicorn", "your_application_module:app", "--bind", "0.0.0.0:8000"]
