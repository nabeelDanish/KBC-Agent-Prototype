"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  Flask API
    - Provides the main access point to run the front_end API application
    - which communicates over the web using Https to provide an interface to our project
"""

# Imports
from app import app

# Running the Main App
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
