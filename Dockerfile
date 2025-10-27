FROM python:3.12-slim

# Install poetry
RUN pip install poetry

WORKDIR /stonksbot

# Copy only dependencies files first
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

CMD ["poetry", "run", "python", "stonksbot/main.py"]