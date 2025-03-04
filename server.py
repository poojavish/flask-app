from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


# Database connection
db_config = {
    "host": os.environ.get("DB_HOST", "shuttle.proxy.rlwy.net"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "your_password"),
    "database": os.environ.get("DB_NAME", "murder_mystery")
}

def execute_query(user_query):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Restrict queries to SELECT only
    if not user_query.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed!"}

    try:
        cursor.execute(user_query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return {"columns": columns, "data": data}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

@app.route('/query', methods=['POST'])
def query_db():
    user_query = request.json.get("query")
    result = execute_query(user_query)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from environment
    app.run(host="0.0.0.0", port=port, debug=True)