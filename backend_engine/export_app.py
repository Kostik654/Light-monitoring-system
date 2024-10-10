from flask import Flask, Response
import time

app = Flask(__name__)

@app.route('/monitoring')
async def metrics():

    return {"status": "OK"}
