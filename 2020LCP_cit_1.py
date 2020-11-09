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

blocks_cit = 0 # for now to have guilty condition in first block, maybe use condition numbers to randomize

probe_crime_text = "Gebe dich als Person mit dem Namen Tim Koch aus und sende eine Nachricht an die Person mit dem Decknamen 'Blaue Jacke'.\nIn dieser Nachricht schreibst du 'Blaue Jacke' es gehe um die Opreation Kuh und du bittest darum, die Regen Akte mit den U-Boot Plänen zur Hai Straße zu bringen.\n\n Leertaste drücken um fortzufahren.\n Im Folgenden werden die Details dieser Anordnung abgefragt."

probe_crime_list = ' Username : Tim Koch\n\n Deckname : Blaue Jacke\n\n Operation : Operation Kuh\n\n Akte : Regen Akte\n\n Pläne : U Boot Pläne\n\n Ort : Hai Strasse'

distraction_text = "Bearbeiten Sie nun bitte die Ihnen auf einem Blatt gereichten Aufgaben. Sie haben dafür 10 Minuten Zeit. Drücken Sie anschließend die Leertaste um fortzufahren."

target_guilty_list = ' Username : Frank Moser\n\n Deckname : Grüner Hut\n\n Operation : Operation Schwein\n\n Akte : Schnee Akte\n\n Pläne : Schiff Pläne\n\n Ort : Barsch Strasse'

target_innocent_list = ' Username : Sven Groß\n\n Deckname : Grüne Krawatte\n\n Operation : Operation Tanne\n\n Akte : Schwan Akte\n\n Pläne : Stahl Pläne\n\n Ort : Fuchs Strasse'

crime_learning_dict = {u"user": u"Tim Koch", u"person" : u"Blaue Jacke", u"operation" : u"Operation Kuh", u"akte" : u"Regen Akte", u"plan" : u"U-Boot Pläne", u"strasse" : u"Hai Strasse"}

probes_guilty = [u"Tim Koch", u"Blaue Jacke", u"Operation Kuh", u"Regen Akte", u"U-Boot Pläne", u"Hai Straße"]

probes_innocent = [u"Paul Nowak", u"Weißes Shirt", u"Operation Fichte", u"Eulen Akte", u"Messing Pläne", u"Löwen Straße"]

targets_guilty = [u"Frank Moser", u"Grüner Hut", u"Operation Schwein", u"Schnee Akte", u"Schiff Pläne", u"Barsch Straße"]

targets_innocent = [u"Sven Groß", u"Grüne Krawatte", u"Operation Tanne", u"Schwan Akte", u"Stahl Pläne", u"Fuchs Straße"]

irrelevants_guilty = [u"Braune Schuhe", u"Roter Schal", u"Graue Hose", u"Schwarze Handschuhe", u"Hans Krause", u"Nick Lange", u"Max Horn", u"Leo Bauer", u"Operation Pferd", u"Operation Ziege", u"Operation Schaf", u"Operation Maultier", u"Hagel Akte", u"Wind Akte", u"Graupel Akte", u"Nebel Akte", u"Panzer Pläne", u"Flugzeug Pläne", u"Bomben Pläne", u"Waffen Pläne", u"Kabeljau Straße", u"Karpfen Straße", u"Hecht Straße", u"Forelle Straße"]

irrelevants_innocent = [u"Beiger Anzug", u"Rote Weste", u"Hellbrauner Gürtel", u"Schwarze Socken", u"Ben Schmid", u"Emil Burger", u"Marc Huber", u"Jan Schreiber", u"Operation Eiche", u"Operation Birke", u"Operation Ulme", u"Operation Pinie", u"Zaunkönig Akte", u"Enten Akte", u"Krähen Akte", u"Gänse Akte", u"Zinn Pläne", u"Zink Pläne", u"Blei Pläne", u"Eisen Pläne", u"Reh Straße", u"Wolf Straße", u"Bären Straße", u"Elch Straße"]

key_pair = { 'always' : { 'nontarg': 'k', 'target' : 'l', 'descr' : 'K (linker Zeigefinger) und L (rechter Zeigefinger)' }}



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
    item_selection() # select items
    training_software()
    distraction_task()
    create_file() # created output file
    create_item_base() # base of items to be presented
    set_block_info() # sets block text and related infos based on conditions
    win.mouseVisible = False # hide mouse

    next_block() # begin task & run until finished

    print("************** END OF EXPERIMENT **************")

    ending() # saves demographic & final infos, gives feedback

    waitKeys(keyList = ['b']) # press B to end the exp (prevents subject from closing window)
    quit()

def distraction_task():
    show_instruction(distraction_text)

def crime_text():
    show_instruction(probe_crime_text)


def cit_warning_text():
    show_instruction(text_warning_cit)

text_warning_cit = "Im Folgenden wird ein Reaktionszeit-basierter Lügentest durchgeführt. Achten Sie auf ... etc. " # for experimental group,



training_recall_item = {0 : 'Username', 1 : 'Deckname', 2 : 'Operation', 3 : 'Akte', 4 : 'Pläne', 5 : 'Ort'}


def training_software():
    show_instruction('Lesen Sie den folgenden Text mehrmals aufmerksam durch. Sie werden im Folgenden zu den Details aus dem Text gefragt.\n\n' + probe_crime_text)
    show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Items gründlich auswendig gelernt haben.\n\n' + probe_crime_list)
    training_z = 0
    if testing == True:
        training_y = 17
    else:
        training_y = 0
    while training_z <= 5 and training_y <= 17:
        training_itms = [u"TIM KOCH", u"BLAUE JACKE", u"OPERATION KUH", u"REGEN AKTE", u"U BOOT PLÄNE", u"HAI STRASSE"] # could also use dict and possibly randomize the order for each participant
        instr_display =  TextStim(win, color=instruction_color, font='Verdana', text = u'Bitte geben Sie im Folgenden die korrekte Antwort ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Verdana', text = 'Geben Sie ' + training_recall_item[training_z] + ' ein:', pos=(-100, 0), alignHoriz = 'right', height=35)
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
        if typedin == training_itms[training_z] or typedin_words[0] == "PASS":
            training_z += 1
            training_y += 1
            show_instruction("Richtig! Leertaste drücken, um fortzufahren.")
            if training_y == 6 or training_y == 12:
                training_z = 0
        else:
            instruction_page.setText('Falsch. Lesen Sie bitte die Instruktionen nochmals!')
            instruction_page.draw()
            win.flip()
            wait(2)
            if testing == True:
                training_z = training_z
                training_y = training_y
            else:
                training_z = 0
                training_y = 0 # depending on how strict we want to be
                show_instruction('Bitte lernen Sie die folgenden Items auswendig, der Abfragetest startet von vorne:\n\n' + probe_crime_list)



def ending():
    full_duration = round( ( datetime.now() - start_date ).total_seconds()/60, 2)

    if len(all_main_rts['probe']) > 1 and len(all_main_rts['irrelevant']) > 1:
        dcit = (mean(all_main_rts['probe']) - mean(all_main_rts['irrelevant'])) / std(all_main_rts['irrelevant'])
        if dcit > 0.2:
            end_feed = '\n\nBezüglich Ihrer Ergebnisse: Ihre Reaktionszeit war für die Namen ' + ', '.join( task_probes ).upper() + ' signifikant langsamer als für andere Namen. Also vermuten wir, dass das Ihr richtiger Name ist.'
        else:
            end_feed = '\n\nBezüglich Ihrer Ergebnisse: Ihre Reaktionszeit war für die Namen ' + ', '.join( task_probes ).upper() + ' nicht signifikant langsamer als für andere Namen. Also vermuten wir, dass das nicht Ihr Name ist.'
    else:
        dcit = '-'
        end_feed = ''
    info = 'Danke für die Teilnahme. Wenn Sie möchten, können Sie gehen, aber bitte seien Sie leise dabei.\n\nKurze Information über den Test:\n\nIn dieser Studie versuchen wir, Ihre wirklichen selbstbezogenen Details (z.B. Ihren tatsächlichen Vornamen) von solchen zu unterscheiden, die Ihnen nicht zugehörig sind (z.B. andere Vornamen). Ziel dieses Tests ist es, anhand von Reaktionszeiten herauszufinden, wenn eine Person versucht, bestimmte Daten zu verschleiern bzw. zu verheimlichen. Dies geschieht auf Basis der Vermutung, dass Reaktionszeiten für die Ihnen präsentierten eigenen Namen langsamer ausfallen, als im Falle anderer Namen. Hauptanliegen dieser Studie ist es, zu zeigen, ob dies besser mit der Aufforderung zu einer möglichst schnellen Reaktion oder zu einer möglichst genauen Reaktion funktioniert.' + end_feed + '\n\nFür weitere Informationen wenden Sie sich bitte an den Versuchsleiter (oder schreiben Sie eine E-mail an Gaspar Lukacs).'

    data_out.write(dems + "/" +
      "/".join( [ str(nmbr) for nmbr in
      [practice_repeated['block1'],
      practice_repeated['block2'],
      practice_repeated['block3'],
      full_duration,
      dcit] ] ) +
      "\n")
    data_out.close()
    show_instruction( info )

def set_screen(): # screen properties
    global win, start_text, left_label, right_label, center_disp, instruction_page
    win = Window([1280, 1000], color='Black', fullscr = 1, units = 'pix', allowGUI = True) # 1280 1024
    start_text = TextStim(win, color=instruction_color, font='Verdana', text = u'Um anzufangen, bitte die Leertaste drücken.', pos = [0,-300], height=35, bold = True, wrapWidth= 1100)
    left_label = TextStim(win, color='white', font='Verdana', text = 'unvertraut', pos = [-350,-160], height=35, alignHoriz='center')
    right_label = TextStim(win, color='white', font='Verdana', text = 'vertraut', pos = [350,-160], height=35, alignHoriz='center')
    center_disp = TextStim(win, color='white', font='Arial', text = '', height = 60)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, font='Verdana', color = instruction_color)


def task_instructions( whichtext = ''):
    keys_info = 'Während des Tests sehen Sie Wörter in der Mitte des Bildschirms auftauchen. Sie müssen jedes Wort entweder mit der linken oder mit der rechten Antworttaste kategorisieren. Diese Tasten sind ' + key_pair['always']['descr'] + '. '
    main_item_info = ' Kategorisieren Sie die folgenden Namen als vertraut mit der rechten Taste: ' + ', '.join(the_targets[0]).upper() + "\n\nKategorisieren Sie alle anderen Namen als unvertraut mit der linken Taste. (Diese andere Namen sind: " + ', '.join(the_main_items[0]).upper() + ". Zur Erinnerung: Sie leugnen, irgendwelche der anderen Namen als relevant für Sie wahrzunehmen, also drücken Sie für alle diese die linke Taste.)"
    if whichtext == 'targetcheck':
        return probe_crime_text + main_item_info
    elif whichtext == 'firstblock':
        return keys_info + '\n\nEs werden drei kurze Übungsrunden stattfinden. In der ersten Runde müssen Sie Ausdrücke kategorisieren, die mit Vertrautheit zu tun haben. '
    elif block_num > 1:
        return  keys_info + '\n\nDie restlichen Items sind Vor- und Nachnamen.' + main_item_info + '\n\nHinweis: achten Sie nur auf die Begriffe die mit der rechten Taste kategorisiert werden müssen (' + ', '.join(the_targets).upper() + ') und drücken Sie für alles andere die linke Taste.'
    else:
        return  keys_info

def set_block_info():
    global block_info, block_num, incorrect, tooslow, move_on
    move_on = '\n\nUm weiterzugehen, drücken Sie die Leertaste.\n\nFalls nötig, drücken Sie die Taste ENTER (oder eine der Pfeiltasten) um die vollständigen Anweisungen erneut zu lesen.'
    block_info = [""]
    target_reminder = [
        "Zur Erinnerung: der als vertraut zu kategorisierende Name ist " +
        targets_guilty[1].upper() +
        ". ",
        "Zur Erinnerung: der als vertraut zu kategorisierende Name ist " +
        targets_guilty[1].upper() +
        ". ",
        ]


    block_info.append( task_instructions('firstblock') + '\n\nUm weiterzugehen, drücken Sie die Leertaste.')

    block_info.append('Nun, in dieser zweiten Übungsrunde wollen wir herausfinden, ob Sie die Aufgabe genau verstanden haben. Um sicherzustellen, dass Sie Ihre jeweiligen Antworten richtig kategorisieren, werden Sie für diese Aufgabe genügend Zeit haben. Sie müssen auf jedes Item korrekt antworten. Wählen Sie eine nicht korrekte Antwort (oder geben keine Antwort für mehr als 10 Sekunden ein), müssen Sie diese Übungsrunde wiederholen.'  + target_reminder[0] + "\n" + move_on)

    block_info.append('Sie haben die zweite Übungsrunde geschafft. Nun folgt die dritte und letzte Übungsrunde. In dieser dritten Übungsrunde wird die Antwortzeit verkürzt sein. Eine bestimmte Anzahl an falschen Antworten ist aber erlaubt. Die Wörter (Angaben) "unvertraut", "vertraut" werden nicht mehr angezeigt, die Aufgabe bleibt jedoch dieselbe. \n\n ' + move_on)

    block_info.append("Gut gemacht. Nun beginnt der eigentliche Test. Die Aufgabe bleibt dieselbe. Es wird zwei Blöcke, getrennt durch eine Pause, geben." +
      target_reminder[0] + "\n" + move_on)

    block_info.append(
      "Der erste Block ist nun beendet. Im zweiten Block wird weiter getestet. " +
      target_reminder[1] +
      "Abgesehen davon bleibt die Aufgabe dieselbe.\n" + move_on)

    block_info.append(
      'Nun beginnt der zweite Teil des Tests.\n\n Wie im vorherigen Durchgang drücken Sie  die Tasten ' + key_pair['always']['descr'] + '.\n' +
      "Es folgen erneut zwei Blöcke, getrennt durch eine Pause." +
      target_reminder[0] +
      "\n" + move_on)

    block_info.append(
      "In diesem letzten Block wird nochmals die Kategorie getestet. " +
      target_reminder[0] +
      " \n\n" + move_on)

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
        true_probes = {categories[0]: probes_guilty[0],  categories[1]: probes_guilty[1], categories[2] : probes_guilty[2], categories[3] : probes_guilty[3], categories[4]: probes_guilty[4], categories[5]: probes_guilty[5] }
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

noneword = 'Keine'
def prune():
    global items_to_filt

def item_selection():
    global w_selected
    prune()
    w_selected = {}

def trm(raw_inp):
    return [w for w in raw_inp.replace(',', ' ').split(' ') if w != ''][:2]

def target_check_guilty():
    show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Items gründlich auswendig gelernt haben.\n\n' + target_guilty_list)
    itm_count_guilty = 0
    if testing == True:
        tc_count_guilty = 17
    else:
        tc_count_guilty = 0
    while itm_count_guilty <= 5 and tc_count_guilty <= 17:
        targets_guilty_tc = [u"Frank Moser", u"Grüner Hut", u"Operation Schwein", u"Schnee Akte", u"Schiff Pläne", u"Barsch Straße"]
        instr_display =  TextStim(win, color=instruction_color, font='Verdana', text = u'Bitte geben Sie im Folgenden die korrekte Antwort ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Verdana', text = 'Geben Sie ' + training_recall_item[itm_count_guilty] + ' ein:', pos=(-100, 0), alignHoriz = 'right', height=35)
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
        if typedin_words == targets_guilty_tc[itm_count_guilty] or typedin_words[0] == "PASS":
            itm_count_guilty += 1
            tc_count_guilty += 1
            show_instruction("Richtig! Leertaste drücken, um fortzufahren.")
            if tc_count_guilty == 6 or tc_count_guilty == 12:
                itm_count_guilty = 0
        else:
            instruction_page.setText('Falsch. Lesen Sie bitte die Instruktionen nochmals!')
            instruction_page.draw()
            win.flip()
            wait(2)
            if testing == True:
                itm_count_guilty = itm_count_guilty
                tc_count_guilty = tc_count_guilty
            else:
                itm_count_guilty = 0
                tc_count_guilty = 0
                show_instruction('Bitte lernen Sie die folgenden Items auswendig, der Abfragetest startet von vorne:\n\n' + target_guilty_list)


def target_check_innocent():
    global targets_innocent
    show_instruction('Drücken Sie die Leertaste, wenn Sie die unten stehenden Items gründlich auswendig gelernt haben.\n\n' + target_innocent_list)
    target_innocent_z = 0
    if testing == True:
        target_innocent_y = 17
    else:
        target_innocent_y = 0
    while target_innocent_z <= 5 and target_innocent_y <= 17:
        instr_display =  TextStim(win, color=instruction_color, font='Verdana', text = u'Bitte geben Sie im Folgenden die korrekte Antwort ein, drücken Sie dann ENTER.', pos=(0, 150), height=30, wrapWidth=1100, colorSpace='rgb')
        input_prompt =  TextStim(win, color=instruction_color, font='Verdana', text = 'Geben Sie ' + training_recall_item[target_innocent_z] + ' ein:', pos=(-100, 0), alignHoriz = 'right', height=35)
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
        if typedin == targets_innocent[target_innocent_z] or typedin_words[0] == "PASS":
            target_innocent_z += 1
            target_innocent_y += 1
            show_instruction("Richtig! Leertaste drücken, um fortzufahren.")
            if target_innocent_y == 6 or target_innocent_y == 12:
                target_innocent_z = 0
        else:
            instruction_page.setText('Falsch. Lesen Sie bitte die Instruktionen nochmals!')
            instruction_page.draw()
            win.flip()
            wait(2)
            target_innocent_z = 0
            target_innocent_y = 0
            show_instruction('Bitte lernen Sie die folgenden Items auswendig, der Abfragetest startet von vorne:\n\n' + target_innocent_list)


def create_item_base():
    global blcks_base, stims_base, the_targets, the_main_items, task_probes
    stim_base_tmp = {}
    the_targets = []
    task_probes = []
    the_main_items = []
    if blocks_cit == 0:
        the_targets.append((targets_guilty)*3)
        task_probes.append((probes_guilty)*3)
        the_main_items.append((irrelevants_guilty)*3 + (probes_guilty)*3)
    else:
        the_targets.append((targets_innocent)*3)
        task_probes.append((probes_innocent)*3)
        the_main_items.append((irrelevants_guilty)*3 + (probes_innocent)*3)
    the_main_items.sort()
    stim_base = shuffle(the_targets  + the_main_items)


def main_items():
    global blcks_base, crrnt_phase
    print('main_items()')
    crrnt_phase = 'main'
    block_stim_base = blcks_base.pop(0)
    main_stims = block_stim_base
    return [dct for sublist in main_stims for dct in sublist] # flatten

def rndmz_details(block_stim_base):
    item_order=[]
    prev_last = '' # prev order is the item order of the previous trial sequence
    for i in range(0,18):# each i represents a sequence of 6 trials
        item_order_temp = deepcopy(block_stim_base) # create a temporary item order, this represents the item order WITHIN one trial sequence
        shuffle(item_order_temp) # shuffle this
        while prev_last == item_order_temp[0]: # if the last one of the previous block is the first of this one
            shuffle(item_order_temp) # reshuffle
        item_order.append(deepcopy(item_order_temp)) # make this the item order for this trial sequence
        prev_last = item_order_temp[-1]
    return item_order


def practice_items():
    print('practice_items()')
    blck_itms_temp = []
    if blocks_cit == 0:
        blck_itms_temp += deepcopy(targets_guilty[0] + str(irrelevants_guilty[0:3]) + probes_guilty[0])
    else:
        blck_itms_temp += deepcopy(stims_base[categories[1]])
    shuffle(blck_itms_temp) # shuffle it, why not
    # below the pseudorandomization to avoid close repetition of similar items (same item type)
    safecount = 0 # just to not freeze the app if sth goes wrong
    stim_dicts_f = [] # in here the final list of dictionary items is collected, one by one
    while len(blck_itms_temp) > 0: # stop if all items from blck_itms_temp were use up (added to stim_dicts_f and removed with pop() )
        dict_item = blck_itms_temp[0] # assign first dictionary item as separate variable; for easier access below
        safecount += 1
        if safecount > 911:
            print('break due to unfeasable safecount')
            break
        good_indexes = [] # will collect the indexes where the dict item may be inserted
        dummy_dict = [{ 'word': '-', 'item_type': '-' }] # dummy dict to the end; if the item is to be inserted to the end, there is no following dict that could cause an unwanted repetition
        for f_index, f_item in enumerate(stim_dicts_f + dummy_dict): # check all potential indexes for insertion in the stim_dicts_f as it is so far (plus 1 place at the end)
            #if dict_item['item_type'] in diginto_dict(stim_dicts_f, f_index, 'item_type', 1): # checks whether there is preceding or following identical item_type around the potential index (see diginto_dict function)
             #   continue # if there is, continue without adding the index as good index
            good_indexes.append(f_index) # if did not continue above, do add as good index
        if len(good_indexes) == 0: # if by chance no good indexes found, print notification and reshuffle the items
            print('no good_indexes - count', safecount) # this should normally happen max couple of times
            blck_itms_temp.insert( len(blck_itms_temp), blck_itms_temp.pop(0) ) # move first element to last, and let's hope next first item is luckier and has place
        else: # if there are good places, choose one randomly, insert the new item, and remove it from blck_itms_temp
            stim_dicts_f.insert( choice(good_indexes) , blck_itms_temp.pop(0))
    return stim_dicts_f # return final list (for blck_items var assignment)



def diginto_dict(dct, indx, key_name, min_dstnc):
    if indx - min_dstnc < 0: # if starting index is negative, it counts from the end of the list; thats no good
        strt = 0 # so if negative, we just set it to 0
    else:
        strt = indx - min_dstnc # if not negative, it can remain the same
    return [ d[key_name] for d in dct[ strt : indx+min_dstnc ] ] # return all values for the specified dict key within the specified distance (from the specified dictionary)



def basic_variables():
    global stopwatch, blocks_order, guilt, block_num, all_main_rts, kb_device, practice_repeated, firsttime
    stopwatch = Clock()
    guilt = 1 # always guilty
    #if condition in [5,6,7,8,10,12]:
    #    guilt = 1
    #else:
    #    guilt = 0
    if condition % 2 != 0 and condition < 3: # maybe improve this, confusing?
        blocks_cit = 0
    elif condition % 2 == 0 and condition < 3:
        blocks_cit = 1
    elif condition & 2 != 0 and condition >= 3:
        blocks_cit = 2
    elif condition & 2 == 0 and condition >= 3:
        blocks_cit = 3
     ## CONDITIONS:
        # use condition nos. for control vs. experimental group
        # plus for guilty vs innocent block first
        # 1 (0) : exp + guilty first
        # 2 (1) : exp + inno first
        # 3 (2) : control + guilty first
        # 4 (3) : control + inno first
    block_num = 0
    all_main_rts = { 'probe' : [], 'irrelevant': [] }
    practice_repeated = { 'block1' : 0, 'block2': 0, 'block3': 0}
    firsttime = True
    io = launchHubServer()
    kb_device = io.devices.keyboard

# create output file, begin writing, reset parameters
def create_file():
    global data_out
    f_name = 'exp_ecit_keys_' + str(condition) + "_" + "_" + str(guilt) + "_ord" + "_" + subj_id + '.txt'
    data_out=open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "condition", "width", "phase", "block_number", "trial_number", "stimulus_shown", "category", "stim_type", "response_key", "rt_start", "incorrect", "too_slow", "press_duration", "isi", "date_in_ms" ] ) + "\n" )
    print("File created:", f_name)

def str_if_num( num_val ):
    if isinstance(num_val, str) or isinstance(num_val, unicode):
        return num_val
    else:
        return str( num_val*1000 )

def add_resp():
    global incorrect, tooslow
    data_out.write( '\t'.join( [ subj_id, str(condition), crrnt_instr, crrnt_phase, str(block_num), str(trial_num+1), stim_text, stim_current["categ"], stim_type, resp_key, str_if_num(rt_start), str(incorrect), str(tooslow), str_if_num(press_dur), str_if_num( isi_min_max[0]/1000 + isi_delay ), str(strftime("%Y%m%d%H%M%S", gmtime())) ] ) + '\n' )
    print("resp key:", resp_key, "for stim:", stim_text, "incorrect:", incorrect, "rt_start:", rt_start)

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

def draw_labels():
    if block_num <= 2:
        left_label.draw()
        right_label.draw()

def assign_keys():
    global targetkey, nontargetkey
    targetkey = key_pair['always']['target']
    nontargetkey = key_pair['always']['nontarg']

def next_block():
    global ddline, block_num, rt_data_dict, crrnt_instr, blck_itms, firsttime, crrnt_phase
    if block_num <= 2:
        crrnt_phase = 'practice'
        if block_num == 0:
            rt_data_dict = {}
            assign_keys()
        if ( block_num in (0, 1, 2) ):
            if block_num == 0 or practice_eval():
                block_num+=1
            if block_num == 1:
                if blocks_cit == 0:
                    if condition == 1 or condition == 2:
                        cit_warning_text()
                    target_check_guilty()
                    firsttime = False
                elif blocks_cit == 1:
                    target_check_innocent()
                blck_itms = practice_items()
                ddline = 10
            elif block_num == 2:
                blck_itms = practice_items()
                ddline = main_ddline
            else:
                blck_itms = main_items()
        else:
            block_num+=1
            if block_num == 4:
                if blocks_cit == 0:
                    target_check_innocent()
                elif blocks_cit == 1:
                    target_check_guilty()
                assign_keys()
                blck_itms = main_items()
            else:
                blck_itms = main_items()
        if testing == True:
            blck_itms = blck_itms[0:5]
        run_block()

def practice_eval():
    global rt_data_dict
    is_valid = True
    if first_wrong == True:
        is_valid = False
    elif block_num != 2:
        types_failed = []
        if block_num == 1:
            min_ratio = 0.8
        else:
            min_ratio = 0.6
        for it_type in rt_data_dict:
            it_type_feed_dict = { #'targetref': "sich auf Vertrautheit beziehende Ausdrücke",
        #'nontargref': "sich auf Unvertrautheit beziehende Ausdrücke",
        'main_item': "als unvertraut zu kategorisierende Namen",
        'target': "als vertraut zu kategorisierende Namen" }
            rts_correct = [ rt_item for rt_item in rt_data_dict[it_type] if rt_item > 0.15 ]
            corr_ratio = len( rts_correct )/ len( rt_data_dict[it_type] )
            if corr_ratio < min_ratio:
              is_valid = False
              types_failed.append(
                " " +
                it_type_feed_dict[it_type] +
                " (" + str( int( corr_ratio // 0.01 ) ) +
                "% correct)"
              )
            if is_valid == False:
                block_info[block_num] = "Sie müssen diese Übungsrunde wiederholen, da Sie zu wenige richtige Antworten gegeben haben.\n\nSie benötigen mindestens " + str( int(min_ratio*100) ) + "% richtige Antworten für jeden der Antworttypen, jedoch gaben Sie nicht genügend richtige Antworten für folgende(n) Antworttyp(en):" + ", ".join(types_failed) +  ".\n\nBitte geben Sie genaue und im Zeitlimit liegende Antworten.\n\nMachen Sie sich keine Sorgen, wenn Sie diese Übungsrunde mehrmals wiederholen müssen." + move_on
    if is_valid == False:
        practice_repeated['block' + str(block_num)] += 1
    rt_data_dict = {}
    return is_valid

def show_instruction(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    inst_resp = waitKeys(keyList = ['space', escape_key])
    end_on_esc(inst_resp[0])

def show_block_instr():
    instruction_page.setText( block_info[block_num] )
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    show_again = ['left', 'up', 'right', 'down','return']
    inst_resp = waitKeys( keyList = [ 'space', escape_key ] + show_again )
    end_on_esc( inst_resp[0] )
    if inst_resp[0] in show_again:
        show_instruction( task_instructions() + '\n\nUm weiterzugehen, drücken Sie die Leertaste.' )
        show_block_instr()

def run_block():
    global block_num, trial_num, stim_current, stim_text, stim_type, incorrect, tooslow, first_wrong, show_feed, ddline, isi_delay, resp_key, rt_start, press_dur
    show_block_instr()
    first_wrong = False
    print("len(blck_itms):", len(blck_itms))
    start_with_space()
    for trial_num in range(len(blck_itms)): # go through all stimuli of current block
        print("------- Trial number:", trial_num, "In block:", block_num, "C:", condition, "ord:", blocks_order)
        stim_current = blck_itms[trial_num]
        incorrect = 0
        tooslow = 0
        stim_type = stim_current['item_type']
        stim_text = stim_current["word"]
        isi_delay = randint(1, isi_min_max[1]-isi_min_max[0]) / 1000
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
                if stim_type in ("target"): #, "targetref"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
                    show_false()
            elif resp_key == nontargetkey:
                if stim_type[:10] in ("probe","irrelevant"): #, "nontargref"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
                    show_false()
        draw_labels()
        win.flip()
        wait(isi_min_max[0]/1000)
        press_dur = '-' # remains this if none found, or not with correct key
        for ke in kb_device.getReleases(): # get io keypress events for duration
            try:
                if ke.key == resp_key: # if matches the pygame key, should be fine
                    press_dur = ke.duration # store io keypress duration
            except Exception:
                pass
            break
        add_resp() # store trial data
        if block_num == 2: # check if comprehension check has to be repeated
            if (incorrect+tooslow) > 0:
                first_wrong = True
                break
        else:
            collect_rts()
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

def show_false():
    center_disp.text = 'Falsch!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(0.5)
    center_disp.color = 'white'
def show_tooslow():
    center_disp.text = 'Zu langsam!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(0.5)
    center_disp.color = 'white'


# end session
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



# EXECUTE
execute()
