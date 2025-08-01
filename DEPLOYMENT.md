# Deployment Guide for Render.com

This guide will help you deploy your Stock AI Backend to Render.com.

## Prerequisites

1. A Render.com account
2. Your code pushed to a Git repository (GitHub, GitLab, etc.)
3. A MySQL database (you can use Render's PostgreSQL or external MySQL)

## Step 1: Prepare Your Repository

Your repository should now include:
- `Dockerfile` - For containerized deployment
- `render.yaml` - Render service configuration
- `start.sh` - Production startup script
- `requirements.txt` - Python dependencies
- `.dockerignore` - Docker build optimization

## Step 2: Set Up Database

### Option A: Use Render PostgreSQL (Recommended)
1. Create a new PostgreSQL service in Render
2. Note the connection details (host, port, database, username, password)

### Option B: Use External MySQL
1. Set up a MySQL database (AWS RDS, PlanetScale, etc.)
2. Note the connection details

## Step 3: Deploy to Render

### Method 1: Using render.yaml (Recommended)
1. Connect your GitHub repository to Render
2. Render will automatically detect the `render.yaml` file
3. Configure the following environment variables in Render dashboard:

**Required Environment Variables:**
```
DB_HOST=your_database_host
DB_PORT=5432 (for PostgreSQL) or 3306 (for MySQL)
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
OPENAI_API_KEY=your_openai_api_key
```

**Optional Environment Variables:**
```
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false
```

### Method 2: Manual Setup
1. Create a new Web Service in Render
2. Connect your GitHub repository
3. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `chmod +x start.sh && ./start.sh`
   - **Environment:** Python 3.11

## Step 4: Configure Environment Variables

In your Render service dashboard, add these environment variables:

### Database Configuration
- `DB_HOST`: Your database host
- `DB_PORT`: Database port (5432 for PostgreSQL, 3306 for MySQL)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name

### OpenAI Configuration
- `OPENAI_API_KEY`: Your OpenAI API key

### Application Configuration
- `APP_HOST`: 0.0.0.0 (default)
- `APP_PORT`: 8000 (default)
- `DEBUG`: false (for production)

## Step 5: Deploy

1. Click "Create Web Service" in Render
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues
4. Once deployed, your API will be available at the provided URL

## Step 6: Verify Deployment

1. Check the health endpoint: `https://your-app-name.onrender.com/health`
2. Test the API documentation: `https://your-app-name.onrender.com/docs`
3. Verify database connectivity through the `/database/status` endpoint

## Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Database Connection Issues**
   - Verify database credentials
   - Check if database is accessible from Render's network
   - For external databases, ensure they allow connections from Render's IP ranges

3. **Application Startup Issues**
   - Check the logs in Render dashboard
   - Verify environment variables are set correctly
   - Ensure the startup script has execute permissions

4. **Memory/Performance Issues**
   - Consider upgrading to a higher plan
   - Optimize database queries
   - Implement caching if needed

## Monitoring

- Use Render's built-in logging to monitor your application
- Set up alerts for downtime
- Monitor database performance
- Track API response times

## Security Notes

1. Never commit API keys or database credentials to your repository
2. Use environment variables for all sensitive data
3. Regularly rotate your OpenAI API key
4. Consider implementing rate limiting for production use

## Cost Optimization

- Start with the free tier for testing
- Monitor usage and upgrade only when needed
- Consider using Render's PostgreSQL for better integration
- Implement proper caching to reduce API calls

## Support

If you encounter issues:
1. Check Render's documentation
2. Review the application logs
3. Test locally with the same environment variables
4. Contact Render support if needed 