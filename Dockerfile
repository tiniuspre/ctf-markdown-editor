FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the application runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_RUN_HOST=0.0.0.0


RUN python -m playwright install
RUN python -m playwright install-deps


# Define the command to run the application
CMD ["flask", "run"]