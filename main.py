
import PySimpleGUI as sg
pip install svglib

import Implementacion_GLC_a_AP.Main as GLC
import Implementacion_REGEX_a_AFI.Main as RTA
import Implementacion_REGEX_a_AFI.Fragmenter
import Implementacion_REGEX_a_AFI.AutomataMaker
import Implementacion_REGEX_a_AFI.Preparer as Preparer

sg.theme('BluePurple')


class useregex:
    def __init__(self, userchain):
        self. result = ''
    def main():
        return RTA.main(userchain)


class GLCtoAP:
    def __init__(self) -> None:
        self.expressions = []

    def tagExp(self, expression):
        self.expressions.append(expression)

    def main(self):
        GLC.separador(self.expressions)
        print('made image')




#user_glc = GLCtoAP()

layout = [[sg.Text('---REGEX to AFI CONVERTER---')],
          [sg.Text('Type in a RegEx:'), sg.Input(key='CHAIN')],
          [sg.Button(
              'Show resulting AFI'), sg.Button('Exit')],
          [sg.Image(key='AFI')],
          [sg.Text('GLC to PA')],
          [sg.Text('Type Rule in form S->a|bc|D  :'),
           sg.Input(key='-INPUT RULE-')],
          [sg.Button('Add Rule'), sg.Button(
              'Show Automaton')],
          [sg.Image()]]

window = sg.Window('REGEX to AFI', layout)

while True:  # Event Loop
    user_expression = []
    userGLC = GLCtoAP
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show resulting AFI':
        print(values['CHAIN'][0])
        image_path = useregex(values['CHAIN'])
        window['AFI'].update(filename=image_path)
        # Update the "output" text element to be the value of "input" element
    if event == 'Enter an alphabet symbol':
        pass
window.close()
