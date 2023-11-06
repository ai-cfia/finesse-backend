# src/main.py
from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/')
def read_root():
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": unix_timestamp}
