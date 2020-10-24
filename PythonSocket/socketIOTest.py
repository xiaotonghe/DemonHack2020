from aiohttp import web
import socketio

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(async_mode='aiohttp')
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

# We kick off our server
if __name__ == '__main__':
    web.run_app(app)
