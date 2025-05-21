FROM python:3.10-slim

# Update packages, install git and remove cache
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt streamlit

# Copy application code
COPY . .

# Create output directory with proper permissions
RUN mkdir -p /app/output && chmod 777 /app/output

# Expose the Streamlit port
EXPOSE 8501

# Environment variables
ENV GEMINI_API_KEY=""
ENV GITHUB_TOKEN=""

# Set default command to start Streamlit
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
