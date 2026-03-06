"""
Database schema setup for Leadsec JobCard System
Run this file to create the database and tables
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def parse_db_url(url):
    """Parse database URL to extract connection parameters"""
    parsed = urlparse(url)
    return {
        'user': parsed.username or 'root',
        'password': parsed.password,
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 3306,
        'database': parsed.path.lstrip('/') if parsed.path else 'leadsec'
    }

def create_database():
    """Create database and tables"""
    
    try:
        # Parse DATABASE_URL from .env
        db_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost:3306/leadsec')
        # Remove driver prefix if present
        if '://' in db_url:
            db_url = db_url.split('://', 1)[1]
            db_url = 'mysql+pymysql://' + db_url
        
        db_config = parse_db_url(db_url)
        
        # Connect to MySQL server (without specifying database initially)
        connection_params = {
            'host': db_config['host'],
            'user': db_config['user'],
            'port': db_config['port']
        }
        
        if db_config['password']:
            connection_params['password'] = db_config['password']
        
        connection = mysql.connector.connect(**connection_params)
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS leadsec")
        print("Database 'leadsec' created or already exists")
        
        cursor.close()
        connection.close()
        
        # Connect to the leadsec database
        connection_params['database'] = db_config['database']
        connection = mysql.connector.connect(**connection_params)
        
        cursor = connection.cursor()
        
        # Create jobcards table
        create_jobcards_table = """
        CREATE TABLE IF NOT EXISTS jobcards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_title VARCHAR(255) NOT NULL,
            job_description TEXT,
            client_name VARCHAR(255) NOT NULL,
            client_email VARCHAR(255) NOT NULL,
            client_phone VARCHAR(20),
            service_location TEXT NOT NULL,
            technician_name VARCHAR(255) NOT NULL,
            service_date DATE NOT NULL,
            labor_hours FLOAT,
            materials_used TEXT,
            cost_estimate DECIMAL(10, 2),
            notes TEXT,
            client_signature LONGTEXT,
            signature_timestamp TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_by VARCHAR(255)
        );
        """
        
        cursor.execute(create_jobcards_table)
        print("Table 'jobcards' created or already exists")
        
        # Create indexes (ignore errors if they already exist)
        try:
            cursor.execute("CREATE INDEX idx_status ON jobcards(status);")
        except Error:
            pass  # Index already exists
        
        try:
            cursor.execute("CREATE INDEX idx_client_email ON jobcards(client_email);")
        except Error:
            pass  # Index already exists
        
        try:
            cursor.execute("CREATE INDEX idx_created_at ON jobcards(created_at);")
        except Error:
            pass  # Index already exists
        
        cursor.close()
        connection.commit()
        connection.close()
        
        print("Database setup completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()
