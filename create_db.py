"""
Database schema setup for Leadsec JobCard System
Run this file to create the database and tables
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create database and tables"""
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            port=3306
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS leadsec")
        print("Database 'leadsec' created or already exists")
        
        # Select database
        cursor.execute("USE leadsec")
        
        # Create jobcards table
        create_jobcards_table = """
        CREATE TABLE IF NOT EXISTS jobcards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_title VARCHAR(255) NOT NULL,
            job_description LONGTEXT,
            client_name VARCHAR(255) NOT NULL,
            client_email VARCHAR(255) NOT NULL,
            client_phone VARCHAR(20),
            service_location LONGTEXT NOT NULL,
            technician_name VARCHAR(255) NOT NULL,
            service_date DATE NOT NULL,
            labor_hours FLOAT,
            materials_used LONGTEXT,
            cost_estimate DECIMAL(10, 2),
            notes LONGTEXT,
            client_signature LONGTEXT,
            signature_timestamp DATETIME,
            status VARCHAR(50) DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_by VARCHAR(255),
            INDEX idx_status (status),
            INDEX idx_client_email (client_email),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_jobcards_table)
        print("Table 'jobcards' created or already exists")
        
        cursor.close()
        connection.commit()
        connection.close()
        
        print("Database setup completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()
