import PySimpleGUI as sg
from numpy import append, array

sg.theme('BluePurple')


class useregex:
    def __init__(self):
        self.alphabet = []

    def input_symbol_to_alphabet(self, symbol):
        print(f'{symbol} was entered')
        self.alphabet.append(symbol)
        print(self.alphabet)

    def submit_regex(self):
        print('SEND REGEX TO JSON....')
    def get_regex(self):
        return str(self.alphabet)


user_regex = useregex()
ls_regex = user_regex.get_regex()


layout = [[sg.Text('Type in a symbol:'), sg.Input(key='-INPUT REGEX-')],
          [sg.Text('Type in a RegEx:'), sg.Input(key='-INPUT SYMBOL-')],
          [sg.Button('Enter alphabet symbol'), sg.Button('Show AFI'), sg.Button('Exit')],
          [sg.Text('PLACEHOLDER IMAGE')],
          [sg.Image(r'C:\Users\julio\Desktop\PROJECTS\AUTOMATAS\ProyectoAutomatas_6to_OMJD\app\jack.jpg')]]

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
