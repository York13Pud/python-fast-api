# FastAPI Notes

## Basics


FastAPI uses uvicorn to run the application as a web server. To run the app, run the below in the terminal:

``` console
uvicorn main:app --reload
```

* uvicorn: The command for the server to run the app.
* main: The name of the file that has the start code for the application.
* app: The name you gave to the application that creates a FastAPI instance.
* --reload: This is optional. It will check for file saves and reload the server when it detects any.

Once the server is running, it will tell you what the URL it is running on and the TCP port. This is typically:

[http://127.0.0.1:8000](http://127.0.0.1:8000 "http://127.0.0.1:8000")

In addition, you can view the API docs at the below URL (it uses SwaggerUI to render):

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs "http://127.0.0.1:8000/docs")
