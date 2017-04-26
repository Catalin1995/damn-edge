import os

from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename

import recognition

app = Flask(__name__, static_folder="static")

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/classifiers')
def get_classifisers():
    return jsonify({"classifiers": recognition.classifier_list()})

@app.route('/')
def home():
    return render_template('upload.html')
#    return render_template('upload.html', classifiers = recognition.classifier_list())

@app.route('/upload', methods = ['POST'])
def upload_file():
    f = request.files['file']

    filename = secure_filename(f.filename)
    save_path = os.path.join('static', 'uploads', filename)
    f.save(save_path)

    classifier = request.values.get("classifier")

    output = recognition.label_image(save_path, classifier)
    output['url'] = os.path.join('/uploads', filename)
    return jsonify(output)

if __name__ == '__main__':
   app.run(debug = True)
