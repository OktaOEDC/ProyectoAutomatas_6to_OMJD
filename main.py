from cmath import exp
import PySimpleGUI as sg
from numpy import append, array
import Implementacion_GLC_a_AP.Main as GLC
import Implementacion_REGEX_a_AFI as RTA
sg.theme('BluePurple')


class useregex:
    def __init__(self):
        self.alphabet = []

    def input_symbol_to_alphabet(self, symbol):
        print(f'{symbol} was entered')
        self.alphabet.append(symbol)
        print(self.alphabet)

    def submit_regex(self):
        # la regla tiene que ser escrita de la siguiente forma: S->a|bc|D
        print('SEND REGEX TO JSON....')

    def get_regex(self):
        return str(self.alphabet)


class GLCtoAP:
    def __init__(self) -> None:
        self.expressions = []

    def tagExp(self, expression):
        self.expressions.append(expression)

    def main(self):
        GLC.separador(self.expressions)


class REGEXtoAFI:
    def __init__(self) -> None:
        self.idk = ''

    def main(self):
        RTA.main(self.idk)

    def addchain(self, regular_expression):
        self.idk(regular_expression)


user_regex = useregex()
ls_regex = user_regex.get_regex()


layout = [[sg.Text('---REGEX to AFI---')], [sg.Text('Type in a symbol:'), sg.Input(key='-INPUT REGEX-')],
          [sg.Text('Type in a RegEx:'), sg.Input(key='-INPUT SYMBOL-')],
          [sg.Button('Enter alphabet symbol'), sg.Button(
              'Show AFI'), sg.Button('Exit')],
          [sg.Text('PLACEHOLDER IMAGE')],
          [sg.Text('GLC to PA')],
          [sg.Text('Type Rule in form S->a|bc|D  :'),
           sg.Input(key='-INPUT RULE-')],
          [sg.Button('Add Rule'), sg.Button(
              'Show Automaton')],
          [sg.Image(r'./jack.jpg')]]

window = sg.Window('REGEX to AFI', layout)

while True:  # Event Loop
    user_expression = []
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show AFI':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(ls_regex)
    if event == 'Enter an alphabet symbol':
        user_regex.input_symbol_to_alphabet(values['-IN-'])
        window['-INPUT SYMBOL-'].update('')
    if event == 'Enter an alphabet symbol':
        pass
window.close()
