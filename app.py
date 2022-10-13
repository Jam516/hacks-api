from flask import Flask, jsonify
from flask_cors import CORS
from flask_caching import Cache
from sqlalchemy import create_engine
import pandas as pd
import os

config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

connect_url = os.environ.get("POSTGRESQL")
engine = create_engine(connect_url)

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')
    return response

@app.route('/')
@cache.cached()
def hacks():
    df = pd.read_sql_table(
        'sheet1',
        con=engine
    )
    output = df.to_json(orient='records')
    return output

if __name__ == '__main__':
    app.run()
