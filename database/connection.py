import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.engine = None
        self.SessionLocal = None
        
    def connect(self):
        """Establish database connection using mysql-connector-python"""
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                autocommit=True,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                logger.info("Successfully connected to MySQL database")
                return True
                
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            return False
    
    def create_sqlalchemy_engine(self):
        """Create SQLAlchemy engine for ORM operations"""
        try:
            self.engine = create_engine(
                config.DATABASE_URL,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("SQLAlchemy engine created successfully")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Error creating SQLAlchemy engine: {e}")
            return False
    
    def get_session(self):
        """Get database session"""
        if not self.SessionLocal:
            self.create_sqlalchemy_engine()
        return self.SessionLocal()
    
    def test_connection(self):
        """Test database connection and return table information"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            
            # Get table information
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            table_info = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                table_info[table_name] = [
                    {
                        'field': col[0],
                        'type': col[1],
                        'null': col[2],
                        'key': col[3],
                        'default': col[4],
                        'extra': col[5]
                    }
                    for col in columns
                ]
            
            cursor.close()
            return {
                'status': 'connected',
                'database': config.DB_NAME,
                'tables': table_info
            }
            
        except Error as e:
            logger.error(f"Database connection test failed: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            
            return {
                'status': 'success',
                'data': results,
                'row_count': len(results)
            }
            
        except Error as e:
            logger.error(f"Query execution failed: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

# Global database instance
db = DatabaseConnection() 