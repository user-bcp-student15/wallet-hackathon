import os

import psycopg
from flask import Flask, jsonify
from psycopg import OperationalError

app = Flask(__name__)


@app.get("/health")
def health():
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "wallet"),
            user=os.getenv("DB_USER", "wallet"),
            password=os.getenv("DB_PASSWORD", ""),
            connect_timeout=3,
        ) as connection:
            connection.execute("SELECT 1")
    except OperationalError:
        return jsonify(status="unhealthy", database="unavailable"), 503

    return jsonify(status="ok", database="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))