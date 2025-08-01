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
        self.db_type = "mysql"  # Default to MySQL
        
    def detect_db_type(self):
        """Detect database type from DATABASE_URL"""
        if config.DATABASE_URL.startswith("postgresql://"):
            self.db_type = "postgresql"
        elif config.DATABASE_URL.startswith("mysql://"):
            self.db_type = "mysql"
        logger.info(f"Detected database type: {self.db_type}")
        
    def connect(self):
        """Establish database connection"""
        try:
            self.detect_db_type()
            
            if self.db_type == "postgresql":
                # For PostgreSQL, we'll use SQLAlchemy engine
                return self.create_sqlalchemy_engine()
            else:
                # For MySQL, use mysql-connector-python
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
            logger.error(f"Error connecting to database: {e}")
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
            if self.db_type == "postgresql":
                return self._test_postgresql_connection()
            else:
                return self._test_mysql_connection()
                
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _test_mysql_connection(self):
        """Test MySQL connection"""
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
    
    def _test_postgresql_connection(self):
        """Test PostgreSQL connection"""
        if not self.engine:
            self.create_sqlalchemy_engine()
        
        with self.engine.connect() as connection:
            # Get table information
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            
            table_info = {}
            for table in tables:
                result = connection.execute(text(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = '{table}'
                    ORDER BY ordinal_position
                """))
                columns = result.fetchall()
                table_info[table] = [
                    {
                        'field': col[0],
                        'type': col[1],
                        'null': col[2],
                        'default': col[3]
                    }
                    for col in columns
                ]
            
            return {
                'status': 'connected',
                'database': config.DB_NAME,
                'tables': table_info
            }
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if self.db_type == "postgresql":
                return self._execute_postgresql_query(query, params)
            else:
                return self._execute_mysql_query(query, params)
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _execute_mysql_query(self, query, params=None):
        """Execute MySQL query"""
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
    
    def _execute_postgresql_query(self, query, params=None):
        """Execute PostgreSQL query"""
        if not self.engine:
            self.create_sqlalchemy_engine()
        
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            results = [dict(row) for row in result]
            
            return {
                'status': 'success',
                'data': results,
                'row_count': len(results)
            }
    
    def close(self):
        """Close database connection"""
        if self.db_type == "mysql" and self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")
        elif self.engine:
            self.engine.dispose()
            logger.info("Database engine disposed")

# Global database instance
db = DatabaseConnection() 