import requests
import PySimpleGUI as sg
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


#key de la API
def getKey():
    #api_file = open("C:/Users/felix/OneDrive/Escritorio/Felix/api-key.txt", "r")cañ
    #api_key = api_file.read()
    #api_file.close()
    api_key = "AIzaSyAoNhOreZM8gnr2blfjb82xG7p1jmOFHEU"
    return api_key


#Se pide el input del numero de direcciones
def arrDirecciones():
    arr_dir = []
    layout2 = [[sg.Text("Ingrese la dirección: ")],
        [sg.Input(key='Direccion')],
        [sg.Text(size=(100,1), key='-OUTPUT-')],
        [sg.Button('Siguiente'), sg.Button('Salir'), sg.Button('Terminar')]]
    win2 = sg.Window('Rutas MDR', layout2, margins=(300,300))
    while True:
        event2, value2 = win2.read()
        if event2 == 'Salir' or sg.WINDOW_CLOSED:
            win2.close()
            return 0
        if event2 == 'Siguiente':
            arr_dir.append(value2['Direccion'])
            win2['-OUTPUT-'].update('Solo se ingresó una dirección: ' + value2['Direccion'])
            win2['Direccion'].update('')
        if event2 == 'Terminar':
            return arr_dir
    
        
    
def filaDir():        
    fila = []
    fila.append("ZonaOblatos, Calle Sebastian Allende 444, Col, Blanco y Cuéllar, 44730 Guadalajara, Jal.")
    return fila

def retrieveMaps(arrDir):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get('https://www.google.com.mx/maps/preview')
    for i in range(len(arrDir)):
        if i == 0:
            browser.find_element_by_name("q").send_keys(arrDir[i])
            browser.find_element_by_class_name('searchbox-directions-icon').click()
            browser.find_element_by_class_name('tactile-searchbox-input').send_keys(arrDir[i])
        elif i == 1:
            browser.find_element_by_css_selector("div[aria-label='Elige un punto de partida o haz clic en el mapa...']").send_keys("Molinos Don Ramon")
            browser.find_element_by_class_name('tactile-searchbox-input').send_keys(Keys.ENTER)
        elif i!= 1 and 0:
            browser.find_element_by_class_name('widget-direction-icon waypoint-add').click()
            browser.find_element_by_css_selector(["aria-haspopup=true"]).send_keys(arrDir[i])
            browser.find_element_by_class_name('tactile-searchbox-input').send_keys(Keys.ENTER)
        elif i == len(arrDir)-1 and len(arrDir)>2:
            browser.find_element_by_class_name('blue-link section-directions-action-button').click()
            browser.find_element_by_class_name('widget-pane-link').click()
            break

#Se realiza el request de la API de google maps
def apiMaps(arr,fila):
    if len(arr) != 0:
        tiempo_arr = []
        despliegue_arr = []
        while(len(fila) != 0):
            for i in range (len(arr)):
                url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"
                r = requests.get(url + "origins=" + fila[0] + "&destinations=" + arr[i] + "&key=" + getKey())
                time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
            
                if(len(arr) > 1):
                    tiempoNuevo = time[0]+time[1]
                    if time[2] == "h":
                        tiempoHora = int(time[0])*60
                        timepoNuevo = time[8]+time[9]
                        tiempoNuevo2 = int(tiempoNuevo) + tiempoHora
                        tiempo_arr.append(int(tiempoNuevo2))
                    else:    
                        tiempo_arr.append(int(tiempoNuevo))
                else:
                    sg.popup(fila[0])
                    despliegue_arr.append(fila.pop(0))
                    despliegue_arr.append(arr[0])
                    sg.popup(arr[0])
                    retrieveMaps(despliegue_arr)
                    return arr[0]
            
            if len(fila) == 1:
                tiempo_min = min(tiempo_arr)
                tiempo_index = tiempo_arr.index(tiempo_min)
                        
                fila.append(arr[tiempo_index])
                despliegue_arr.append(arr.pop(tiempo_index))
                sg.popup(fila[0])
                fila.pop(0)
                tiempo_arr = []   
            else:
                break 
    else:
        print("Nada mas se ingreso una direccion")       
             
            
layout = [[sg.Text("Bienvenido a Rutas La Mejicana ")],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Iniciar'), sg.Button('Salir')]]

window = sg.Window('Rutas MDR', layout, margins=(500,300))


while True:
    event1, values1 = window.read()
    # See if user wants to quit or window was closed
   
    if event1 == sg.WINDOW_CLOSED or event1 == 'Salir':
        break
    elif event1 == 'Iniciar':
        window.Hide()
        apiMaps(arrDirecciones(),filaDir())
        break

# Finish up by removing from the screen
window.close()
#num = input("Ingrese el numero de direcciones: ")
#apiMaps(arrDirecciones(num),filaDir())



