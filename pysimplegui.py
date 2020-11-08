import PySimpleGUI as sg

sg.theme('LightBrown3')  

layout = [[sg.Text('Püsiv aken vol2', text_color='blue', font=("Helvetica", 15))],
    [sg.Text('Lisa raamat: ', size=(15, 1)), sg.InputText()],
    [sg.Text('Loetud/lugemata/pooleli:  ', size=(15, 1)), sg.InputText()],
    [sg.Submit("Lisa nimistusse"), sg.Cancel("Sulge aken")]]

window = sg.Window('Püsiv aken vol2', layout)

while True:
    event, values = window.read()
    #kui aken pannakse kinni, lõpetab programm töö
    if event == sg.WIN_CLOSED or event == 'Sulge aken':
        break
    #kui vajutatakse nuppu 'LOE!', pannakse põhiaken kinni ja avaneb uus aken
    if event == "Lisa nimistusse":
        window.close()
    input1, input2 = values[0], values[1]
    sg.Popup('Lisatud raamat: ',
                input1, input2)
     
window.close()

event, values = window.read()
window.close()


input1, input2 = values[0], values[1]
print(input1, input2)
