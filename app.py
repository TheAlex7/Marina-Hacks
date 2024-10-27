from flask import Flask, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/')
def contact():
    return send_file('contact.html')

# Route to handle file upload
@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Extract form fields and file
    age = request.form.get('age')
    sex = request.form.get('sex')
    localization = request.form.get('localization')
    file = request.files.get('SkinCondition')

    # Check if the request contains a file
    if 'SkinCondition' not in request.files:
        return "No file part in the request", 400

    # If no file is selected, redirect to home or show an error
    if file.filename == '':
        return "No selected file", 400

    # Check if the file type is allowed
    if file and allowed_file(file.filename):
        # Secure the filename and save it to the UPLOAD_FOLDER
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # data written into text/JSON file
        data = {
            'age': age,
            'sex': sex,
            'localization': localization,
            'filename': filename
        }

        # Define a file path for the metadata file (e.g., filename with .json extension)
        metadata_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_metadata.json")
        
        # Write metadata to the file
        with open(metadata_file_path, 'w') as metadata_file:
            json.dump(data, metadata_file)

        # Build query string with additional form data
        query_string = f'age={age}&sex={sex}&localization={localization}&filename={filename}'
        

        # Redirect back to main page (can probably change this when we send info into api)
        return redirect(url_for('index') + '?' + query_string)
    else:
        return "File type not allowed", 400

if __name__  == '__main__':
    # remove debug if app works fine!
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
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