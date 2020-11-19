#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from psychopy.visual import Window, TextStim
from psychopy.core import wait, Clock, quit
from psychopy.event import clearEvents, waitKeys, Mouse
from psychopy.gui import Dlg
from time import gmtime, strftime
from codecs import open
from random import shuffle, choice, randint
from copy import deepcopy
from psychopy.iohub import launchHubServer
from numpy import mean, std
from datetime import datetime
from itertools import permutations
import random
## for testing
testing = True # True for testing, False for real recording
###
main_ddline = 1 # sec
isi_min_max = (500, 800)
instruction_color = '#9999FF'
############ MAIN ITEMS - paste from JS


probe_crime_text_1 = "Gebe dich als Person mit dem Namen Tim Koch aus und sende eine Nachricht an die Person mit dem Decknamen 'Blaue Jacke'.\nIn dieser Nachricht schreibst du 'Blaue Jacke' es gehe um die Operation Kuh und du bittest darum, die Regen Akte mit den U-Boot Plänen zur Hai Straße zu bringen.\n\n Leertaste drücken um fortzufahren.\n Im Folgenden werden die Details dieser Anordnung abgefragt."
probe_crime_text_2 = "Gebe dich als Person mit dem Namen Paul Nowak aus und sende eine Nachricht an die Person mit dem Decknamen 'Weißes Shirt'.\nIn dieser Nachricht schreibst du 'Weißes Shirt' es gehe um die Operation Fichte und du bittest darum, die Eulen Akte mit den Messing Plänen zur Löwen Straße zu bringen.\n\n Leertaste drücken um fortzufahren.\n Im Folgenden werden die Details dieser Anordnung abgefragt."
probe_crime_list_1 = ' Username : Tim Koch\n\n Deckname : Blaue Jacke\n\n Operation : Operation Kuh\n\n Akte : Regen Akte\n\n Pläne : U Boot Pläne\n\n Ort : Hai Strasse'
probe_crime_list_2 = ' Username : Paul Nowak\n\n Deckname : Weißes Shirt\n\n Operation : Operation Fichte\n\n Akte : Eulen Akte\n\n Pläne : Messing Pläne\n\n Ort : Löwen Strasse'

crime_list_1 = ["Tim Koch", "Blaue Jacke", "Operation Kuh",  "Regen Akte", "U-Boot Pläne", "Hai-Straße"]
crime_list_2 = ["Paul Nowak", "Weißes Shirt","Operation Fichte","Eulen Akte","Messing Pläne","Löwen Strasse"]
dummy_list_numbers = [0, 1, 2, 3, 4, 5]

training_recall_item = {0 : 'Username', 1 : 'Deckname', 2 : 'Operation', 3 : 'Akte', 4 : 'Pläne', 5 : 'Ort'}




if testing:
    escape_key = 'escape'
    instr_wait = 0.1
else:
    escape_key = 'notallowed'
    instr_wait = 0.5

# EXECUTE all main functions here
def execute():
    start_input() # prompt to input stuff
    # now initiate stuff
    set_screen() # creates psychopy screen and stim objects
    # window opens
    create_file() # created output file
    training_instruction()
    training_software()
    training_list()
    training_software()
    training_list()
    training_software()
    final_slide()
    win.mouseVisible = False # hide mouse


    print("************** END OF LEARNING TASK **************")

    ending() # saves demographic & final infos, gives feedback

    waitKeys(keyList = ['b']) # press B to end the exp (prevents subject from closing window)
    quit



def crime_text():
    show_instruction(probe_crime_text)

def training_instruction():
    global condition
    if condition % 2 != 0:
        probe_crime_text = probe_crime_text_1
        probe_crime_list = probe_crime_list_1
    else:
        probe_crime_text = probe_crime_text_2
        probe_crime_list = probe_crime_list_2# do it three times, no matter if correct answers, randomly assigned which probe set
    show_instruction('Lesen Sie den folgenden Text mehrmals aufmerksam durch. Sie werden im Folgenden zu den Details aus dem Text gefragt.\n\n' + probe_crime_text)
    show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Items gründlich auswendig gelernt haben.\n\n' + probe_crime_list)

def training_list():
    global condition
    if condition % 2 != 0:
        probe_crime_list = probe_crime_list_1
    else:
        probe_crime_list = probe_crime_list_2
    show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Items gründlich auswendig gelernt haben.\n\n' + probe_crime_list)

def training_software():
    global condition, required, typedin
    required_items = []
    if condition % 2 != 0:
        required_items = crime_list_1
    else:
        required_items = crime_list_2
    combine_shuffle = list(zip(required_items, dummy_list_numbers))
    shuffle(combine_shuffle)
    required_items[:], dummy_list_numbers[:] = zip(*combine_shuffle)
    counter = 0
    while counter <= 5:
        required = required_items[counter]
        cue = training_recall_item[dummy_list_numbers[counter]]
        counter += 1
        instr_display =  TextStim(win, color=instruction_color, font='Verdana', text = u'Bitte geben Sie im Folgenden die korrekte Antwort ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Verdana', text = 'Geben Sie ' + cue + ' ein:', pos=(-100, 0), alignHoriz = 'right', height=35)
        input_display =  TextStim(win, color='white', pos=(-100, -4), alignHoriz = 'left', height=35, bold = True, colorSpace='rgb')
        typedin = ''
        while True:
            input_display.setText(typedin)
            instr_display.draw()
            input_prompt.draw()
            input_display.draw()
            win.flip()
            char = waitKeys()[0]
            if char == 'backspace' and len(typedin) > 0:
                typedin = typedin[:-1]
            elif char == escape_key:
                break
            elif char == 'return':
                if len( trm(typedin) ) > 0:
                    break
            elif len(char) == 1 and char.isalpha():
                typedin += char.upper()
            elif char == 'space':
                typedin += ' '
            elif char == 'comma':
                 typedin += ','
        typedin_words = trm(typedin)
        #print(required, "\n", str(typedin))
        #print(similar_text(str(required.upper()), str(typedin)))
        add_resp()
        if counter <= 5:
            show_instruction("Mit Leertaste zum nächsten Item")
        else:
            break

def final_slide():
    show_instruction("Vielen Dank, wenden Sie sich nun bitte an die Versuchsleitung.")
    waitKeys(keyList = ['b'])

def set_screen(): # screen properties
    global win, start_text, left_label, right_label, center_disp, instruction_page
    win = Window([1280, 1000], color='Black', fullscr = 1, units = 'pix', allowGUI = True) # 1280 1024
    start_text = TextStim(win, color=instruction_color, font='Verdana', text = u'Um anzufangen, bitte die Leertaste drücken.', pos = [0,-300], height=35, bold = True, wrapWidth= 1100)
    left_label = TextStim(win, color='white', font='Verdana', text = 'unvertraut', pos = [-350,-160], height=35, alignHoriz='center')
    right_label = TextStim(win, color='white', font='Verdana', text = 'vertraut', pos = [350,-160], height=35, alignHoriz='center')
    center_disp = TextStim(win, color='white', font='Arial', text = '', height = 60)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, font='Verdana', color = instruction_color)


def start_input():
    global subj_id, dems, condition, gender, categories, true_probes, true_forename, true_surname, name_ausgeben, decknamen
    input_box = Dlg(title=u'Grunddaten', labelButtonOK=u'OK', labelButtonCancel=u'Abbrechen')
    input_box.addText(text=u'')
    input_box.addField(label=u'c.', tip = '1-12')
    input_box.addField(label=u'VP', tip = 'Ziffern')
    input_box.addText(text=u'')
    input_box.addText(text=u'Bitte ausfüllen:')
    input_box.addField(label=u'Geschlecht', initial = '', choices=[u'männlich',u'weiblich'] )
    input_box.addField(label=u'Alter', tip = 'Ziffern')
    input_box.addField(label=u'Herkunftsland', initial = '', choices=[u'Österreich',u'Deutschland',u'Schweiz'] )
    input_box.addField(label=u'Händigkeit', initial = '', choices=[u'rechtshändig',u'linkshändig'], tip = '(bevorzugte Hand zum Schreiben)' )
    input_box.addText(text=u'')
    input_box.addText(text=u'Ihr Name:')
    input_box.addText(text=u'(Jeweils nur einen Namen, kein Doppelname!)')
    input_box.addField(label=u'Vorname')
    input_box.addField(label=u'Nachname')
    input_box.addText(text=u'')
    input_box.show()
    if input_box.OK:
        stop = False
        try:
            condition = int(input_box.data[0])
        except ValueError:
            condition = 99
            print("Condition must be a number!")
        ## CONDITIONS:
        # use condition nos. for control vs. experimental group
        # plus for guilty vs innocent block first
        #
        # check if variables correctly given
        if condition not in range(1,13): # range(1,13):
            if testing:
                condition = 1 # set value for testing to skip Dlg input box
                print("condition was not set, now set to " + str(condition) + " for testing.")
            else:
                print("condition was not set correctly (should be 1/2/3/4)")
                stop = True
        try:
            subj_num = int(input_box.data[1])
        except ValueError:
            if testing:
                subj_num = 99 # set value for testing to skip Dlg input box
                print("subj_num was not set, now set to " + str(subj_num) + " for testing.")
            else:
                print("vp (subject number) was not set correctly (should be simple number)")
                stop = True
        try:
            age = int(input_box.data[3])
        except ValueError:
            if testing:
                age = 11 # set value for testing to skip Dlg input box
                print("age was not set, now set to " + str(age) + " for testing.")
            else:
                print("age was not set correctly (should be simple number)")
                stop = True
        true_forename = input_box.data[6]
        true_surname = input_box.data[7]
        if len(true_forename) < 2:
            print('forename less than 2 chars')
            if testing:
                true_forename = 'Till'
            else:
                stop = True
        elif not true_forename.isalpha():
            print('forename is not alphabetic only')
            stop = True

        if len(true_surname) < 2:
            print('surname less than 2 chars')
            if testing:
                true_surname = 'Lubczyk'
            else:
                stop = True
        elif not true_surname.isalpha():
            print('surname is not alphabetic only')
            stop = True
        if stop:
            print("\nTry again with correct inputs.\n")
            quit()
        subj_id = str(subj_num).zfill(2) + "_" + str(strftime("%Y%m%d%H%M%S", gmtime()))
        if input_box.data[2] == 'weiblich':
            gender = 2
        else:
            gender = 1
        dems = 'dems/gender/age/country/hand/reps1/rep2/rep3/rep6/drtn/dcit' + '\t' + str(gender) + '/' + str(age)  + '/' + input_box.data[4]  + '/' + input_box.data[5]

        categories = ['Name', 'Deckname', 'Operation', 'Akte', 'Pläne', 'Straße']
        confirm_dlg()
    else:
        quit()

def confirm_dlg():
    global start_date
    confirm_input = Dlg(title=u'Confirmation', labelButtonOK=u'JA', labelButtonCancel=u'Nein')
    input_feed = u'Bitte bestätigen Sie, dass Ihr Vor- und Nachname richtig geschrieben wird: ' + true_forename.upper() + ' ' + true_surname.upper()
    confirm_input.addText(text='')
    confirm_input.addText(text=input_feed)
    confirm_input.addText(text='')
    confirm_input.show()
    if confirm_input.OK:
        start_date = datetime.now()
    else:
        start_input()


def create_file():
    global data_out
    f_name = 'exp_lcp_cit_recall_task' + str(condition) + "_" + "_" + str(condition) + "_ord" + "_" + subj_id + '.txt'
    data_out=open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "condition", "probe_item", "typed_in", "similarityscore"  ] ) + "\n" )
    print("File created:", f_name)



def start_with_space():
    start_text.draw() # start with space
    center_disp.setText("+")
    center_disp.draw()
    draw_labels()
    win.flip()
    inst_resp = waitKeys(keyList = ['space',escape_key])
    end_on_esc(inst_resp[0])
    draw_labels()
    win.flip()
    wait(isi_min_max[0]/1000)


def show_instruction(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    inst_resp = waitKeys(keyList = ['space', escape_key])
    end_on_esc(inst_resp[0])



def end_on_esc(escap):
    if escap == escape_key : # escape
        print("Trying to escape?")
        instruction_page.setText('Sure you want to discontinue and quit the experiment?\n\nPress "y" to quit, or press "n" to continue.')
        instruction_page.draw()
        win.flip()
        wait(1)
        quit_resp = waitKeys(keyList = ['y', 'n'])
        if quit_resp[0] == 'y':
            print("************ ESCAPED ************")
            data_out.close()
            win.close()
            quit()
        else:
            clearEvents()
            print("Continuing...")


# from https://github.com/luosch/similar_text

def similar_str(str1, str2):
    """
    return the len of longest string both in str1 and str2
    and the positions in str1 and str2
    """
    max_len = tmp = pos1 = pos2 = 0
    len1, len2 = len(str1), len(str2)

    for p in range(len1):
        for q in range(len2):
            tmp = 0
            while p + tmp < len1 and q + tmp < len2 \
                    and str1[p + tmp] == str2[q + tmp]:
                tmp += 1

            if tmp > max_len:
                max_len, pos1, pos2 = tmp, p, q

    return max_len, pos1, pos2


def similar_char(str1, str2):
    """
    return the total length of longest string both in str1 and str2
    """
    max_len, pos1, pos2 = similar_str(str1, str2)
    total = max_len

    if max_len != 0:
        if pos1 and pos2:
            total += similar_char(str1[:pos1], str2[:pos2])

        if pos1 + max_len < len(str1) and pos2 + max_len < len(str2):
            total += similar_char(str1[pos1 + max_len:], str2[pos2 + max_len:]);

    return total


def similar_text(str1, str2):
    """
    return a int value in [0, 100], which stands for match level
    """
    if not (isinstance(str1, str) or isinstance(str1, unicode)):
        raise TypeError("must be str or unicode")
    elif not (isinstance(str2, str) or isinstance(str2, unicode)):
        raise TypeError("must be str or unicode")
    elif len(str1) == 0 and len(str2) == 0:
        return 0.0
    else:
        return int(similar_char(str1, str2) * 200.0 / (len(str1) + len(str2)))

def trm(raw_inp):
    return [w for w in raw_inp.replace(',', ' ').split(' ') if w != ''][:2]


def add_resp():
    global condition, required
    data_out.write( '\t'.join( [ str(subj_id), str(condition), str(required), str(typedin), str(similar_text(str(required.upper()), str(typedin)))]) + '\n' )
    print(required, str(typedin), similar_text(str(required.upper()), str(typedin)))




def ending ():
    data_out.write(dems + "/" +
      "\n")
    data_out.close()
    show_instruction( "ENDE" )

# EXECUTE
execute()
