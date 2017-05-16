from glob import glob
import os
from os import listdir
from os.path import join

import tensorflow as tf
import sys

def label_image(image_path, classifier):
  # change this as you see fit
  labels_path = "classifiers/%s/retrained_labels.txt" % classifier
  graph_path = "classifiers/%s/retrained_graph.pb" % classifier

  # Read in the image_data
  image_data = tf.gfile.FastGFile(image_path, 'rb').read()

  # Loads label file, strips off carriage return
  label_lines = [line.rstrip() for line in tf.gfile.GFile(labels_path)]

  # Unpersists graph from file
  with tf.gfile.FastGFile(graph_path, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      _ = tf.import_graph_def(graph_def, name='')

  with tf.Session() as sess:
      # Feed the image_data as input to the graph and get first prediction
      softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

      predictions = sess.run(softmax_tensor, \
               {'DecodeJpeg/contents:0': image_data})

      # Sort to show labels of first prediction in order of confidence
      top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
      print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
      print(top_k)
      print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
      result = {}
      for node_id in top_k:
          human_string = label_lines[node_id]
          score = predictions[0][node_id]
          result[human_string] = "%.5f" % score

  tf.reset_default_graph()  #to remove memory leak
  return result

def classifier_list():
  array = []
  for x in glob('classifiers/*'):
    array.append(x.split('/')[1])
  return array

def find_components(images_path):
  classifier = 'component'
  # change this as you see fit
  labels_path = "classifiers/%s/retrained_labels.txt" % classifier
  graph_path = "classifiers/%s/retrained_graph.pb" % classifier

  images_paths = []
  for f in listdir(images_path):
        if f.endswith(('png', 'jpg', 'jpeg')):
              images_paths.append(os.path.join(images_path, f))

  result = { "back car window": {"score": 0, "path_to_image": ""},
            "back left headlight": {"score": 0, "path_to_image": ""},
            "back right headlight": {"score": 0, "path_to_image": ""}
          }

  for image_path in images_paths:
    print("find for " + image_path)
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile(labels_path)]

    # Unpersists graph from file
    with tf.gfile.FastGFile(graph_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        # result = {}
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            if(float(result[human_string]['score']) < float("%.5f" % score)):
                  result[human_string]['score'] = "%.5f" % score
                  result[human_string]['path_to_image'] = image_path

    tf.reset_default_graph()  #to remove memory leak

  return result