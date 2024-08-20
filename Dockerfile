# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ruff and black for linting and formatting
RUN pip install ruff black pandas rich

# Copy the scripts directory contents into the container at /app and make them executable
COPY scripts/*.sh .
RUN chmod a+x *.sh


# Copy the current directory contents into the container at /app
COPY . .

# Run the application
CMD ["python", "src/purchases_stats.py", "data/purchases_v1.json"]
