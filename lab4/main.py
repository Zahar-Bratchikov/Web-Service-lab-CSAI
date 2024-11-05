from fastapi import FastAPI
from web_app import api_router
from uvicorn import Config, Server

app = FastAPI()
app.include_router(api_router)

if __name__ == '__main__':
    config = Config(app=app, host="localhost", port=8080)
    server = Server(config)
    server.run()
