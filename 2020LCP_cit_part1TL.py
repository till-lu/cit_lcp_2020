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
testing = False # True for testing, False for real recording
###
main_ddline = 1 # sec
isi_set = (500, 800, 1100)
instruction_color = '#111111' #formerly = #9999FF
############ MAIN ITEMS - paste from JS


probe_crime_list_1 = ' Ausgeben als : Tim Koch\n\n Nachricht an Deckname : Blaue Jacke\n\n Aktion : Operation Kuh\n\n Objekt : Regen Akte\n\n Inhalt des Objektes : Helikopter Pläne\n\n Adresse : Hai Straße'
probe_crime_list_2 = ' Ausgeben als : Paul Nowak\n\n Nachricht an Deckname : Weißes Shirt\n\n Aktion : Operation Fichte\n\n Objekt : Eulen Akte\n\n Inhalt des Objektes : Messing Pläne\n\n Adresse : Löwen Straße'

crime_list_1 = ["Tim Koch", "Blaue Jacke", "Operation Kuh",  "Regen Akte", "Helikopter Pläne", "Hai Straße"]
crime_list_2 = ["Paul Nowak", "Weißes Shirt","Operation Fichte","Eulen Akte","Messing Pläne","Löwen Straße"]
dummy_list_numbers = [0, 1, 2, 3, 4, 5]

training_recall_item = {0 : 'Ausgeben als', 1 : 'Nachricht an Deckname', 2 : 'Aktion', 3 : 'Objekt', 4 : 'Inhalt des Objektes', 5 : 'Adresse'}

rounds = 1


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
    consent_instructions()
    training_instruction()
    which_round_indicator()
    training_software()
    which_round_indicator()
    training_list()
    training_software()
    which_round_indicator()
    training_list()
    training_software()
    final_slide()
    win.mouseVisible = False # hide mouse


    print("************** END OF LEARNING TASK **************")

    ending() # saves demographic & final infos, gives feedback

    waitKeys(keyList = ['b']) # press B to end the exp (prevents subject from closing window)
    quit()

def consent_instructions():
    show_instruction("Bitte füllen Sie die Einverständniserklärung zur Teilnahme am Experiment aus. \nSie sollten diese vor sich auf dem Tisch finden. Bei Unklarheiten oder weiteren Fragen heben Sie leise Ihre Hand.\nWenn Sie damit fertig sind, drücken sie die Leertaste, um mit dem Experiment zu starten.")
    show_instruction("Sie werden nun eine Reihe von Aufgaben am Computer durchführen. Bitte lesen und befolgen Sie die Anweisungen sorgfältig. Sollten Sie während des Experiments Fragen haben, melden Sie sich bei der Versuchsleitung, bevor Sie fortfahren.\nDrücken Sie die Leertaste, um die Anweisungen zu sehen.")




def which_round_indicator():
    global condition
    if rounds == 1:
        show_instruction("Es folgt nun die erste Runde, in der die soeben gezeigten Wortpaare abgefragt werden. Geben Sie diese exakt so, wie sie Ihnen eben gezeigt wurden, ein. \nLeertaste drücken, um fortzufahren.")
    elif rounds == 2:
        show_instruction("Es folgen erneut alle Informationen, die Sie benötigen, wenn Sie sich als Komplize ausgeben. Damit diese Täuschung funktioniert, ist es sehr wichtig, dass jedes Detail der Nachricht korrekt ist. Bitte prägen Sie sich deshalb erneut alle Informationen ein. \nLeertaste drücken, um fortzufahren.")
    elif rounds == 3:
        show_instruction("Es folgt nun eine dritte und letzte Runde. Die Wortpaare werden noch einmal gezeigt, bevor diese ein letztes Mal abgefragt werden.\nLeertaste drücken, um fortzufahren.")






def training_instruction():
    global condition
    if condition % 2 != 0:
        probe_crime_list = probe_crime_list_1
    else:
        probe_crime_list = probe_crime_list_2
    show_instruction('Sie sollen eine Person kontaktieren, die unter Verdacht steht, kriminelle Aktivitäten begangen zu haben. Schreiben Sie dieser Person eine E-Mail, in der Sie um die Übergabe illegal erlangter Dokumente bitten. Dazu geben Sie sich als einer der Komplizen der Person aus und loggen sich in den Mail-Account dieses Komplizen ein. In der Nachricht bitten Sie den Verdächtigen, dass er Sie an einem bestimmten Ort trifft und die entsprechenden Dokumente bei sich hat. Die Informationen, die Sie für diese Aufgabe benötigen werden, werden Ihnen gleich präsentiert.\n\n Drücken Sie die Leertaste um fortzufahren.')
    show_instruction('Für das Verfassen der E-Mail werden Sie die folgenden Informationen brauchen. Sie loggen sich in den Uni Wien Webmail Account des Komplizen ein und senden dann eine Nachricht an den Decknamen der anderen verdächtigen Person. Sie erklären dieser Person, dass es um eine bestimmte Aktion geht und bitten die Person, Sie an einer bestimmten Adresse zu treffen und zu diesem Treffen das genannte Objekt mit dem sich darin befindenden Inhalt mitzubringen. Drücken Sie daher erst die Leertaste, wenn Sie die unten stehenden Wortpaare, die für das Verfassen der Nachricht benötigt werden, gründlich auswendig gelernt haben. Im Folgenden werden diese in drei Runden abgefragt.\n\n' +  probe_crime_list)

def training_list():
    global condition
    if condition % 2 != 0:
        probe_crime_list = probe_crime_list_1
    else:
        probe_crime_list = probe_crime_list_2
    show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Items gründlich auswendig gelernt haben.\nSie loggen sich in den Uni Wien Webmail Account des Komplizen ein und senden dann eine Nachricht an den Decknamen der anderen verdächtigen Person. Sie erklären dieser Person, dass es um eine bestimmte Aktion geht und bitten die Person, Sie an einer bestimmten Adresse zu treffen und zu diesem Treffen das genannte Objekt mit dem sich darin befindenden Inhalt mitzubringen.\n\n' +  probe_crime_list)


def training_software():
    global condition, required, typedin, rounds
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
        instr_display =  TextStim(win, color=instruction_color, font='Helvetica', text = u'Bitte geben Sie im Folgenden das korrekte, zuvor auswendig gelernte Wortpaar ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Helvetica', text = cue + ':', pos=(-100, 0), alignHoriz = 'right', height=35)
        input_display =  TextStim(win, color='black', pos=(-100, -4), alignHoriz = 'left', height=35, bold = True, colorSpace='rgb')
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
        add_resp()
        if counter <= 5:
            wait(0.5)
        else:
            break
    rounds += 1




def final_slide():
    show_instruction("Sie haben nun alle relevanten Informationen gelernt. Bitte führen Sie die Aufgabe nun aus, indem Sie im Google Chrome Browser auf webmail.univie.ac.at gehen und sich dort mit dem eingespeicherten user:account einloggen und die Nachricht mit den gelernten Informationen verfassen und senden. Wenden Sie sich bitte an die Versuchsleitung, um zum Desktop zu gelangen und führen Sie die Aufgabe dann eigenständig aus. Sollten Sie weitere Fragen haben, wenden Sie sich bitte ebenfalls an die Versuchsleitung.")
    waitKeys(keyList = ['b'])

def set_screen(): # screen properties
    global win, start_text, left_label, right_label, center_disp, instruction_page
    win = Window([1280, 1000], color='#dddddd', fullscr = 1, units = 'pix', allowGUI = True) # 1280 1024
    start_text = TextStim(win, color=instruction_color, font='Helvetica', text = u'Um anzufangen, bitte die Leertaste drücken.', pos = [0,-300], height=35, bold = True, wrapWidth= 1100)
    left_label = TextStim(win, color='#111111', font='Verdana', text = 'unvertraut', pos = [-350,-160], height=35, alignHoriz='center')
    right_label = TextStim(win, color='#111111', font='Verdana', text = 'vertraut', pos = [350,-160], height=35, alignHoriz='center')
    center_disp = TextStim(win, color='#111111', font='Arial', text = '', height = 60)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, font='Helvetica', color = instruction_color)


def start_input():
    global subj_id, dems, condition, gender
    input_box = Dlg(title=u'Grunddaten', labelButtonOK=u'OK', labelButtonCancel=u'Abbrechen')
    input_box.addText(text=u'')
    input_box.addField(label=u'c.', tip = '1-8')
    input_box.addField(label=u'VP', tip = 'Ziffern')
    input_box.addText(text=u'')
    input_box.addText(text=u'Bitte ausfüllen:')
    input_box.addField(label=u'Geschlecht', initial = '', choices=[u'männlich',u'weiblich', u'divers'] )
    input_box.addField(label=u'Alter', tip = 'Ziffern')
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
        # 1       probes 1 + exp + crime first
        # 2       probes 2 + exp + nocrime first
        # 3       probes 1 + exp + nocrime first
        # 4       probes 2 + exp + crime first
        # 5       probes 1 + control + crime first
        # 6       probes 2 + control + no crime first
        # 7       probes 1 + control + no crime first
        # 8       probes 2 + control + crime first first
        # check if variables correctly given
        if condition not in range(1,8):
            if testing:
                condition = 1 # set value for testing to skip Dlg input box
                print("condition was not set, now set to " + str(condition) + " for testing.")
            else:
                print("condition was not set correctly (should be 1/2/3/4/5/6/7/8)")
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
        if stop:
            print("\nTry again with correct inputs.\n")
            quit()
        subj_id = str(subj_num).zfill(3) + "_" + str(strftime("%Y%m%d%H%M%S", gmtime()))
        if input_box.data[2] == 'weiblich':
            gender = 2
        elif input_box.data[2] == 'männlich':
            gender = 1
        else:
            gender = 3
        dems = 'dems\tgender/age\t' + str(gender) + '/' + str(age)
        start_date = datetime.now()
    else:
        quit()



def create_file():
    global data_out
    f_name = 'lcp1_learning_' + str(condition) + "_" + subj_id + '.txt'
    data_out=open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "condition", "probe_item", "typed_in", "similarityscore", "rounds"  ] ) + "\n" )
    print("File created:", f_name)



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
    data_out.write( '\t'.join( [ str(subj_id), str(condition), str(required), str(typedin), str(similar_text(str(required.upper()), str(typedin)))]) + '\t' +  str(rounds) + '\n' )
    print(required, str(typedin), similar_text(str(required.upper()), str(typedin)))




def ending ():
    data_out.write(dems + "\n")
    data_out.close()
    show_instruction( "ENDE" )

# EXECUTE
execute()
