import bottle
import routes



app = routes.apps

if __name__ == '__main__':
    bottle.run(app=app,port=8080, reloader=True, debug=True)