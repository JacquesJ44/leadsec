#!/usr/bin/env python
"""
Leadsec JobCard API - Main Entry Point
Run with: python run.py
"""

from app import create_app
import os

app = create_app(os.getenv('production'))

# if __name__ == '__main__':
#     app.run(
#         host='0.0.0.0',
#         port=int(os.getenv('FLASK_PORT', 5000)),
#         debug=os.getenv('FLASK_DEBUG', True)
#     )
