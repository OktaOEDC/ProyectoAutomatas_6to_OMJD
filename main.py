from pickle import TRUE
import PySimpleGUI as sg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import Implementacion_GLC_a_AP.Main as GLC
import Implementacion_REGEX_a_AFI.Main as RTA
import Implementacion_REGEX_a_AFI.Fragmenter
import Implementacion_REGEX_a_AFI.AutomataMaker
import Implementacion_REGEX_a_AFI.Preparer as Preparer
import cairosvg

sg.theme('BluePurple')


def regexfunc(chain):
    return RTA.main(chain)


class GLCtoAP:
    def __init__(self):
        self.expressions = []
        self.readable = ''

    def tagExp(self, expression):
        self.expressions.append(expression)
        self.readable += expression+"\n"
    def clearExps(self):
        self.expressions=[]
        self.readable=''

    def getReadable(self):
        return self.readable

    def main(self):
        GLC.separador(self.expressions)

    def getExp(self):
        return self.expressions


import os
import os 
    
# path 
paths =['./images', './AFI']
    
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents' 
try: 
    for path in paths:
        os.mkdir(path)
except OSError as error: 
    print(error)  

image_layout = [[sg.Text('---REGEX to AFI CONVERTER---')],
                [sg.Text('Type in a RegEx:', key='regex-info'), sg.Input(key='CHAIN')],
                [sg.Button(
                    'Show resulting AFI'),sg.Button('Clear Regex'), sg.Button('Exit')], [sg.Image(key='AFI')]]
for i in range(200):
    ls = [sg.Text(' ')]
    image_layout.append(ls)
    
glc_layout = [[sg.Text('GLC to PA')],
              [sg.Text('Type Rule in form S->a|bc|D  :', key='inst'),
              sg.Input(key='INPUTRULE')],
              [sg.Text(key='RULES')],
              [sg.Button('Add Rule'), sg.Button(
                  'Show Automaton'), sg.Button('Clear Rules')],
              [sg.Image(key='AP')]]
layout = [
    [sg.Column(image_layout, key='column', scrollable=True,
               vertical_scroll_only=False, expand_x=True, expand_y=True, s=(600, 900)),
     sg.Column(glc_layout, key='glc_column', scrollable=True, vertical_scroll_only=False, expand_x=True, expand_y=True, vertical_alignment='top', grab=True)]
]
userGLC = GLCtoAP()


window = sg.Window('Automatas', layout)

while True:  # Event Loop
    user_expression = []
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show resulting AFI':
        try:
            afi_path = regexfunc(values['CHAIN'])
            cairosvg.svg2png(url='./AFI/AFI.dot.svg', write_to="./images/afi.png",
                            output_width=600, output_height=None)
            print(values['CHAIN'][0])
            window['AFI'].update(filename="./images/afi.png")
        except:
            window['regex-info'].update('Type in a FUNCTIONING regex: ')
        # Update the "output" text element to be the value of "input" element
    if event =='Clear Regex':
        try:
            window['AFI'].update(filename=None)
            pass
        except:
            pass    
    if event == 'Clear Rules':
        try:
            userGLC.clearExps()
            print('Cleared Rules')
            window['RULES'].update(' ')
            window['inst'].update('Type a Rule in the form S->a|bc|D: ')
        except: 
            pass
    if event == 'Add Rule':
                
        try:
            userGLC.tagExp(values['INPUTRULE'])
            window['RULES'].update(userGLC.getReadable())
        except:
            window['RULES'].update(userGLC.getReadable()+'NOT A VALID RULE\n')

    if event == 'Show Automaton':

        try:
            userGLC.main()
            window['AP'].update(filename='./images/AP_texto.png')
        except:
            window['inst'].update('Type a VALID Rule in the form S->a|bc|D  again: ')
window.close()
