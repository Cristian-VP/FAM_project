# all the imports
from fastapi import FastAPI

# creating a server with python FastAPI
app = FastAPI()

# hello world endpoint
@app.get("/")
def read_root(): # function that is binded with the endpoint
    return {"Hello": "World"}