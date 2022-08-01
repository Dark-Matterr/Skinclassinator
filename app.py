import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from keras.models import model_from_json
from core import Detection
from werkzeug import SharedDataMiddleware
import uuid

# Constant Model Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Flask Initialization and Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 2048 * 2048

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has image file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            random_name = str(uuid.uuid4().hex)
            filename = secure_filename(file.filename)
            filename = random_name+ "." + filename.split('.')[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('predict', filename = filename))
    return render_template('index.html') 


@app.route('/predict/<filename>')
def predict(filename):
    detection = Detection()
    pathfile = app.config['UPLOAD_FOLDER'] + '/' + filename
    img_resize = detection.resize_img(pathfile)
    classes_res , prob_res  = detection.predict(img_resize, model)
    predictions = {}
    for i in range(1,4):
        predictions[f"class{str(i)}"] = classes_res[i-1]
        predictions[f"prob{str(i)}"] = prob_res[i-1]
    path_to_file = '/uploads/' + filename
    return render_template('index.html', image = path_to_file, scroll = 'analyze', data=predictions)

if __name__ == '__main__':
    global model
    json_f = open('models/model.json', 'r')
    json_model = json_f.read()
    json_f.close()
    model = model_from_json(json_model)
    model.load_weights('models/model.h5')
    app.run(host='127.0.0.1', port=5000, debug=True)
