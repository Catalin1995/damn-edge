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

      new_width_image = int(original_width / 5)
      new_height_image = int(original_height / 5)

      new_images = []
      i = 0
      j = 0

      while i * move + new_width_image < original_width:
          while j * move + new_height_image < original_height:
              flipped_image = sess.run(tf.image.crop_to_bounding_box(image, i * move, j * move , new_width_image, new_height_image))
              new_images.append(flipped_image)
              j = j + 1
          i = i + 1
          j = 0

      filename = file_path.split(os.sep)[-1].split('.')[0]
      path = file_path.split(os.sep)
      path.pop()
      path = os.path.join(*path, 'labels')

      os.makedirs(path)

      for i in range(len(new_images)):
          a = Image.fromarray(new_images[i], "RGB")
          newFileName = filename + str(i) + '.jpg'
          a.save(os.path.join(path, newFileName))

      return path
