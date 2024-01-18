import cv2
import numpy as np
import os
from PIL import Image
import pickle
import dlib
import sys
import imutils
import face_recognition

training_path = 'dataset/'
pickle_filename = "face_encodings_custom.pickle"

def load_encodings(path_dataset):
  
  list_encodings = []
  list_names = []

  subdirs = [os.path.join(path_dataset, f) for f in os.listdir(path_dataset)]

  for subdir in subdirs:
    
    name = subdir.split(os.path.sep)[-1]
    images_list = [os.path.join(subdir, f) for f in os.listdir(subdir) if not os.path.basename(f).startswith(".")]

    for image_path in images_list:
      img = cv2.imread(image_path)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

      print(name + " <-- " + image_path)

      face_roi = face_recognition.face_locations(img, model="cnn")  

      (start_y, end_x, end_y, start_x) = face_roi[0]
      roi = img[start_y:end_y, start_x:end_x]
      roi = imutils.resize(roi, width=100)
      cv2.imshow('face', cv2.cvtColor(roi, cv2.COLOR_RGB2BGR))

      img_encoding = face_recognition.face_encodings(img, face_roi)
      
      if (len(img_encoding) > 0):
        img_encoding = img_encoding[0]
        list_encodings.append(img_encoding)
        list_names.append(name)
      else:
        print("Couldn't encode face from image => {}".format(image_path))

  return list_encodings, list_names

list_encodings, list_names = load_encodings(training_path)

print(len(list_encodings))
print(list_names)

encodings_data = {"encodings": list_encodings, "names": list_names}
with open(pickle_filename, "wb") as f:
  pickle.dump(encodings_data, f)
  
print('\n')
print('Rostos codificados com sucesso!')