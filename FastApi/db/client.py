# --- MongoDB ---

# Download: https://www.mongodb.com/try/download/community
# Install: https://www.mongodb.com/docs/manual/installation/
# Modulo conexión MongoDB: pip install pymongo

from pymongo import MongoClient

# Base de datos local
#db_client = MongoClient().local

# Base de datos remota
db_client = MongoClient("mongodb+srv://<USERNAME>:0SDZ0NYk7zKqkFGU@cluster0.7frsrtk.mongodb.net/?retryWrites=true&w=majority").test