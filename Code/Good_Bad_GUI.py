import os
from pathlib import Path
from PIL import Image, ImageOps
import PySimpleGUIQt as sg

MAIN_PATH = os.getcwd()
IMAGE_PATH = os.path.join(MAIN_PATH,"jesus2.png")

def exchange(list_on, list_off):
    element = list_off.pop()
    list_on.append(element)

def get_top(list1):
    element = list1.pop()
    list1.append(element)

    return element

def get_next(list1):
    element1 = list1.pop()
    element2 = list1.pop()
    list1.append(element2)
    list1.append(element1)

    return element2

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
                    [sg.Button("Start", key="-Start-"), sg.Button("Next", key="-Next-"), sg.Button("Reject", key="-Reject-")],
                    [sg.Button("Back", key="-Back-")],
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
    
    # I want to populate a stack with all the image paths I want to keep
    # and at the same time I want to move onto the next photo in the 
    # directory. I want to do this by either pressing the Next button or
    # by pressing the d key
    elif event == "-Next-" and initialized == 1:
        print(top_image)
        for_back = 0
        keep_list.append(full_path)

        try:
            next_image = get_next(image_files_in)
            full_path = os.path.join(input_path, next_image)
            reshape_image(full_path,500,500,"black")
            window['-Image-'].update(filename=full_path)
            exchange(image_files_out,image_files_in)
        except:
            print("No images that way!")

        '''if for_back == 1:
            try:
                exchange(image_files_out,image_files_in)
                exchange(image_files_out,image_files_in)
            except:
                print("No images that way!")
        else:
            try:
                exchange(image_files_out,image_files_in)
            except:
                print("No images that way!")'''
    elif event == "d" and initialized == 1:
        window['-Next-'].click()

    # If I come across a photo that I don't want to keep, I want to
    # just move onto the next photo without adding it to the stack.
    # I do this by pressing the w key
    elif event == "-Reject-" and initialized == 1:
        print(top_image)
        for_back = 0

        try:
            next_image = get_next(image_files_in)
            full_path = os.path.join(input_path, next_image)
            reshape_image(full_path,500,500,"black")
            window['-Image-'].update(filename=full_path)
            exchange(image_files_out,image_files_in)
        except:
            print("No images that way!")

        '''if for_back == 1:
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

        print(top_image, "skipped")

        for_back = 0
        full_path = os.path.join(input_path, top_image)
        reshape_image(full_path,500,500,"black")
        window['-Image-'].update(filename=full_path)'''
    elif event == "w" and initialized == 1:
        window['-Reject-'].click()

    # If I make a mistake, I want to be able to go back to the previous
    # image and also remove it from the stack. I want to do this by
    # pressing the a key
    elif event == "-Back-" and initialized == 1:
        print(top_image)
        for_back = 0

        try:
            top_image = get_top(image_files_out)
            full_path = os.path.join(input_path, top_image)

            if full_path in keep_list:
                keep_list.pop()

            reshape_image(full_path,500,500,"black")
            window['-Image-'].update(filename=full_path)
            exchange(image_files_in,image_files_out)
        except:
            print("No images that way!")
    elif event == "a" and initialized == 1:
        window['-Back-'].click()

    # Once I have made it through all the photos in my directory, I want
    # to save the stack of all the image paths I plan to keep. I do that 
    # by pressing the Save button
    if event == "-Save-" and initialized == 1:
        with open(os.path.join(output_path,"keep_images.txt"), 'w') as fp:
            fp.write('\n'.join(keep_list))

    # We start with initialized everything, bringing up the first image
    # A being able to decide on the first image. Once the decision
    # has been made, it brings up the next image
    elif event == "-Start-" and initialized == 0:
        for_back = 0
        image_files_in = []
        image_files_out = []
        keep_list = []

        input_path = values["-Input_Dir-"]
        output_path = values["-Output_Dir-"]
    
        image_files_in = os.listdir(input_path)
        top_image = get_top(image_files_in)
        full_path = os.path.join(input_path, top_image)
        print(top_image)
        window['-Image-'].update(filename=full_path)
    elif event == "d" and initialized == 0:
        keep_list.append(full_path)
        initialized = 1

        next_image = get_next(image_files_in)
        full_path = os.path.join(input_path, next_image)
        
        reshape_image(full_path,500,500,"black")
        window['-Image-'].update(filename=full_path)
        exchange(image_files_out,image_files_in)
    elif event == "w" and initialized == 0:
        initialized = 1

        next_image = get_next(image_files_in)
        full_path = os.path.join(input_path, next_image)
        
        reshape_image(full_path,500,500,"black")
        window['-Image-'].update(filename=full_path)
        exchange(image_files_out,image_files_in)
    elif event == "a" and initialized == 0:
        print("No images that way!")


    print("This is keep ", keep_list)
    print("This is out", image_files_out)


window.close()