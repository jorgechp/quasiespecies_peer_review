from server.flaskr.api import launch_api

app = launch_api()
app.run(host='0.0.0.0', port='7000', debug=True)