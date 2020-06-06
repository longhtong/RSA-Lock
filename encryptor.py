import PySimpleGUI as sg
import rsa as rsa
def main():
    sg.theme('Dark Blue 3')  # please make your windows colorful

    layout = [[sg.Button('Encrypt'), 
                sg.Button('Decrypt')],
                [sg.Button('New User')]]

    window = sg.Window('RSA Encryptor', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Encrypt':
            # change the "output" element to be the value of "input" element
            print("Encryption")
            encryptStartingWindow()
        elif event == 'New User':
            newUserWindow()
        elif event == 'Decrypt':
            decryptStartingWindow()
    window.close()

def encryptStartingWindow():
    sg.theme('Dark Blue 3')
    layout = [  [sg.Text(text = "Please Enter Public Keys")],
                [sg.Text(text = "RSA Key: "), sg.Input(key = "-N-")],
                [sg.Text(text = "Secondary Key: "), sg.Input(key = "-e-")],
                [sg.Button('Submit')]]

    window = sg.Window('RSA Encryptor', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Submit':
            #save the info
            #open another window for encryption
            N = values["-N-"]
            e = values["-e-"]
            # print(N, "RSA  \n")
            # print(e,"e \n")
            window.close()
            encryptWindow(int(N), int(e))
            
def decryptStartingWindow():
    sg.theme('Dark Blue 3')
    layout = [  [sg.Text(text = "Please Enter Public Keys")],
                [sg.Text(text = "RSA Key: "), sg.Multiline(key = "-N-")],
                [sg.Text(text = "Secondary Key: "), sg.Multiline(key = "-e-")],
                [sg.Text(text = "Private Key: "), sg.Multiline(key = "-d-")],
                [sg.Button('Submit')]]

    window = sg.Window('RSA Encryptor', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Submit':
            #save the info
            #open another window for encryption
            N = values["-N-"]
            d = values["-d-"]
            window.close()
            decryptWindow(int(N), int(values["-e-"]), int(d))
            
        
#Provide 3 keys to user. Options to proceed to encryption or decryption       
def newUserWindow():
    rsaNew = rsa.RSAObj.newUser()
    sg.theme('Dark Blue 3')
    layout =    [[sg.Text(text = "RSA Key: ")],
                [sg.MLine(str(rsaNew.getN()))],
                [sg.Text(text = "Secondary Key: ")],
                [sg.MLine(str(rsaNew.getE()))],
                [sg.Text(text = "Private Key: ")],
                [sg.MLine(str(rsaNew.getD()))],
                [sg.B("Proceed to Encryption"), sg.B("Proceed to Decryption")]]
    window = sg.Window('RSA Encryptor', layout)
    event, values = window.read()
    nextAction = None

    if event == "Proceed to Encryption":
        nextAction = encryptWindow
    elif event == "Proceed to Decryption":
        nextAction = decryptWindow
    else:
        window.close()

    layout1 = [[sg.Text("Would you like to use your newly generated keys?")],
                [sg.B("Yes"), sg.B("No")]]
    window1 = sg.Window('RSA Encryptor', layout1)
    event, values = window1.read()
    if event == "Yes":
        window.close() 
        window1.close()         
        nextAction(rsaNew.getN(), rsaNew.getE(), rsaNew.getD())
        print("YES and window and popup closed")
    elif event == "No":
        window.close() 
        window1.close() 
        encryptStartingWindow()
        #nextAction()
        print("NO and window and popup closed")
    elif event == sg.WIN_CLOSED or event == 'Exit':
        window.close() 
        window1.close() 
    
    
def encryptWindow(N = None, e = None, dummy = None):
    sg.theme('Dark Blue 3')

    layout = [[sg.T("Encrypt a Message")],
                [sg.Multiline(key = "-MessIn-")],
                [sg.B("Encrypt Message")],
                [sg.T("Encrypt a File")],
                [sg.In(key = "-FileName-"), sg.FileBrowse()],
                [sg.B("Encrypt File")]]
    window = sg.Window('RSA Encryptor', layout)
    rsaEncrypt = rsa.RSAObj(N = N, e = e, d = dummy)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break
        if event == "Encrypt Message":
            rsaEncrypt.getMessage(values["-MessIn-"])
            encryptedMess = rsaEncrypt.encrypteMess()
            layoutMess = [[sg.Multiline(default_text= encryptedMess)]]
            sg.Window('RSA Encryptor', layoutMess).read(close = True)
            
            

        elif event == "Encrypt File":
            print("Encrypte FIle: \n")
            print(values["-FileName-"])
def decryptWindow(N = None, e = None, d = None):
    sg.theme('Dark Blue 3')

    layout = [[sg.T("Decrypt a Message")],
                [sg.Multiline(key = "-MessIn-")],
                [sg.B("Decrypt Message")],
                [sg.T("Decrypt a File")],
                [sg.In(key = "-FileName-"), sg.FileBrowse()],
                [sg.B("Decrypt File")]]
    window = sg.Window('RSA Encryptor', layout)
    rsaDecrypt = rsa.RSAObj(N = N, e = e, d = d)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break
        if event == "Decrypt Message":
            rsaDecrypt.getMessage(values["-MessIn-"])
            decryptedMess = rsaDecrypt.decrypteMess()
            layoutMess = [[sg.Multiline(default_text= decryptedMess)]]
            sg.Window('RSA Encryptor', layoutMess).read(close = True)

        elif event == "Decrypt File":
            print("Decrypt FIle: \n")
            print(values["-FileName-"])


main()