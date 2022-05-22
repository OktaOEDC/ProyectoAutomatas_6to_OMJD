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
        self.readable_rules = ''
        self.readable_pushdown_automaton = ''

    def tagExp(self, expression):
        self.expressions.append(expression)
        self.readable_rules += expression+'\n'
        print(self.expressions)

    def get_readable(self):
        return self.readable_rules

    def clear_rules(self):
        self.expressions = []
        self.readable_rules = ''

    def translate_to_pushdown_automaton(self):
        self.pushdown_automaton = GLC.separador(self.expressions)
        for q in self.pushdown_automaton:
            self.readable_pushdown_automaton += q+'\n'

    def get_pushdown_automaton(self):
        return self.readable_pushdown_automaton


class REGEXtoAFI:
    def __init__(self) -> None:
        self.idk = ''

    def main(self):
        RTA.main(self.idk)

    def addchain(self, regular_expression):
        self.idk(regular_expression)


user_regex = useregex()
ls_regex = user_regex.get_regex()
userGLC = GLCtoAP()

layout = [[sg.Text('---REGEX to AFI---')],
          [sg.Text('Type in a symbol:'), sg.Input(key='-INPUT REGEX-')],
          [sg.Text('Type in a RegEx:'), sg.Input(key='-INPUT SYMBOL-')],
          [sg.Button('Enter alphabet symbol'), sg.Button(
              'Show AFI'), sg.Button('Exit')],
          [sg.Text('PLACEHOLDER IMAGE')],
          [sg.Text('GLC to PA')],
          [sg.Text('Type Rule in form S->a|bc|D  :'),
           sg.Input(key='-INPUT-RULE-')],
          [sg.Text(key='-RULES-')],
          [sg.Button('Add Rule'), sg.Button(
              'Show Automaton'), sg.Button(
              'Clear Rules')], [sg.Text( key='-PA-')],
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
    if event == 'Add Rule':
        userGLC.tagExp(values['-INPUT-RULE-'])
        window['-RULES-'].update(userGLC.get_readable())
    if event == 'Clear Rules':
        userGLC.clear_rules()
        window['-RULES-'].update(userGLC.get_readable())

    if event == 'Show Automaton':
        userGLC.translate_to_pushdown_automaton()
        window['-PA-'].update(userGLC.get_pushdown_automaton())


window.close()
