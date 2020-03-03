from pynput.keyboard import Key, Listener, Controller
import time
import re
import os
import subprocess
import pygetwindow as gw


key_press_limit = 2.0 # seconds

SLO_language = {'sheet':'note', 'lyrics':'besedilo', 'library':'knjiznica'}

dict_language = SLO_language

apps_to_kill = ['wordpad.exe', 'AcroRd32.exe'] # apps used for opening files

# ----------------------------------------------------

keyboard = Controller()
start_dir = os.getcwd()
MMT_tool_path = start_dir

path_library = os.path.join(start_dir, dict_language['library'])
os.chdir(path_library)

print('\nStart path: ', os.getcwd())

keys = []
times = []
time_last = time.time()

number_strings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def kill_previous():
    for app in apps_to_kill:

        try:
            process = subprocess.Popen(['taskkill', '/F', '/IM', app],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        shell=False)

            stdout, stderr = process.communicate()
        except:
            pass

def open_files(string):

    print('Opening files with string {}.'.format(string))

    try:

        filename_notes = [f for f in os.listdir() if (dict_language['sheet'] in f and f.split(' ')[-1].split('.')[0]==string)][0]
        filename_lyrics = [f for f in os.listdir() if (dict_language['lyrics'] in f and f.split(' ')[-1].split('.')[0]==string)][0]

        # kill previous processes
        kill_previous()

    except IndexError:
        
        print('Files with string {} not found.'.format(string))

        return None

    print('Filename_notes:', filename_notes)
    print('Filename_lyrics:', filename_lyrics)

    for filename in [filename_notes, filename_lyrics]:

        path_filename = os.path.join(os.getcwd(), filename)
        os.startfile(path_filename)

        filetype = filename.split(' ')[-1].split('.')[1]

#        print(path_filename, filetype)
    
        if filetype != 'pdf':
            filename = filename.split('.')[0] # remove file extension

        # --- maximize and activate window ---

        time.sleep(2)

        app_window = gw.getWindowsWithTitle(filename)[0]
    
        try:

            if app_window.isMaximized==False:
                app_window.maximize()

            app_window.activate()

        except:
            pass
    
    time.sleep(0.3)

    # --- move lyrics window to second display ---
    os.chdir(MMT_tool_path)

    process = subprocess.Popen(['MultiMonitorTool.exe', '/MoveWindow', '2', 'Title', dict_language['lyrics']],
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                shell=False)

    stdout, stderr = process.communicate()

    os.chdir(path_library) # go back to library of files

    return None


def on_press(key):

    global keys
    global time_last

    time_diff = time.time()-time_last

    print('\nKey pressed: ', key)

    if key == Key.esc:
        # Stop listener
        return False
        
    # --- if enter is pressed open files with key buffer in filename---
    if time_diff <  key_press_limit and key == Key.enter and len(keys) > 0:

        try:
            string = ''.join([key_i.char for key_i in keys])

            open_files(string)

        except AttributeError:
            pass

        keys = []

    # --- if requirements are met add key to key buffer ---
    try:
        if key.char in number_strings:

            if time_diff <  key_press_limit:
                keys.append(key)

            else:
                keys = [key]

        # --- clear buffer ---
        else:
            keys = []
    
    except AttributeError:
        pass
    
    print('Keys in buffer: {}.'.format(keys))

    time_last = time.time()

    CMD_title = ''.join([key_i.char for key_i in keys])
    os.system("TITLE " + CMD_title)

    return None


with Listener(on_press=on_press) as listener:
    listener.join()
