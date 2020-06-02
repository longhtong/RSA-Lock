import PySimpleGUI as sg

def main():
    sg.theme('Dark Blue 3')  # please make your windows colorful

    layout = [[sg.Button('Encrypt'), sg.Button('Decrypt')]]

    window = sg.Window('RSA Encryptor', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Encrypt':
            # change the "output" element to be the value of "input" element
            layout1 = [[sg.Button('New1'), sg.Button('New2')]]
            window = sg.Window('RSA Encryptor', layout1)

    window.close()
def encryptWindow():
    pass
def decryptWindow():
    pass
main()