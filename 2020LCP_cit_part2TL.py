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
instruction_color = '#111111'
############ MAIN ITEMS - paste from JS
##small things to do:
## - ending / debriefing completely, questions necessary?
## - block instructions
## - how to ask for recall items


distraction_text = "Bearbeiten Sie nun bitte die Ihnen auf einem Blatt gereichten Aufgaben. Sie haben dafür 10 Minuten Zeit. Drücken Sie anschließend die Leertaste um fortzufahren."

target_guilty_list = ' Ausgeben als : Frank Moser\n\n Nachricht an Deckname : Grüner Hut\n\n Aktion : Operation Schwein\n\n Objekt : Schnee Akte\n\n Inhalt des Objektes : Schiff Pläne\n\n Adresse : Barsch Straße'

target_innocent_list = ' Ausgeben als : Sven Groß\n\n Nachricht an Deckname : Grüne Krawatte\n\n Aktion : Operation Tanne\n\n Objekt : Schwan Akte\n\n Inhalt des Objektes : Stahl Pläne\n\n Adresse : Fuchs Straße'

probes_guilty = [u"Tim Koch", u"Blaue Jacke", u"Operation Kuh", u"Regen Akte", u"Helikopter Pläne", u"Hai Straße"]

probes_innocent = [u"Paul Nowak", u"Weißes Shirt", u"Operation Fichte", u"Eulen Akte", u"Messing Pläne", u"Löwen Straße"]

targets_guilty = [u"Frank Moser", u"Grüner Hut", u"Operation Schwein", u"Schnee Akte", u"Schiff Pläne", u"Barsch Straße"]

targets_innocent = [u"Sven Groß", u"Grüne Krawatte", u"Operation Tanne", u"Schwan Akte", u"Stahl Pläne", u"Fuchs Straße"]

irrelevants_guilty = [u"Braune Schuhe", u"Roter Schal", u"Graue Hose", u"Schwarze Handschuhe", u"Hans Krause", u"Nick Lange", u"Max Horn", u"Leo Bauer", u"Operation Pferd", u"Operation Ziege", u"Operation Schaf", u"Operation Maultier", u"Hagel Akte", u"Wind Akte", u"Graupel Akte", u"Nebel Akte", u"Panzer Pläne", u"Flugzeug Pläne", u"Bomben Pläne", u"Waffen Pläne", u"Kabeljau Straße", u"Karpfen Straße", u"Hecht Straße", u"Forelle Straße"]

irrelevants_innocent = [u"Beiger Anzug", u"Rote Weste", u"Hellbrauner Gürtel", u"Schwarze Socken", u"Ben Schmid", u"Emil Burger", u"Marc Huber", u"Jan Schreiber", u"Operation Eiche", u"Operation Birke", u"Operation Ulme", u"Operation Pinie", u"Zaunkönig Akte", u"Enten Akte", u"Krähen Akte", u"Gänse Akte", u"Zinn Pläne", u"Zink Pläne", u"Blei Pläne", u"Eisen Pläne", u"Reh Straße", u"Wolf Straße", u"Bären Straße", u"Elch Straße"]

dummy_list_numbers = [0,1,2,3,4,5]

dummy_list_numbers_2 = [0,1,2,3,4,5]

training_target = 'Grüner Hut'

key_pair = { 'always' : { 'nontarg': 'f', 'target' : 'j', 'descr' : 'F (linker Zeigefinger) und J (rechter Zeigefinger)' }}

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
    basic_variables() # basic variables assigned, calculated
    set_screen() # creates psychopy screen and stim objects
    # window opens
    distraction_task()
    cm_warning()
    create_file() # created output file
    set_block_info() # sets block text and related infos based on conditions
    win.mouseVisible = False # hide mouse

    next_block() # begin task & run until finished

    print("************** END OF EXPERIMENT **************")

    ending() # saves demographic & final infos, gives feedback

    waitKeys(keyList = ['b']) # press B to end the exp (prevents subject from closing window)
    quit()

def distraction_task():
    show_instruction(distraction_text)



def cm_warning():
    global win, start_text, left_label, right_label, center_disp, instruction_page, instruction_color
    show_instruction("Jetzt geht es um Ihre Merkfähigkeit. Sie werden erneut Wortpaare auswendig lernen und diese in drei Runden wiedergeben. Darauf folgt ein Test, in dem Ihnen Wortpaare gezeigt werden. In diesem Test sollen Sie auf die nun gleich gezeigten und anschließend von Ihnen gelernten Wortpaare mit einer anderen Taste reagieren als auf alle anderen gezeigten Wortpaare. \n\nUm weiterzugehen, drücken Sie die Leertaste.")
    if condition in [1, 2, 3, 4]:
        cit_warning_text()
    instruction_color = '#9999FF'
    win = Window([1280, 1000], color='Black', fullscr = 1, units = 'pix', allowGUI = True) # 1280 1024
    start_text = TextStim(win, color=instruction_color, font='Verdana', text = u'Um anzufangen, bitte die Leertaste drücken.', pos = [0,-300], height=35, bold = True, wrapWidth= 1100)
    left_label = TextStim(win, color='white', font='Verdana', text = 'nein', pos = [-350,-160], height=35, alignHoriz='center')
    right_label = TextStim(win, color='white', font='Verdana', text = 'ja', pos = [350,-160], height=35, alignHoriz='center')
    center_disp = TextStim(win, color='white', font='Arial', text = '', height = 60)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, font='Verdana', color = instruction_color)



def crime_text():
    show_instruction(probe_crime_text)


def cit_warning_text():
    show_instruction(text_warning_cit)
    waitKeys(keyList = ['b']) # b to continue

text_warning_cit = "ACHTUNG: Im nachfolgenden Test werden Sie auch Wörter sehen, die Sie für das Senden der kriminellen E-Mail gelernt haben. Forschungen haben gezeigt, dass die Reaktionszeit auf im Zusammenhang mit Straftaten stehenden Begriffen langsamer ist als auf andere. \nDies bedeutet, dass Sie im Test länger für eine Antwort brauchen würden, wenn das gezeigte Wort aus der E-Mail stammt. \n\nVersuchen Sie daher, eine solche Verzögerung zu vermeiden und zu „vertuschen“, dass Sie die entsprechenden Wörter schon einmal gesehen haben. Lernen Sie dazu die im folgenden präsentierte Liste an Begriffen besonders gut, damit diese Ihnen noch vertrauter werden und Sie sie schneller einordnen können als jene aus der Straftat. Versuchen sie außerdem, mehr auf den Kontext der Wörter zu achten (d.h. woher Ihnen das Wort bekannt ist), als rein nach Vertrautheit zu entscheiden. Dabei ist es aber wichtig, dass Sie trotzdem nicht zu langsam antworten! Je erfolgreicher Sie Ihr Wissen über die Begriffe aus der E-Mail vertuschen können, desto kürzer dauert der Test für Sie. \n\nWenn Sie diesen Hinweis gründlich gelesen haben, heben Sie bitte Ihre Hand und geben Sie der Versuchsleitung anschließend mündlich bekannt, dass sie das weitere Vorgehen verstanden haben." # for experimental group,


training_recall_item = {0 : 'Ausgeben als', 1 : 'Nachricht an Deckname', 2 : 'Aktion', 3 : 'Objekt', 4 : 'Inhalt des Objektes', 5 : 'Adresse'}





def ending():
    full_duration = round( ( datetime.now() - start_date ).total_seconds()/60, 2)

    info = 'Danke für die Teilnahme. Wenn Sie möchten, können Sie gehen, aber bitte seien Sie leise dabei.\n\nKurze Information über den Test:\n\nIn dieser Studie versuchen wir, die Details aus der zu Beginn verfassten E-Mail von anderen Items zu unterscheiden. Ziel des Tests ist es, anhand von Reaktionszeiten herauszufinden, wenn eine Person versucht, Wissen über bestimmte Items zu verschleiern bzw. zu verheimlichen. Dies geschieht auf Basis der Vermutung, dass Reaktionszeiten für die Items, die für die anfängliche E-Mail benötigten wurden langsamer ausfallen, als im Falle anderer Items. Hauptanliegen dieser Studie ist es, zu zeigen, ob dies auch funktioniert, wenn die Funktionsweise des Teste vorher erklärt wird.\n\nFür weitere Informationen wenden Sie sich bitte an den Versuchsleiter (oder schreiben Sie eine E-mail an Gaspar Lukacs).'

    data_out.write(dems + "/" +
      "/".join( [ str(nmbr) for nmbr in
      [practice_repeated['block1'],
      practice_repeated['block2'],
      practice_repeated['block3'],
      full_duration,
      ] ] ) +
      "\n")
    data_out.close()
    show_instruction( info )

def set_screen(): # screen properties
    global win, start_text, left_label, right_label, center_disp, instruction_page
    win = Window([1280, 1000], color='#dddddd', fullscr = 1, units = 'pix', allowGUI = True) # 1280 1024
    start_text = TextStim(win, color=instruction_color, font='Helvetica', text = u'Um anzufangen, bitte die Leertaste drücken.', pos = [0,-300], height=35, bold = True, wrapWidth= 1100)
    left_label = TextStim(win, color='#111111', font='Verdana', text = 'unvertraut', pos = [-350,-160], height=35, alignHoriz='center')
    right_label = TextStim(win, color='#111111', font='Verdana', text = 'vertraut', pos = [350,-160], height=35, alignHoriz='center')
    center_disp = TextStim(win, color='#111111', font='Arial', text = '', height = 60)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, font='Helvetica', color = instruction_color)





def task_instructions( whichtext = ''):
    keys_info = 'Während des Tests sehen Sie Wörter in der Mitte des Bildschirms auftauchen. Sie müssen jedes Wort entweder mit der linken oder mit der rechten Antworttaste kategorisieren. Diese Tasten sind ' + key_pair['always']['descr'] + '. '
    main_item_info = ' '

def set_block_info():
    global block_info, block_num, incorrect, tooslow, move_on
    move_on = '\n\nUm weiterzugehen, drücken Sie die Leertaste.\n\nFalls nötig, drücken Sie die Taste ENTER (oder eine der Pfeiltasten) um die vollständigen Anweisungen erneut zu lesen.'
    block_info = [""]
#    if block_num == 1:
#        block_info.append( 'Im Folgenden kategorisieren Sie bitte Wortpaare, die sie in der vorherigen Aufgabe auswendig gelernt und wiedergegeben haben als vertraut, alle anderen als unvertraut. \n\nUm weiterzugehen, drücken Sie die Leertaste.' + move_on)
#    elif block_num == 2:
#        if condition in [1, 2, 3, 4]:
#            block_info.append(text_warning_cit + move_on)
#    elif block_num == 3:
#        block_info.append( ' Die Aufgabe bleibt genau dieselbe.' + move_on)

def start_input():
    global subj_id, dems, condition, start_date
    input_box = Dlg(title=u'Grunddaten', labelButtonOK=u'OK', labelButtonCancel=u'Abbrechen')
    input_box.addText(text=u'')
    input_box.addField(label=u'c.', tip = '1-8')
    input_box.addField(label=u'VP', tip = 'Ziffern')
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
        if condition not in range(1,9): # range(1,13):
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
        subj_id = str(subj_num).zfill(2) + "_" + str(strftime("%Y%m%d%H%M%S", gmtime()))
        dems = 'sbjID + condition' + str(subj_num) + str(condition)
        start_date = datetime.now()




def trm(raw_inp):
    return [w for w in raw_inp.replace(',', ' ').split(' ') if w != ''][:2]

def target_check_one():
    global condition, required, typedin, rounds
    if rounds == 1:
        show_instruction('Im Folgenden wird Ihnen erneut eine Liste an Wortpaaren präsentiert, die Sie danach, erneut in drei Runden, wiedergeben müssen. \n\nDrücken Sie die Leertaste, um fortzufahren.')
    required_items = []
    if condition in [1,2,5,6]:
        required_items = targets_guilty
        if rounds == 1:
            show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_guilty_list)
        elif rounds == 2:
            show_instruction('Es folgt nun die zweite Runde.\n\nDrücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_guilty_list)
        elif rounds == 3:
            show_instruction('Es folgt die letzte Runde des Abfragetests. Lernen Sie unten stehenden Wortpaare gründlich auswendig, drücken Sie Leertaste, um fortzufahren. \n\n' + target_guilty_list)
    else:
        required_items = targets_innocent
        if rounds == 1:
            show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_innocent_list)
        elif rounds == 2:
            show_instruction('Es folgt nun die zweite Runde.\n\nDrücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_innocent_list)
        elif rounds == 3:
            show_instruction('Es folgt die letzte Runde des Abfragetests. Lernen Sie unten stehenden Wortpaare gründlich auswendig, drücken Sie Leertaste, um fortzufahren. \n\n' + target_innocent_list)
    combine_shuffle = list(zip(required_items, dummy_list_numbers))
    shuffle(combine_shuffle)
    required_items[:], dummy_list_numbers[:] = zip(*combine_shuffle)
    counter = 0
    while counter <= 5:
        required = required_items[counter]
        #required_2 = ''
        cue = training_recall_item[dummy_list_numbers[counter]]
        counter += 1
        instr_display =  TextStim(win, color=instruction_color, font='Verdana', text = u'Bitte geben Sie im Folgenden die korrekte Antwort ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Verdana', text =  cue + ':', pos=(-100, 0), alignHoriz = 'right', height=35)
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
        add_recall_resp()
        if counter <= 5:
            wait(0.5)
        else:
            break
    rounds += 1


def target_check_two():
    global condition, required, typedin, rounds, dummy_list_numbers, training_recall_item, dummy_list_numbers_2
    required_items = []
    if rounds == 4:
        show_instruction('Im Folgenden wird Ihnen eine weitere Liste an Wortpaaren präsentiert, die Sie danach wiedergeben müssen. \n\nDrücken Sie die Leertaste, um fortzufahren.')
    if condition in [1,2,5,6]:
        required_items = targets_innocent
        if rounds == 4:
            show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_innocent_list)
        elif rounds == 5:
            show_instruction('Es folgt nun die zweite Runde.\n\n Drücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_innocent_list)
        elif rounds == 6:
            show_instruction('Es folgt die letzte Runde des Abfragetests. Lernen Sie unten stehenden Wortpaare gründlich auswendig, drücken Sie Leertaste, um fortzufahren. \n\n' + target_innocent_list)
    else:
        required_items = targets_guilty
        if rounds == 4:
            show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_guilty_list)
        elif rounds == 5:
            show_instruction('Es folgt nun die zweite Runde.\n\n Drücken Sie die Leertaste, wenn Sie die unten stehenden Wortpaare gründlich auswendig gelernt haben.\n\n' + target_guilty_list)
        elif rounds == 6:
            show_instruction('Es folgt die letzte Runde des Abfragetests. Lernen Sie unten stehenden Wortpaare gründlich auswendig, drücken Sie Leertaste, um fortzufahren. \n\n' + target_guilty_list)
    combine_shuffle = list(zip(required_items, dummy_list_numbers_2))
    shuffle(combine_shuffle)
    required_items[:], dummy_list_numbers_2[:] = zip(*combine_shuffle)
    counter = 0
    while counter <= 5:
        #required_2 = ''
        required = required_items[counter]
        cue = training_recall_item[dummy_list_numbers_2[counter]]
        counter += 1
        instr_display =  TextStim(win, color=instruction_color, font='Verdana', text = u'Bitte geben Sie im Folgenden die korrekte Antwort ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Verdana', text = cue + ':', pos=(-100, 0), alignHoriz = 'right', height=35)
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
        add_recall_resp()
        if counter <= 5:
            wait(0.5)
        else:
            break
    rounds += 1



def create_items(x_probes, x_targets, x_irrelevants, xtimes):
    # list of dicts with all possible items
    stims_base = []
    for itm in x_probes:
        stims_base.append({'word': itm, 'item_type': 'probe'})
    for itm in x_targets:
        stims_base.append({'word': itm, 'item_type': 'target'})
    for itm in x_irrelevants:
        stims_base.append({'word': itm, 'item_type': 'irrelevant'})
    # this list is added one by one to the full final list
    # each time in a new random order
    full_stim_list = []
    for i in range(xtimes):
        shuffle(stims_base)
        full_stim_list += deepcopy(stims_base)
    return(full_stim_list)


def main_items():
    global blcks_base, crrnt_phase
    print('main_items()')
    crrnt_phase = 'main'
    block_stim_base = blcks_base.pop(0)
    main_stims = block_stim_base
    return [dct for sublist in main_stims for dct in sublist] # flatten





def basic_variables():
    global stopwatch, blocks_order, guilt, block_num, all_main_rts, kb_device, practice_repeated, firsttime, guilt
    stopwatch = Clock()
    if condition in [1,4,5,8]:
        guilt = 1 # start guilty
    else:
        guilt = 0 # start innocent
     ## CONDITIONS:
        # 1       probes 1 + exp + crime first
        # 2       probes 2 + exp + nocrime first
        # 3       probes 1 + exp + nocrime first
        # 4       probes 2 + exp + crime first
        # 5       probes 1 + control + crime first
        # 6       probes 2 + control + no crime first
        # 7       probes 1 + control + no crime first
        # 8       probes 2 + control + crime first
    block_num = 0
    all_main_rts = { 'probe' : [], 'irrelevant': [] }
    practice_repeated = { 'block1' : 0, 'block2': 0, 'block3': 0}
    firsttime = True
    io = launchHubServer()
    kb_device = io.devices.keyboard

# create output file, begin writing, reset parameters
def create_file():
    global data_out
    f_name = 'exp_lcp_cit_maintask' + str(condition) + "_" + "_" + str(guilt) + "_ord" + "_" + subj_id + '.txt'
    data_out=open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "condition", "phase", "block_number", "trial_number", "stimulus_shown",  "stim_type", "response_key", "rt_start", "incorrect", "too_slow", "press_duration", "isi", "date_in_ms" ] ) + "\n" )
    print("File created:", f_name)

def str_if_num( num_val ):
    if isinstance(num_val, str) or isinstance(num_val, unicode):
        return num_val
    else:
        return str( num_val*1000 )

def add_resp():
    global incorrect, tooslow
    data_out.write( '\t'.join( [ subj_id, str(condition), crrnt_phase, str(block_num), str(trial_num+1), stim_text, stim_current["item_type"], stim_type, resp_key, str_if_num(rt_start), str(incorrect), str(tooslow), str_if_num(press_dur), str_if_num( isi_set[0]/1000 + isi_delay ), str(strftime("%Y%m%d%H%M%S", gmtime())), str(guilt) ] ) + '\n' )
    print("resp key:", resp_key, "for stim:", stim_text, "incorrect:", incorrect, "rt_start:", rt_start)


def add_recall_resp():
    global condition, required
    data_out.write( '\t'.join( [ str(subj_id), str(condition), str(required), str(typedin), str(similar_text(str(required.upper()), str(typedin.upper())))]) + '_round' + str(rounds) + '\n' )
    print(required.upper(), str(typedin.upper()), similar_text(str(required.upper()), str(typedin)))

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
    wait(isi_set[0]/1000)

def draw_labels():
    if block_num <= 2:
        left_label.draw()
        right_label.draw()

def assign_keys():
    global targetkey, nontargetkey
    targetkey = key_pair['always']['target']
    nontargetkey = key_pair['always']['nontarg']

def next_block():
    global ddline, block_num, rt_data_dict, crrnt_instr, blck_itms, firsttime, crrnt_phase, condition, guilt
    block_num += 1
    if block_num == 1:
        target_check_one()
        target_check_one()
        target_check_one()
        show_instruction('Nun folgt der Test zu der Liste mit Wortkombinationen, die Sie gerade gelernt haben. Sie werden verschiedene Wortkombinationen sehen, die nacheinander auf dem Monitor gezeigt werden. Bei jeder dieser Kombinationen sollen Sie so schnell wie möglich angeben, ob diese in der gelernten Liste enthalten war oder nicht. War die Wortkombination in der zuvor gelernten Liste enthalten, drücken Sie „J“ (JA). Wird eine andere Wortkombination gezeigt, so drücken Sie „F“ (NEIN). Verwenden Sie dazu Ihre beiden Zeigefinger und positionieren sie direkt über den Tasten, damit Sie so schnell und akkurat wie möglich reagieren können. Leertaste drücken, um fortzufahren.')
        show_instruction("Probieren Sie dies nun aus, in dem sie jetzt 'J' drücken...")
        waitKeys(keyList = ['j'])
        show_instruction("...und drücken Sie nun bitte 'F'.")
        waitKeys(keyList = ['f'])
        crrnt_phase = 'main'
        rt_data_dict = {}
        assign_keys()
        if condition in [1, 2, 5, 6]:
            block1_items = create_items(probes_guilty, targets_guilty, irrelevants_guilty, 3)
        elif condition in [3, 4, 7, 8]:
            block1_items = create_items(probes_innocent, targets_innocent, irrelevants_innocent, 3)
        blck_itms = block1_items
        ddline = main_ddline
    elif block_num == 2:
        if guilt == 1:
            guilt = 0
        else:
            guilt = 1
        crrnt_phase = 'main'
        if condition in [1, 2, 5, 6]:
            block2_items = create_items(probes_innocent, targets_innocent, irrelevants_innocent, 3)
            target_check_two()
            target_check_two()
            target_check_two()
        elif condition in [3, 4, 7, 8]:
            block2_items = create_items(probes_guilty, targets_guilty, irrelevants_guilty, 3)
            target_check_two()
            target_check_two()
            target_check_two()
        blck_itms = block2_items
        ddline = main_ddline
    if testing == True:
        blck_itms = blck_itms[0:5]
    while block_num <= 2:
        run_block()


def show_instruction(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    inst_resp = waitKeys(keyList = ['space', escape_key])
    end_on_esc(inst_resp[0])

def show_block_instr():
    global condition, training_target
    if condition in [3,4,7,8]:
        training_target = 'Grüne Krawatte'
    if block_num == 1:
        instruction_page.setText( 'Leertaste drücken, um mit dem Test zu beginnen')
    elif block_num == 2:
        instruction_page.setText('Es folgt erneut ein Test zu der Liste mit Wortkombinationen, die Sie gerade gelernt haben. \nDrücken Sie wieder die rechte Taste (J - Ja) für die von Ihnen so eben wiedergegebenen Wortpaare und die linke Taste (F - Nein) für alle anderen Wortpaare. Seien Sie so schnell und genau wie möglich.\n')
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    show_again = ['left', 'up', 'right', 'down','return']
    inst_resp = waitKeys( keyList = [ 'space', escape_key ] + show_again )
    end_on_esc( inst_resp[0] )
    if inst_resp[0] in show_again:
        show_instruction('\n\nUm weiterzugehen, drücken Sie die Leertaste.' )
        show_block_instr()

def run_block():
    global block_num, trial_num, stim_current, stim_text, stim_type, incorrect, tooslow, first_wrong, show_feed, ddline, isi_delay, resp_key, rt_start, press_dur
    show_block_instr()
    first_wrong = False
    print("len(blck_itms):", len(blck_itms))
    start_with_space()
    for trial_num in range(len(blck_itms)): # go through all stimuli of current block
        print("------- Trial number:", trial_num, "In block:", block_num, "C:", condition, "ord:")
        stim_current = blck_itms[trial_num]
        incorrect = 0
        tooslow = 0
        stim_type = stim_current['item_type']
        stim_text = stim_current["word"]
        isi_delay = (choice(isi_set) - isi_set[0]) / 1000
        wait(isi_delay) # wait ISI
        center_disp.setText(stim_text.upper())
        draw_labels()
        center_disp.draw()
        win.callOnFlip(stopwatch.reset)
        kb_device.clearEvents()
        clearEvents()
        win.flip()
        response = waitKeys(maxWait = ddline, keyList=[targetkey, nontargetkey, escape_key], timeStamped=stopwatch)
        if not response:
            rt_start = stopwatch.getTime()
            resp_key = '-'
            tooslow += 1
            show_tooslow()
        else:
            resp_key = response[0][0]
            rt_start = response[0][1]
            end_on_esc(resp_key)
            if resp_key == targetkey:
                if stim_type in ("target"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
            elif resp_key == nontargetkey:
                if stim_type[:10] in ("probe","irrelevant"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
        draw_labels()
        win.flip()
        wait(isi_set[0]/1000)
        press_dur = '-' # remains this if none found, or not with correct key
        for ke in kb_device.getReleases(): # get io keypress events for duration
            try:
                if ke.key == resp_key: # if matches the pygame key, should be fine
                    press_dur = ke.duration # store io keypress duration
            except Exception:
                pass
            break
        add_resp() # store trial data
        collect_rts()
        if block_num > 2:
            break
    while block_num <= 2:
        next_block()

def collect_rts(): # for practice evaluation & dcit calculation
    global rt_data_dict, all_main_rts, rt_start
    if (incorrect+tooslow) > 0:
        rt_start = -9
    if crrnt_phase == 'practice':
        if stim_type[:10] in ("probe","irrelevant"):
            group_type = 'main_item'
        else:
            group_type = stim_type
        if group_type not in rt_data_dict:
            rt_data_dict[group_type] = []
        rt_data_dict[group_type].append(rt_start)
    if crrnt_phase == 'main' and stim_type[:10] in ("probe","irrelevant") and incorrect != 1 and tooslow != 1 and rt_start > 0.15 and rt_start < main_ddline:
        all_main_rts[ stim_type[:10] ].append(rt_start)


def show_tooslow():
    center_disp.text = 'Zu langsam!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(1)
    center_disp.color = 'white'


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

# EXECUTE
execute()
