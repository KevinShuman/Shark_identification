

import os
from pathlib import Path
from PIL import Image, ImageOps
import PySimpleGUIQt as sg

MAIN_PATH = os.getcwd()
IMAGE_PATH = os.path.join(MAIN_PATH,"jesus2.png")

def exchange_and_get(list_on, list_off):
    element = list_off.pop()
    list_on.append(element)

    return element

def reshape_image(path, x_size, y_size, fill_color):
        im = Image.open(path)
        im = ImageOps.pad(im, (x_size, y_size), color=fill_color)
        im.save(path)


layout_left = [
                    [sg.Text(text="Here we go through the image files in a directory and choose which to store elsewhere")],
                    [sg.Text(text="Directory with image files")],
                    [sg.InputText(key="-Input_Dir-"), sg.FolderBrowse(initial_folder=MAIN_PATH)],
                    [sg.Text(text="Directory to place files")],
                    [sg.InputText(key="-Output_Dir-"), sg.FolderBrowse(initial_folder=MAIN_PATH)],
                    [sg.Button("Start", key="-Start-"), sg.Button("Next", key="-Next-"), sg.Button("Back", key="-Back-")],
                    [sg.Button("Save", key="-Save-")]

]

layout_right = [[sg.Image(IMAGE_PATH, key='-Image-')]]

layout_study = [
                    [sg.Column(layout_left),
                     sg.VerticalSeparator(),
                    sg.Column(layout_right)]
                    ]

window = sg.Window("The Window", layout_study, return_keyboard_events=True)

initialized = 0


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # closes window if user closes window of clicks "Next"
        break
    

    if event == "-Start-":
        initialized = 1
        for_back = 0
        image_files_in = []
        image_files_out = []
        keep_list = []

        input_path = values["-Input_Dir-"]
        output_path = values["-Output_Dir-"]
    
        image_files_in = os.listdir(input_path)
        top_image = exchange_and_get(image_files_out, image_files_in)
        full_path = os.path.join(input_path, top_image)

        window['-Image-'].update(filename=full_path)

    elif event == "-Next-" and initialized == 1:
        if for_back == 1:
            try:
                top_image = exchange_and_get(image_files_out,image_files_in)
                top_image = exchange_and_get(image_files_out,image_files_in)
            except:
                print("No images that way!")
        else:
            try:
                top_image = exchange_and_get(image_files_out,image_files_in)
            except:
                print("No images that way!")

        for_back = 0
        full_path = os.path.join(input_path, top_image)
        keep_list.append(full_path)
        reshape_image(full_path,500,500,"black")
        window['-Image-'].update(filename=full_path)
    elif event == "d" and initialized == 1:
        window['-Next-'].click()

    elif event == "-Back-" and initialized == 1:
        if for_back == 0:
            try:
                top_image = exchange_and_get(image_files_in,image_files_out)
                top_image = exchange_and_get(image_files_in,image_files_out)
            except:
                print("No images that way!")
        else:
            try:
                top_image = exchange_and_get(image_files_in,image_files_out)
            except:
                print("No images that way!")

        for_back = 1
        full_path = os.path.join(input_path, top_image)
        try:
            keep_list.pop()
        except:
            print("Keep list is empty!")
        reshape_image(full_path,500,500,"black")
        window['-Image-'].update(filename=full_path)
    elif event == "a" and initialized == 1:
        window['-Back-'].click()

    if event == "-Save-" and initialized == 1:
        print(keep_list)




window.close()