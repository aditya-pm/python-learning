from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def home() -> dict[str, str]:
    # python dict is automatically converted to JSON object
    return {"message": "Hello World!"}


# stack decorators to target multiple endpoints to the same page/response
# use HTMLResponse to return as HTML string
# use include_in_schema=False to prevent endpoint showing up in documentation
# HTML endpoints are typically viewed in the browser,
# so they are often excluded from API documentation
@app.get("/about", response_class=HTMLResponse)
@app.get("/info", response_class=HTMLResponse)
def about() -> str:
    return "<h1>This is the HTML response page</h1>"


# run with: fastapi dev 00_basic.py
# localhost:8000/
# for documentation: localhost:8000/docs or localhost:8000/redoc
