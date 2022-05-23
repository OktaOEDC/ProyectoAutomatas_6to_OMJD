
import PySimpleGUI as sg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import Implementacion_GLC_a_AP.Main as GLC
import Implementacion_REGEX_a_AFI.Main as RTA
import Implementacion_REGEX_a_AFI.Fragmenter
import Implementacion_REGEX_a_AFI.AutomataMaker
import os
import Implementacion_REGEX_a_AFI.Preparer as Preparer

sg.theme('BluePurple')


class useregex:
    def __init__(self):
        self. result = ''

    def main(chain):
        return RTA.main(chain)


class GLCtoAP:
    def __init__(self):
        self.expressions = []
        self.readable = ''
    def tagExp(self, expression):
        self.expressions.append(expression)
        self.readable+= expression+"\n"
    def getReadable(self):
        return self.readable
    def main(self):
        GLC.separador(self.expressions)

    def getExp(self):
        return self.expressions


layout = [[sg.Text('---REGEX to AFI CONVERTER---')],
          [sg.Text('Type in a RegEx:'), sg.Input(key='CHAIN')],
          [sg.Button(
              'Show resulting AFI'), sg.Button('Exit')],
          [sg.Image(key='AFI')],
          [sg.Text('GLC to PA')],
          [sg.Text('Type Rule in form S->a|bc|D  :'),
           sg.Input(key='INPUTRULE')],
          [sg.Text(key='RULES')],
          [sg.Button('Add Rule'), sg.Button(
              'Show Automaton')],
          [sg.Image(key='AP')]]
userGLC = GLCtoAP()

window = sg.Window('REGEX to AFI', layout)

while True:  # Event Loop
    user_expression = []
    user_input_regex = useregex
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show resulting AFI':
        image_path = user_input_regex.main(values['CHAIN'])
        drawing = svg2rlg(image_path)
        renderPM.drawToFile(drawing, "file.png", fmt="PNG")
        print(values['CHAIN'][0])
        window['AFI'].update(filename="file.png")
        # Update the "output" text element to be the value of "input" element
    if event == 'Add Rule':
        userGLC.tagExp(values['INPUTRULE'])
        
        window['RULES'].update(userGLC.getReadable())
    if event =='Show Automaton': 
        
        userGLC.main()
        window['AP'].update(filename = 'Implementacion_GLC_a_AP/AP_texto.png')

window.close()
