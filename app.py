from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Server online! :D"

@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)


if __name__  == '__main__':
    # remove debug if app works fine!
    app.run(debug=True)

"""
Goal: send the image from the frontend to the backend
Response-Request Cycle
- Request-Response Cycle
- Application and Request Context
    - Context is used to make objects global and accessible
    - request cannot be a global variable bc applications need different requests for specific purposes
    - Context enables make objects global without them interfereing each other
    - Both have set vars: Application (current_app, g) and Request (request and session: dictionary that stores requests that need to be remembered)
    - when any of these contexts become pushed, they become global
- Request Dispatching
    - when app recieves a request, it will look at the functions that can be used to service the request
    - looks at it thru the applications url map
    - flask builds this map using the data map decorator
- Response Object
    - contains the information that the client included in the http request
    - Tries to get several pieces of information that the client sends
    - Ex. get_data, get_json, is_secure
    - Request Hooks: before, before_first, after, teardown
- Response:
    - Methods: set and delete_cookie, set and get data
    - Variables: status_code, headers, content_length, content_type
    - Another type of response exists called Redirect
- Representational State Transfer
"""