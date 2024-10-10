from quart import Quart, jsonify

app = Quart(__name__)


@app.route('/monitoring')
async def metrics():
    return jsonify({"status": "OK"})