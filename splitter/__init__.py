import tensorflow as tf
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

def split_image(file_path):
    filename_queue = tf.train.string_input_producer([file_path]) #  list of files to read

    reader = tf.WholeFileReader()
    key, value = reader.read(filename_queue)

    my_img = tf.image.decode_jpeg(value)

    init_op = tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        image = my_img.eval()
        move = int(image.shape[0] / 20)

        original_width = image.shape[0]
        original_height = image.shape[1]

        new_width_image = int(original_width / 4)
        new_height_image = int(original_height / 2)

        filename = file_path.split(os.sep)[-1].split('.')[0]
        path = file_path.split(os.sep)
        path.pop()
        path = os.path.join(*path, 'labels')

        os.makedirs(path)
    
    classifiers = [
        {   
            'classifier': 'back_car_window',
            'end_x': 1,
            'end_y': 1/2,
            'start_x': 0,
            'start_y': 0,
            'move': 40,
            'reverse': False,
            'new_width_image': 1/2,
            'new_height_image': 1/4,
            'filename': filename
        },
        {
            'classifier': 'back_left_headlight',
            'end_x': 1/2,
            'end_y': 1,
            'start_x': 0,
            'start_y': 0,
            'move': 40,
            'reverse': False,
            'new_width_image': 1/5,
            'new_height_image': 1/4,
            'filename': filename
        },
        {
            'classifier': 'back_right_headlight',
            'end_x': 1,
            'end_y': 1,
            'start_x': 1/2,
            'start_y': 0,
            'move': 40,
            'reverse': True,
            'new_width_image': 1/5,
            'new_height_image': 1/4,
            'filename': filename
        }
    ]

    for classifier in classifiers:
        generate_labels_for_classifier(image, path, classifier)

    return path

def generate_labels_for_classifier(image, path, classifier):
    original_height = image.shape[0]
    original_width = image.shape[1]

    new_width_image = int(original_width * classifier['new_width_image'])
    new_height_image = int(original_height * classifier['new_height_image'])

    end_x = int(original_width * classifier['end_x'])
    end_y = int(original_height * classifier['end_y'])

    move = int(original_width / classifier['move']) 

    i = int(original_height * classifier['start_y'])
    j = int(original_width * classifier['start_x'])

    new_path = os.path.join(path, classifier['classifier'])

    os.makedirs(new_path)

    while i + new_height_image <= end_y:
        while j + new_width_image <= end_x:
            with tf.Graph().as_default(), tf.Session() as sess:
                cropped_image = sess.run(tf.image.crop_to_bounding_box(image, i, j, new_height_image, new_width_image))
                new_filename = classifier['filename'] + "_" + str(i) + "_" + str(j) + ".jpg"
                save_image(cropped_image, new_path, new_filename)
            j = j + move
        i = i + move
        j = int(original_width * classifier['start_x'])

def save_image(image, path, filename):
    a = Image.fromarray(image, "RGB")
    a.save(os.path.join(path, filename))
