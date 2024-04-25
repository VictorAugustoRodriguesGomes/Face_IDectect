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

def recognize_faces(image, list_encodings, list_names, resizing=0.250, tolerance=0.4):
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
    
    num_format = f"{face_distances[best_match_index]:.2f}"
    conf_values.append(str(num_format))

  face_locations = np.array(face_locations)
  face_locations = face_locations / resizing
  
  return face_locations.astype(int), face_names, conf_values

def show_recognition(frame, face_locations, face_names, conf_values):
  for face_loc, name, conf in zip(face_locations, face_names, conf_values):
    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]  

    conf = conf
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)   
    
  return frame

def window_main():
    font_h1 = ("Arial", 30)
    font_h2 = ("Arial", 25)
    font_h3 = ("Arial", 10)
    
    sg.theme('DarkTanBlue')
    
    col1 = [
        [sg.Text('Face IDectect', font=font_h1, text_color='#ffffff')],
        [sg.Image(filename="", key="cam1", background_color='#ff00ff')],
    ]
    
    col2 = [
        [sg.Text('Análises: ', font=font_h1, text_color='#ffffff')],
        [sg.Text('Face não detectada!', key='username', font=font_h2, text_color='#ffffff')],
        [sg.Text('', key='conf_label', text_color='#ffffff', font=font_h2)],  # Elemento de texto para a confiabilidade
        [sg.Text('[0.0]', key='usertrust', text_color='#ffffff', font=font_h2)],
        [sg.Text('', key='userra', text_color='#ffffff', font=font_h2)],
        [sg.Text('', key='userage', text_color='#ffffff', font=font_h2)],
        [sg.Text('', key='conf_message', text_color='#ff0000', font=font_h2)],
    ]
    
    menu_webcan = [[sg.Image(filename="", key="cam1")]]
    
    menu_def = [['Sobre', 'Sobre'], ['Ajuda', 'Ajuda'], ['Sair', 'Sair']]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Column(col1), sg.Column(col2)],
    ]
    #990, 380
    return sg.Window( 'Face IDectect', layout, size = (1000, 370), background_color='#242834', finalize=True)

def window_intro():
    font_h1 = ("Arial", 50)
    font_h2 = ("Arial", 25)

    sg.theme('DarkTanBlue')
    layout2 = [
        [sg.Image("icone.png", size=(1000, 500))],
    ]

    return sg.Window('Face IDectect', layout2, size=(1000, 500), background_color='#ffffff', finalize=True)

def window_Sobre():
    font_h1 = ("Arial", 30)
    font_h2 = ("Arial", 15)

    sg.theme('DarkTanBlue')

    col1 = [
        [sg.Image("icone.png", size=(600, 200))],
    ]

    layout3 = [
        [sg.Image("icone.png", size=(750, 280))],
        [sg.Text(' ', text_color='#ffffff', font=font_h2, justification='center')],
        [sg.Text('Emerson Silva Pestana - RA: T602H12', text_color='#ffffff', font=font_h2, justification='center')],
        [sg.Text('Kaique Santos Lima de Oliveira - RA: D2901JO', text_color='#ffffff', font=font_h2, justification='center')],
        [sg.Text('Lucas Santos Camargo - RA: N4587E4', key='usertrust', text_color='#ffffff', font=font_h2, justification='center')],
        [sg.Text('Victor Augusto Rodrigues Gomes - RA: N481GD4', key='userra', text_color='#ffffff', font=font_h2, justification='center')],
    ]
  
    return sg.Window( 'Face IDectect', layout3, size = (500, 470), background_color='#242834', finalize=True)

def window_Ajuda():
    font_h1 = ("Arial", 30)
    font_h2 = ("Arial", 15)

    layout = [
        [sg.Text('Ajuda', font=font_h1)],
        [sg.Text('1 - Para o rosto ser reconhecido, deve-se ficar alinhado.', font=font_h2)],
        [sg.Text('2 - Com a presença de luzes adequadas.', font=font_h2)],
        [sg.Text('3 - Não fazer movimentos bruscos durante a detecção.', font=font_h2)],
        [sg.Text('4 - Garanta que o rosto esteja em um ângulo adequado para captura', font=font_h2)],
    ]

    return sg.Window('Ajuda', layout, size=(680, 200), background_color='#242834', finalize=True)

windowMain, windowIntro, windowSobre, windowAjuda = window_main(), window_intro(), window_Sobre(), window_Ajuda()

qual_janela = 'windowIntro'
introTime = 0
while True:
    Window, event, values = sg.read_all_windows(timeout=20)
   
    start_time = time.time()

    if qual_janela == 'windowIntro' and introTime == 300:
      windowMain.un_hide()
      windowIntro.hide()
      windowAjuda.hide()
      introTime = 0
      qual_janela = 'windowMain'
    
    if qual_janela == 'windowIntro':
      windowMain.hide()
      windowSobre.hide()
      windowAjuda.hide()
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
      windowAjuda.hide()
      windowSobre.un_hide()
      
    if Window == windowMain and event == "Ajuda":
      qual_janela = 'windowAjuda'
      windowMain.hide()
      windowIntro.hide()
      windowAjuda.hide()
      windowAjuda.un_hide()
      
    if Window == windowSobre and event == sg.WIN_CLOSED:
      qual_janela = 'windowMain'
      windowSobre.hide()
      windowIntro.hide()
      windowAjuda.hide()
      windowMain.un_hide()
      
    if Window == windowAjuda and event == sg.WIN_CLOSED:
      qual_janela = 'windowMain'
      windowSobre.hide()
      windowIntro.hide()
      windowAjuda.hide()
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
        windowMain["userra"].update('RA: N481GD4')
        windowMain["userage"].update('Idade: 23 anos')
        
      if face_names == ['dataset/Lucas']:
        windowMain["username"].update('Nome: Lucas')
        windowMain["usertrust"].update(conf_values)
        windowMain["userra"].update('RA: N4587E4')
        windowMain["userage"].update('Idade: 22 anos')
      
      if face_names == []:
        windowMain["username"].update('Face não detectada!')
        windowMain["usertrust"].update('[0.0]')
        windowMain["userra"].update('')
        windowMain["userage"].update('')
      
      if face_names == ['Not identified']:
        windowMain["username"].update('Face detectada! ')
        windowMain["usertrust"].update('[100%]')
        windowMain["userra"].update('Reconhecimento facial')
        windowMain["userage"].update('Não identificado') 
 
windowIntro.close()
video_capture.release()
cv2.destroyAllWindows()