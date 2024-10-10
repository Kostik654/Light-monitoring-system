from quart import Quart

app = Quart(__name__)


@app.route('/monitoring')
async def metrics():

    #  TEST DATA

    data = {
        "metric_1": 123,
        "metric_2": 456,
        "metric_3": 789
    }

    prometheus_data = f"""
    # HELP metric_1 Description of metric_1
    metric_1 {data['metric_1']}
    # HELP metric_2 Description of metric_2
    metric_2 {data['metric_2']}
    # HELP metric_3 Description of metric_3
    metric_3 {data['metric_3']}
    """
    return prometheus_data, 200, {'Content-Type': 'text/plain; version=0.0.4'}
