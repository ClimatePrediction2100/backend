# Use the official Python base image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /backend

# Copy the Poetry configuration files to the working directory
COPY pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Create temporal database for test
RUN poetry run alembic upgrade head

# Copy the application code to the working directory
COPY . .

# Expose the port on which the FastAPI server will run
EXPOSE 8000

# Run the FastAPI server using Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]