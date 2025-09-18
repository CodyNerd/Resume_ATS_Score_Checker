# Deployment Guide

This guide covers different ways to deploy the Resume ATS Score Checker application.

## 🌐 Streamlit Cloud (Recommended)

### Prerequisites
- GitHub account
- NVIDIA API key from [build.nvidia.com](https://build.nvidia.com/)

### Steps

1. **Fork or clone this repository to your GitHub account**

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Click "New app" and connect your GitHub repository**

4. **Configure the deployment:**
   - Repository: `Lokeessshhh/Resume_ATS_Score_Checker`
   - Branch: `main`
   - Main file path: `app.py`

5. **Add environment variables in Streamlit Cloud:**
   - Go to "Advanced settings"
   - Add secrets in TOML format:
   ```toml
   NVIDIA_API_KEY = "your_nvidia_api_key_here"
   ```

6. **Deploy the app**

### Environment Variables for Streamlit Cloud

Add these to your Streamlit Cloud secrets:

```toml
# Required
NVIDIA_API_KEY = "your_nvidia_api_key_here"

# Optional
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
```

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and run

```bash
# Build the image
docker build -t resume-ats-checker .

# Run the container
docker run -p 8501:8501 -e NVIDIA_API_KEY=your_api_key_here resume-ats-checker
```

## ☁️ Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set NVIDIA_API_KEY=your_nvidia_api_key_here
   ```

3. **Create a Procfile**
   ```
   web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## 🔧 Local Development

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lokeessshhh/Resume_ATS_Score_Checker.git
   cd Resume_ATS_Score_Checker
   ```

2. **Run setup script**
   ```bash
   python setup.py
   ```

3. **Edit .env file**
   ```bash
   # Add your NVIDIA API key
   NVIDIA_API_KEY=your_nvidia_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔐 Security Considerations

### For Production Deployments

1. **Never commit API keys to version control**
2. **Use environment variables for all sensitive data**
3. **Enable HTTPS in production**
4. **Consider implementing rate limiting**
5. **Add user authentication if needed**
6. **Monitor API usage and costs**

### Environment Variables

Always set these environment variables in your deployment platform:

- `NVIDIA_API_KEY` (required)
- `NVIDIA_BASE_URL` (optional)
- `NVIDIA_MODEL` (optional)

## 🚨 Troubleshooting

### Common Issues

1. **"NVIDIA_API_KEY environment variable is required"**
   - Solution: Set the API key in your environment variables

2. **PDF processing errors**
   - Solution: Ensure `poppler-utils` is installed (included in `packages.txt`)

3. **Port already in use**
   - Solution: Use a different port with `--server.port=8502`

4. **Memory issues**
   - Solution: Consider upgrading your deployment plan or optimizing the application

### Getting Help

- Check the application logs
- Verify environment variables are set correctly
- Ensure your NVIDIA API key is valid and has sufficient credits
- Test with smaller files first

## 📊 Monitoring

### Recommended Monitoring

1. **API usage and costs**
2. **Application performance**
3. **Error rates**
4. **User engagement metrics**

### Logging

The application includes basic logging. For production, consider:
- Structured logging
- Log aggregation
- Error tracking (e.g., Sentry)
- Performance monitoring