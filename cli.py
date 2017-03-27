#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import recognition

classifiers = recognition.classifier_list()

if len(sys.argv) != 3:
    print("./cli.py IMAGE_PATH window")
    raise Exception("need 2 arguments: file and classifier")

if sys.argv[2] not in classifiers:
    print(recognition.classifier_list())
    raise Exception("invalid classifier %s" % sys.argv[2])

print(recognition.label_image(sys.argv[1], sys.argv[2]))
