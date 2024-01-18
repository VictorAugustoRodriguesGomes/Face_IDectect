import time
import cv2
import PySimpleGUI as sg
import numpy as np
import os
import pickle
import re
import face_recognition

camera_Width  = 600 
camera_Heigth = 480 
frameSize = (camera_Width, camera_Heigth)
video_capture = cv2.VideoCapture(0)
time.sleep(2.0)

pickle_name = "face_encodings_custom.pickle" 

data_encoding = pickle.loads(open(pickle_name, "rb").read())
list_encodings = data_encoding["encodings"]
list_names = data_encoding["names"]

def recognize_faces(image, list_encodings, list_names, resizing=0.25, tolerance=0.6):
  image = cv2.resize(image, (0, 0), fx=resizing, fy=resizing)
  img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  face_locations = face_recognition.face_locations(img_rgb)
  face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

  face_names = []   
  conf_values = []    
  for encoding in face_encodings:
    matches = face_recognition.compare_faces(list_encodings, encoding, tolerance=tolerance)
    name = "Not identified"
    
    face_distances = face_recognition.face_distance(list_encodings, encoding)
    best_match_index = np.argmin(face_distances)  
    if matches[best_match_index]:
      name = list_names[best_match_index] 
    face_names.append(name) 
    conf_values.append(face_distances[best_match_index])
    
  face_locations = np.array(face_locations)
  face_locations = face_locations / resizing
  return face_locations.astype(int), face_names, conf_values

def show_recognition(frame, face_locations, face_names, conf_values):
  for face_loc, name, conf in zip(face_locations, face_names, conf_values):
    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]  

    conf = "{:.8f}".format(conf)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)   
    
  return frame

def window_main():
    font_h1 = ("Arial", 40)
    font_h2 = ("Arial", 25)
    font_h3 = ("Arial", 10)
    
    sg.theme('Reddit')
    
    menu_main = [ ['Sobre'], ['Sair'],]
    
    title = [sg.Text('Face IDectect', background_color='#ffffff', text_color='#000000', font=font_h1) ]
    
    col1 = [ 
            [sg.Image(filename="", key="cam1", background_color='#ff00ff' )],   
        ]
    
    col2 = [
            [sg.Text('Face IDectect', background_color='#ffffff', text_color='#000000', font=font_h1)],
            [sg.Text('Face não detectada!', key='username', background_color='#ffffff', text_color='#000000', font=font_h2)],
            [sg.Text('Confiabilidade :', background_color='#ffffff', text_color='#000000', font=font_h2)],
            [sg.Text('[0.0]', key='usertrust', background_color='#ffffff', text_color='#000000', font=font_h2)],
            [sg.Text('', key='userra', background_color='#ffffff', text_color='#000000', font=font_h2)],
            [sg.Text('', key='userage', background_color='#ffffff', text_color='#000000', font=font_h2)],
            [sg.Text('', key='usercpf', background_color='#ffffff', text_color='#000000', font=font_h2)],
    ]
    
    menu_webcan = [[sg.Image(filename="", key="cam1")]]
    
    layout = [
        [[sg.Button('Sobre', button_color=('black', 'white'), font=font_h3), sg.Button('Sair', button_color=('black', 'white'), font=font_h3)]],
        [sg.Column(col1), sg.Column(col2)], 
    ]
    return sg.Window( 'Face IDectect', layout, size = (1010, 500), background_color='#999999', finalize=True)

def window_intro():
    font_h1 = ("Arial", 50)
    font_h2 = ("Arial", 25)
      
    sg.theme('Reddit')
    layout2 = [
      [sg.Image("icone.png", size=(1000, 500))],
       
      ]
    
    return sg.Window( 'Face IDectect', layout2, size = (1000, 500), background_color='#ffffff', finalize=True)

def window_Sobre():
  font_h1 = ("Arial", 50)
  font_h2 = ("Arial", 25)
      
  sg.theme('Reddit')
  
  col1 = [ 
           [sg.Image("icone.png", size=(600, 200))],
        ]
  
  layout3 = [
      [sg.Image("icone.png", size=(750, 300))],
      [sg.Text('Emerson Silva Pestana - RA: T602H12', background_color='#ffffff', text_color='#000000', font=font_h2)],
      [sg.Text('Kaique Santos Lima de Oliveira - RA: D2901JO', background_color='#ffffff', text_color='#000000', font=font_h2)],
      [sg.Text('Lucas Santos Camargo - RA: N4587E4', key='usertrust', background_color='#ffffff', text_color='#000000', font=font_h2)],
      [sg.Text('Victor Augusto Rodrigues Gomes - RA: N481GD4', key='userra', background_color='#ffffff', text_color='#000000', font=font_h2)],
         
      ]
  
  return sg.Window( 'Face IDectect', layout3, size = (750, 520), background_color='#ffffff', finalize=True)

windowMain, windowIntro, windowSobre = window_main(), window_intro(), window_Sobre()

qual_janela = 'windowIntro'
introTime = 0
while True:
    Window, event, values = sg.read_all_windows(timeout=20)
   
    start_time = time.time()

    if qual_janela == 'windowIntro' and introTime == 300:
      windowMain.un_hide()
      windowIntro.hide()
      introTime = 0
      qual_janela = 'windowMain'
    
    if qual_janela == 'windowIntro':
      windowMain.hide()
      windowSobre.hide()
      introTime = introTime + 1
     
    if Window == windowMain and event == sg.WIN_CLOSED: 
        break
      
    if Window == windowIntro and event == sg.WIN_CLOSED: 
        windowIntro.hide()
        windowMain.un_hide()
        qual_janela = 'windowMain'
        
    if Window == windowMain and event == 'Sair':
        break
      
    if Window == windowMain and event == "Sobre":
      qual_janela = 'windowSobre'
      windowMain.hide()
      windowIntro.hide()
      windowSobre.un_hide()
      
    if Window == windowSobre and event == sg.WIN_CLOSED:
      qual_janela = 'windowMain'
      windowSobre.hide()
      windowIntro.hide()
      windowMain.un_hide()
    
    if qual_janela == 'windowMain':
      start_time = time.time()
      ret, frameOrig = video_capture.read()
      frame = cv2.resize(frameOrig, frameSize)
      imgbytes = cv2.imencode(".png", frame)[1].tobytes()
      windowMain["cam1"].update(data=imgbytes)
    
      face_locations, face_names, conf_values = recognize_faces(frame, list_encodings, list_names, 0.25)

      processed_frame = show_recognition(frame, face_locations, face_names, conf_values)
    
      imgbytes = cv2.imencode(".png", frame)[1].tobytes()
      windowMain["cam1"].update(data=imgbytes)
      
      if face_names == ['dataset/Victor']:
        windowMain["username"].update('Nome: Victor')
        windowMain["usertrust"].update(conf_values)
        windowMain["userra"].update('RA: N481GD-4')
        windowMain["userage"].update('Idade: 23 anos')
        windowMain["usercpf"].update('CPF: 147.512.852-52')
      
      if face_names == []:
        windowMain["username"].update('Face não detectada!')
        windowMain["usertrust"].update('[0.0]')
        windowMain["userra"].update('')
        windowMain["userage"].update('')
        windowMain["usercpf"].update('')
      
      if face_names == ['Not identified']:
        windowMain["username"].update('Face detectada! ')
        windowMain["usertrust"].update('[100%]')
        windowMain["userra"].update('Reconhecimento facial')
        windowMain["userage"].update('Não identificado')
        windowMain["usercpf"].update('')  
 
windowIntro.close()
video_capture.release()
cv2.destroyAllWindows()