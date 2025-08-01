#!/usr/bin/env python3
"""
Stock AI Analysis System - Main Entry Point
"""

import uvicorn
import logging
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the Stock AI Analysis System"""
    try:
        logger.info("Starting Stock AI Analysis System...")
        logger.info(f"Server will run on {config.APP_HOST}:{config.APP_PORT}")
        logger.info(f"Debug mode: {config.DEBUG}")
        
        # Start the server
        uvicorn.run(
            "api.main:app",
            host=config.APP_HOST,
            port=config.APP_PORT,
            reload=config.DEBUG,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    main() 