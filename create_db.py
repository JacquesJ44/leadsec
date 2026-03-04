"""
Database schema setup for Leadsec JobCard System
Run this file to create the database and tables
"""

import psycopg2
from psycopg2 import Error, sql
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create database and tables"""
    
    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='password',
            port=5432
        )
        
        # Set autocommit mode to create database
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'leadsec'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            cursor.execute("CREATE DATABASE leadsec OWNER leadsec_user")
            print("Database 'leadsec' created")
        else:
            print("Database 'leadsec' already exists")
        
        cursor.close()
        connection.close()
        
        # Connect to the leadsec database
        connection = psycopg2.connect(
            host='localhost',
            user='leadsec_user',
            password='password',
            port=5432,
            database='leadsec'
        )
        
        cursor = connection.cursor()
        
        # Create jobcards table
        create_jobcards_table = """
        CREATE TABLE IF NOT EXISTS jobcards (
            id SERIAL PRIMARY KEY,
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
            cost_estimate NUMERIC(10, 2),
            notes TEXT,
            client_signature TEXT,
            signature_timestamp TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by VARCHAR(255)
        );
        """
        
        cursor.execute(create_jobcards_table)
        print("Table 'jobcards' created or already exists")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON jobcards(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_client_email ON jobcards(client_email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON jobcards(created_at);")
        
        cursor.close()
        connection.commit()
        connection.close()
        
        print("Database setup completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()
