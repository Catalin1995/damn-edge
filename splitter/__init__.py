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
    
    generate_labels_for_back_window(image, original_width, original_height, move, path, filename)
    generate_labels_for_back_left_headlight(image, original_width, original_height, move, path, filename)

    classifiers = [
        'back_car_window': {
            'end_x': 2,
            'end_y': 1,
            'start_x': 0,
            'start_y': 0,
            'move': 20,
            'reverse': True,
            'new_width_image': 4,
            'new_height_image': 4
        }
    ]

    generate_labels_for_classifier(image, path, classifier)

    return path

def generate_labels_for_classifier(image, path, classifier):
    original_height = image.shape[0]
    original_width = image.shape[1]

    new_width_image = int(original_width / classifier['new_width_image'])
    new_height_image = int(original_height / classifier['new_height_image'])

    end_x = int(original_width / classifier['end_x'])
    end_y = int(original_height / classifier['end_y'])
    
    i = original_width / move
    j = original_height / move

def generate_labels_for_back_left_headlight(image, original_width, original_height, move, path, filename):
    original_height = image.shape[0]
    original_width = image.shape[1]

    new_width_image = int(original_width / 4)
    new_height_image = int(original_height / 4)

    end_x = int(original_width / 2)
    end_y = original_height

    i = 0
    j = original_height / move

    new_path = os.path.join(path, 'back_left_headlight')

    os.makedirs(new_path)

    while i * move + new_height_image < end_y:
        while j * move + new_width_image < end_x:
            with tf.Graph().as_default(), tf.Session() as sess:
                flipped_image = sess.run(tf.image.crop_to_bounding_box(image, i * move, j * move , new_height_image, new_width_image))
                new_filename = filename + "_" + str(i) + "_" + str(j) + '.jpg'
                save_image(flipped_image, new_path, new_filename)
            j = j + 1
        i = i + 1
        j = 0

def generate_labels_for_back_window(image, original_width, original_height, move, path, filename):
    original_height = image.shape[0]
    original_width = image.shape[1]

    new_height_image = int(original_height / 4)
    new_width_image = int(original_width / 2)

    end_x = original_width
    end_y = int(original_height / 2)

    i = 0
    j = 0

    new_path = os.path.join(path, 'back_car_window')

    os.makedirs(new_path)

    while i * move + new_height_image < end_y:
        while j * move + new_width_image < end_x:
            with tf.Graph().as_default(), tf.Session() as sess:
                flipped_image = sess.run(tf.image.crop_to_bounding_box(image, i * move, j * move , new_height_image, new_width_image))
                new_filename = filename + "_" + str(i) + "_" + str(j) + '.jpg'
                save_image(flipped_image, new_path, new_filename)
            j = j + 1
        i = i + 1
        j = 0

def save_image(image, path, filename):
    a = Image.fromarray(image, "RGB")
    a.save(os.path.join(path, filename))
