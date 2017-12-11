import os

from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename

import recognition
import splitter

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

@app.route('/splitImage', methods = ['POST'])
def split_image():
    f = request.files['file']

    filename = secure_filename(f.filename)

    path_to_save = os.path.join('static', 'uploads', filename.split('.')[0])

    if(os.path.isdir(path_to_save)):
        return jsonify({'message': 'This img is already uploaded!'})

    os.makedirs(path_to_save)

    save_path = os.path.join('static', 'uploads', filename.split('.')[0], filename)
    f.save(save_path)

    paths = splitter.split_image(save_path)

    print("Done to split the image")

    print("Start finding components")

    result = []

    for path in  paths:
        result.append(recognition.find_components(path, 'component'))  #this must to be changed automaticaly

    # result.append(recognition.find_components(paths[2], 'component'))  #this must to be changed automaticaly

    print('1111111111111111111111111111111111111111111111111111111111111')
    print(result)
    print('1111111111111111111111111111111111111111111111111111111111111')

    return jsonify({'path': paths})

if __name__ == '__main__':
   app.run(debug = True)
