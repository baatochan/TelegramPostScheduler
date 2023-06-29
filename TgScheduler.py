import PySimpleGUI as sg
import io
import PIL.Image
import base64
from datetime import datetime

def preserve_size(im, expected_size=(256, 256), fill_color=(0, 0, 0, 0)):
    x, y = im.size
    new_im = PIL.Image.new('RGBA', expected_size, fill_color)
    new_im.paste(im, (int((expected_size[0] - x) / 2), int((expected_size[1] - y) / 2)))
    return new_im

def convert_to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.LANCZOS)
        img = preserve_size(img, resize)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

ImageFileTypes = (("Image Files", "*.png *.gif *.bmp *.jpg *.jpeg"),)

leftColumn = [
    [sg.Image(filename="img/no-image.png", key="ImagePreview", size=(400, 300))],
    [
        sg.Text("Path: ", font="any 12"),
        sg.InputText(default_text="Enter path or select file...", key="FilePath", enable_events=True, size=(37, 1)),
        sg.FileBrowse(size=(8,1), file_types=ImageFileTypes)
    ],
    [sg.Text("Sites to mention", font="any 16 bold", justification="center", size=(30, 1))],
    [
        sg.Checkbox(text="🐦 Twitter", font=("Segoe UI Emoji", 12)),
        sg.InputText(size=(41,1))
    ],
    [
        sg.Checkbox(text="🎨 dA", font=("Segoe UI Emoji", 12)),
        sg.InputText(size=(45,1))
    ],
    [
        sg.Checkbox(text="Custom 1", font=("Segoe UI Emoji", 12)),
        sg.InputText(size=(10,1)),
        sg.InputText(size=(30,1))
    ],
    [
        sg.Checkbox(text="Custom 2", font=("Segoe UI Emoji", 12)),
        sg.InputText(size=(10,1)),
        sg.InputText(size=(30,1))
    ],
    [
        sg.Checkbox(text="Custom 3", font=("Segoe UI Emoji", 12)),
        sg.InputText(size=(10,1)),
        sg.InputText(size=(30,1))
    ],
    [sg.Text("Post on:", font="any 16 bold", justification="center", size=(30, 1))],
    [
        sg.InputText(default_text=datetime.today().strftime('%Y-%m-%d'), size=(10, 1)),
        sg.InputText(default_text=datetime.today().strftime('%H:%M'), size=(10, 1)),
    ],
]

middleColumn = [
    [sg.Text("TAGS:", font="any 20 bold", justification="center", size=(23, 1))],
    [sg.Text("Custom tags:"), sg.InputText(size=(42,1))],
    [sg.Text("Common ones", font="any 16 bold", justification="center", size=(30, 1))],
    [
        sg.Checkbox(text="Tag 1", font="any 12"),
        sg.Checkbox(text="Tag 2", font="any 12"),
        sg.Checkbox(text="Tag 3", font="any 12"),
        sg.Checkbox(text="Tag 4", font="any 12"),
    ],
    [
        sg.Checkbox(text="Tag 5", font="any 12"),
        sg.Checkbox(text="Tag 6", font="any 12"),
        sg.Checkbox(text="Tag 7", font="any 12"),
        sg.Checkbox(text="Tag 8", font="any 12"),
    ],
    [
        sg.Checkbox(text="Tag 9", font="any 12"),
        sg.Checkbox(text="Tag 10", font="any 12"),
    ],
    [sg.Text("Selected tags:", font="any 16 bold", justification="center", size=(30, 1))],
    [sg.Multiline(size=(53,5))],
    [sg.Text("Description:", font="any 16 bold", justification="center", size=(30, 1))],
    [sg.Multiline(size=(53,15))],
]

rightColumn = []

layout = [
    [
        sg.Column(leftColumn),
        sg.VSeparator(),
        sg.Column(middleColumn),
        sg.VSeparator(),
        sg.Column(rightColumn)
    ]
]

window = sg.Window("Telegram Post Scheduler", layout, size=(1200, 800), resizable=True)

while True:
    event, values = window.read()

    if event == "FilePath":
        path = values["FilePath"]
        try:
            window["ImagePreview"].update(convert_to_bytes(path, (400, 300)))
        except:
            pass

    if event == sg.WINDOW_CLOSED:
        break

window.close()
