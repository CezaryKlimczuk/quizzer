FROM ubuntu:noble

# Preventing Python from writing pyc files to disc
ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl
RUN apt-get update && apt-get install -y curl

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# # Copy the uv lock file
# COPY uv.lock pyproject.toml ./

# # Install the dependencies
# RUN uv sync

# COPY . .