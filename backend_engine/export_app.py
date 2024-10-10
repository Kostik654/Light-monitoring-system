from flask import Flask, Response
import time

app = Flask(__name__)

metrics_data = {
    'requests_total': 0,
    'avg_response_time': 0,
    'uptime_seconds': time.time()
}

@app.route('/monitoring')
def metrics():
    uptime = time.time() - metrics_data['uptime_seconds']
    metrics_response = [
        '# HELP requests_total Total number of requests',
        '# TYPE requests_total counter',
        f'requests_total {metrics_data["requests_total"]}',
        '# HELP avg_response_time Average response time in seconds',
        '# TYPE avg_response_time gauge',
        f'avg_response_time {metrics_data["avg_response_time"]}',
        '# HELP uptime_seconds Uptime of the application in seconds',
        '# TYPE uptime_seconds gauge',
        f'uptime_seconds {uptime}',
    ]
    return Response("\n".join(metrics_response), mimetype='text/plain')
