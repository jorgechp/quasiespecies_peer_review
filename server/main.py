from server.flaskr.api import launch_api

app = launch_api(instance_path='/home/jorge/Documents/proyectos/quasiespecies_peer_review/server')
app.run(host='0.0.0.0', port='7000', debug=True)