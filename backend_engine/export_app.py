from flask import Flask, Response
import time

from logger import LogItOut

app = Flask(__name__)


@app.route('/monitoring')
def metrics():
    LogItOut(message_='Monitoring endpoint accessed')
    return {"status": "OK"}
