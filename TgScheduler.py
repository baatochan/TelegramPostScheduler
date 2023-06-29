import PySimpleGUIQt as sg

layout = [
    [sg.Text(
        text="Hello, World!",
        font=("Arial Bold", 30),
        justification="center")]
]

window = sg.Window("Hello World", layout, size=(400, 200))

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

window.close()
