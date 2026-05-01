import PySimpleGUI as sg
import PySimpleGUI as psg
import start,tts,v2t
from functions import main
import tkinter as tk


def voicemode():
    layout = [[sg.Text("Please say a query after pressing the button",justification="center")],
              [sg.Button("Take Input")],
              [sg.Text("Your Input:"), sg.Multiline(size=(30,2),key='-input-')],
              [sg.Text("Output:"), sg.Multiline(size=(50,10),key='-output-')]]
    
    window = sg.Window("Voice Mode",layout,resizable=True)

    while True:
        events, values = window.read()
        if(events == "Take Input"):
            inp = v2t.stt()
            window['-input-'].update(inp)
            out = main(inp)
            if(out == "sleep"):
                tts.say("goodbye")
                window.close()
                login_window()
            else:
                window['-output-'].update(out)
                tts.say(out)
        
                
#                window.close()
#                textmode(output)
        if(events == sg.WIN_CLOSED):
            window.close()
            exit()

def textmode(output=" "):
    layout = [[sg.Text("Please enter a query!",justification="center")],
              [sg.Text("Query:"),sg.InputText()],
              [sg.Button("Send Query")],
              [sg.Text("Output:"), sg.Multiline(size=(50,10),key='-output-')]]
    
    window = sg.Window("Text Mode",layout,resizable=True)

    while True:
        events, values = window.read()
        if(events == "Send Query"):
            query = values[0]
            if(query == "sleep"):
                tts.say("Goodbye")
                window.close()
                login_window()
            else:
                output = main(query)
                window['-output-'].update(output)
                tts.say(output)
#                window.close()
#                textmode(output)
        if(events == sg.WIN_CLOSED):
            window.close()
            exit()

def textorvoice():
    layout = [[sg.Text("What mode do you want?", justification="center")],
              [sg.Button("Voice Mode")],
              [sg.Button("Go Back")]]
    
    

    window = sg.Window("Choose", layout,size=(715,207),keep_on_top=True)

    while True:
        events, values = window.read()
    
        if(events == 'Voice Mode'):
            print("Voice Selected")
            window.close()
            voicemode()
        if(events == 'Go Back'):
            window.close()
            login_window()
        if(events == sg.WIN_CLOSED):
            break

def sucess():
    sg.theme('Dark Amber')
    layout = [[sg.Text("Sucessfull!!", justification="center")],
              [sg.Button("Ok")]]

    window = sg.Window("Sucess", layout)

    while True:
        events, values = window.read()
        if(events == 'Ok'):
            window.close()
        if(events == sg.WIN_CLOSED):
            break

def error():
    layout = [[sg.Text("Something went wrong!", justification="center")],
              [sg.Button("Ok")]]

    window = sg.Window("Error", layout)

    while True:
        events, values = window.read()
        if(events == 'Ok'):
            window.close()
        if(events == sg.WIN_CLOSED):
            break


def login_window():
    login_layout = [ [sg.Text("Please Enter user details",justification='center')],
                    [sg.Text("Username : "), sg.InputText()],
                    [sg.Text("Password : "), sg.InputText(text_color='White',background_color='White')],
                    [sg.Button("Login")],
                    [sg.Button("Go Back")] ]
            
    loginpage = sg.Window("Login!",login_layout,auto_size_text=True, auto_size_buttons=True, resizable=True)

    while True:
        login_events, login_values = loginpage.read()
        if(login_events == "Login"):
            username = login_values[0]
            password = login_values[1]
            login = start.login(username,password)
            if(login==True):
                print("Log in successful")
                sucess()
                loginpage.close()
                textorvoice()
            else:
                error()
        if(login_events == "Go Back"):
            loginpage.close()
            main_window()
        if(login_events == sg.WIN_CLOSED):
            break

def register_window():
    register_layout = [ [sg.Text("Enter details to register",justification='center')],
                        [sg.Text('Enter Username'),sg.InputText()],
                        [sg.Text('Enter password'),sg.InputText()],
                        [sg.Button('Register')],
                        [sg.Button('Go Back')]]
    
    registerpage = sg.Window("Register",register_layout,auto_size_text=True, auto_size_buttons=True, resizable=True)

    while True:
        register_events, register_values = registerpage.read()
        if(register_events=='Register'):
            username = register_values[0]
            password = register_values[1]
            register = start.register(username,password)
            if(register==True):
                print("User has been registered")
                sucess()
            else:
                print(register)
        if(register_events=='Go Back'):
            registerpage.close()
            main_window()

def main_window():
  

    
    main_layout = [  [sg.Text(text="Welcome!!", justification='center')],
                   [sg.Image(filename='', key='-IMAGE-')],
                [sg.Button("Login",size=(10, 1))],
                [sg.Button("Register",size=(10, 1))],
                [sg.Button("Exit",size=(10, 1))]         ]

    startpage = sg.Window('Welcome',main_layout,finalize=True)

    image_filename = 'background.gif'  # Replace with your image file path
    startpage['-IMAGE-'].update(filename=image_filename)

    while True:
        events, values = startpage.read()
        if(events==sg.WIN_CLOSED or events == 'Exit'):
            exit()
        if(events == 'Login'):
            startpage.close()
            login_window()
        if(events == 'Register'):
            startpage.close()
            register_window()




      
main_window()