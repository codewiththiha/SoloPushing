import random
import tkinter as tk
from ToDo_DB import *
from gui_data_todo import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import Menu
import pygame
import google.generativeai as genai
# import os
from ai_prompts import *

#new discovery listbox.size() can also capture the length of listboxes without len()


#___________________________________THE ToDo Logic__________________________________
def is_window_active(top_level):
    return window.winfo_viewable()


sort_mode = 0


def sort_mode_memory(mode):
    global sort_mode
    sort_mode = mode


def on_left_click(event):
    try:
        if is_window_active(top_level_menu.top):
            top_level_menu.top.destroy()
    except Exception:
        pass


def on_right_click(event):
    global challenge_task, exist_task
    task_index = listbox.curselection()
    task_data = listbox.get(task_index)
    if exist_task == 0:
        challenge_task = task_data
    #(task_data)
    current_tab_index = notebook.index("current")
    active_status = return_active_status(task_data)
    #(type(current_tab_index))
    if active_status == 0 and current_tab_index == 0 and task_index:
        top_level_menu(task_data)

    elif active_status == 1 and current_tab_index == 0 and task_index:
        start_challenges(task_data, event)


def top_level_menu(task_data):
    try:
        if is_window_active(top_level_menu.top):
            top_level_menu.top.destroy()
    except Exception as e:
        pass
    top_level_menu.top = tk.Toplevel()
    top_level_menu.top.overrideredirect(True)
    top_level_menu.top.title('Menu_121')
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    top_level_menu.top.geometry(f"120x100+{x-30}+{y-20}")
    label_challenge = tk.Label(top_level_menu.top,
                               text='Set Challenge',
                               font=('Arial', 9, 'bold'),
                               bg=color2)
    label_challenge.pack(pady=2)
    scale_challenge = tk.Scale(top_level_menu.top,
                               from_=5,
                               to=45,
                               orient=tk.HORIZONTAL,
                               troughcolor=jp_quiz_dark_text,
                               bd=0,
                               highlightthickness=0)

    top_level_menu.top.config(background=color2)
    scale_challenge.config(background=color2)
    scale_challenge.pack(pady=(0, 8))
    challenge_button = tk.Button(
        top_level_menu.top,
        text='Set',
        bg=color1,
        width=6,
        relief=tk.RIDGE,
        command=lambda:
        (challenge_minute_defines(scale_challenge.get() * 60, task_data),
         update_active_status(task_data, 1), top_level_menu.top.destroy()))
    challenge_button.pack()


exist_task = 0


def start_button_functions():
    global remaining_time, type_mode_globe, timerrunning, exist_task, challenge_task
    notebook.select(tab3)
    label_music_status.config(text=f'You are working on {challenge_task}')
    if exist_task == 1:
        exist_task = 0
    if timerrunning:
        tab3.after_cancel(cancel_id)
    if pause_status == 1:
        pause_resume()
    elif type_mode_globe == 'normal':
        remaining_time = 0
    else:
        return


def start_challenges(task_name, event):
    popup_menu = tk.Menu(window, tearoff=0)
    popup_menu.add_command(
        label="Start",
        command=lambda:
        (start_button_functions(), challenge_level_start(task_name)))
    popup_menu.tk_popup(event.x_root, event.y_root)


def challenge_minute_defines(seconds, task_name):
    update_remaining_time(
        task_name,
        seconds,
    )


challenge_task = None


def challenge_level_start(task_name):
    global remain_challenge
    remain_time = return_remaining_time(task_name)
    #(f'Remaining time: {remain_time}')
    remain_challenge = remain_time
    timer('challenge', task_name)


def update_score():
    todo_score = listbox.size()
    todo_count_label.config(text=f'ToDo: {todo_score}')
    completed_score = completed_listbox.size()
    completed_count_label.config(text=f'Done: {completed_score}')


def load_to_gui(status, sort_status=None):
    listbox.delete(0, tk.END)
    raw = read_tasks(status, sort_status)
    for task in raw:
        listbox.insert(tk.END, task)


def load_to_gui_completed(status, sort_status=None):
    completed_listbox.delete(0, tk.END)
    raw = read_tasks(status, sort_status)
    for task in raw:
        completed_listbox.insert(tk.END, task)


def add_task():
    sort_mode_list = ["A-Z", "Z-A", "New-Old", "Old-New"]
    task = entry.get()
    if task == '':
        messagebox.showinfo('Attention', 'Please input something')
    elif task != "":
        create_task(task, 'create')
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        load_to_gui("tasks", sort_mode_list[sort_mode])
        load_to_gui_completed("completed_tasks", sort_mode_list[sort_mode])


def remove_task():
    task_index = listbox.curselection()
    completed_task_index = completed_listbox.curselection()
    if task_index:
        task_data = listbox.get(task_index)
        delete_tasks(task_data, 'create')
        listbox.delete(task_index)

    elif completed_task_index:
        completed_task_data = completed_listbox.get(completed_task_index)
        delete_tasks(completed_task_data, 'completed')
        completed_listbox.delete(completed_task_index)
    else:
        messagebox.showinfo('Attention', 'You didn\'t select anything!!')


def info_message():
    remain = return_remaining_time(challenge_task)
    info_message.top = tk.Toplevel()
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    info_message.top.geometry(f"300x160+{x-250}+{y+10}")
    info_message.top.title('Information')
    info_message.top.wm_attributes('-toolwindow', True)
    label_info = tk.Label(
        info_message.top,
        text=
        f'''Remaining time: {round(remain/60,2)} minutes. You can complete the task only after completing the challenge.''',
        wraplength=200)
    label_info.pack(pady=(30, 25))
    info_message.top.config(background=color2)
    button_ok = tk.Button(info_message.top,
                          text='OK',
                          command=destroy_info,
                          width=8,
                          relief=tk.RIDGE,
                          bg=color2)
    button_ok.pack()
    label_info.config(background=color2)


def destroy_info():
    info_message.top.destroy()


def completed_task_mark():
    global challenge_task, exist_task
    active = return_active_status(challenge_task)
    # print(f'active:{active}')

    if exist_task == 1:
        exist_task = 0
        task_index = listbox.curselection()
        task_data = listbox.get(task_index)
        active = return_active_status(task_data)
        exist_task = 1
    if active == 1:
        info_message()
        return
    selected_index = listbox.curselection()
    #(f'selected_index:{selected_index}')

    if not selected_index:
        messagebox.showinfo('Attention', 'You didn\'t select anything!!')
        return

    transfer_task = listbox.get(selected_index)

    listbox.delete(selected_index)
    delete_tasks(transfer_task, status="create")
    create_task(transfer_task, 'uncheck')

    try:
        raw = read_tasks(type_UC='completed_tasks')
        completed_listbox.delete(0, tk.END)
        for task in raw:
            completed_listbox.insert(tk.END, task)
    except:
        raw = read_tasks(type_UC='completed_tasks')
        for task in raw:
            completed_listbox.insert(tk.END, task)
        #('here')


def uncheck_task_mark():
    transfer_task_index = completed_listbox.curselection()
    if not transfer_task_index:
        messagebox.showinfo('Attention', 'You didn\'t select anything!!')
        return

    else:
        transfer_task = completed_listbox.get(transfer_task_index)
        completed_listbox.delete(transfer_task_index)
        #(f'here{transfer_task}')
        delete_tasks(transfer_task, status="completed")
        create_task(transfer_task, 'create')
        load_to_gui('tasks')


def hover_to_detect_todo(event):
    global challenge_task, exist_task
    # try:
    #     if is_window_active(top_level_menu.top):
    #         top_level_menu.top.destroy()
    # except Exception:
    #     pass
    transfer_task_index = completed_listbox.curselection()
    todo_task_index = listbox.curselection()

    if transfer_task_index:
        uncheck_button.config(state='normal')
        complete_button.config(state='disabled')
    if todo_task_index:
        task_data = listbox.get(todo_task_index)
        if exist_task == 0:
            challenge_task = task_data
        complete_button.config(state='normal')
        uncheck_button.config(state='disabled')


#___________________________________THE Japan Quiz Logic__________________________________


# Load questions from the text file
def load_questions(file_path, limit):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')  # return with list
            if len(parts) == 5:
                question, choice1, choice2, choice3, correct = parts
                questions.append(
                    (question, choice1, choice2, choice3, correct))
                if len(questions) == limit:
                    break
    return questions


def get_text():
    questions = []
    choice = return_radio_choice()
    print(choice)
    if choice == "Eng":
        quiz_prompt_defined = quiz_prompt_eng
    elif choice == "MM":
        quiz_prompt_defined = quiz_prompt_mm
        print('here')
    input_data = advanced_questions.text_box.get(1.0, tk.END)
    advanced_questions.text_box.delete(1.0, tk.END)
    genai.configure(api_key='AIzaSyDsam761rs_86Xi8ijblMJbJGE1iq_SoNo')

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""{input_data}{quiz_prompt_defined}""")
    f = response.text
    with open('Japan_Quiz_data//default_questions.txt', 'w',
              encoding='utf-8') as default:
        default.write(f)


    # for line in f:
    #     parts = line.strip().split(';')  # return with list
    #     if len(parts) == 5:
    #         question, choice1, choice2, choice3, correct = parts
    #         questions.append((question, choice1, choice2, choice3, correct))
    #         #(questions)
    # return questions
def return_radio_choice():
    choice = advanced_questions.choice.get()
    return choice


def advanced_questions():
    global questions
    current_tab_index = notebook.index("current")
    questions.clear()
    top = tk.Toplevel()
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    advanced_questions.choice = tk.StringVar(value="Eng")
    frame_radio = tk.Frame(top, bg=color[current_tab_index])
    radio_eng = tk.Radiobutton(frame_radio,
                               text="Eng",
                               variable=advanced_questions.choice,
                               value="Eng",
                               background=color[current_tab_index])

    radio_mm = tk.Radiobutton(frame_radio,
                              text="MM",
                              variable=advanced_questions.choice,
                              value="MM",
                              background=color[current_tab_index])
    top.title("Advanced Questions")
    top.geometry(f"254x260+{x-130}+{y-70}")
    top.resizable(False, False)
    top.config(background=color[current_tab_index])
    advanced_questions.text_box = tk.Text(
        top, height=10, width=25, bg=matching_color[current_tab_index]
    )  # Set height and width for more space
    advanced_questions.text_box.pack(pady=(22, 0))
    button_submit = tk.Button(top,
                              text="Submit",
                              command=lambda:
                              (get_text(), top.destroy(),
                               quiz_initiate_advance(), notebook.select(tab2)),
                              bg=matching_color[current_tab_index])
    button_submit.pack(side="left", padx=30)

    frame_radio.pack(pady=10, side="right", padx=10, fill='both', expand=True)

    frame_radio.config(width=400, height=500)
    radio_eng.pack(side="left", padx=(10, 0))
    radio_mm.pack(side="right", padx=(0, 13))


# Shuffle questions for a new round
def reset_quiz():
    global score, current_question, questions
    score = 0
    next_btn.config(state='normal')
    random.shuffle(questions)  # Randomize questions
    current_question = 0
    update_score_jpn()
    display_question(current_question)


def hover_to_update(event):
    quiz_type = open_adjust_menu.options_listbox.get(tk.ACTIVE)
    with open(f'Japan_Quiz_Data\\{quiz_type}.txt', 'r',
              encoding='utf-8') as length:
        length_data = length.readlines()
    open_adjust_menu.scale.config(to=len(length_data))


def open_adjust_menu():
    current_tab_index = notebook.index("current")
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    top = tk.Toplevel(tab2)
    top.title("Options")
    top.wm_attributes('-toolwindow', True)  # make the title bar disappear
    top.geometry(f"254x230+{x-130}+{y-60}")
    top.resizable(False, False)
    top.config(background=color[current_tab_index])
    #Listbox for Choices
    options = [
        "Verbs", "Nouns", "Adjectives", "Hiragana", "Katakana", "dai 10 ga"
    ]
    open_adjust_menu.options_listbox = tk.Listbox(
        top,
        height=3,
        bg=matching_color[current_tab_index],
        fg='black',
        font=(font_style1, 8),
        highlightthickness=2,
        bd=0)
    for option in options:
        open_adjust_menu.options_listbox.insert(tk.END, option)
    open_adjust_menu.options_listbox.pack(pady=20)
    #Label
    Label1 = tk.Label(top,
                      text='Limit The Number Of Quiz',
                      bg=color[current_tab_index])
    Label1.pack()
    #Scale
    open_adjust_menu.scale = tk.Scale(
        top,
        from_=5,
        to=5,
        orient="horizontal",
        resolution=1,
        bd=0,
        bg=color[current_tab_index],
        troughcolor=jp_quiz_dark_text,
        highlightthickness=0  # Removes the white focus border
    )

    open_adjust_menu.scale.pack(pady=10)
    #button
    quiz_now_button = tk.Button(
        top,
        text='Quiz Now',
        command=lambda:
        (quiz_initiate(), top.destroy(), notebook.select(tab2)),
        relief=tk.RIDGE,
        bg=matching_color[current_tab_index])
    quiz_now_button.pack(pady=20)
    open_adjust_menu.options_listbox.bind("<Motion>", hover_to_update)


def quiz_initiate():
    global questions, current_question
    questions.clear()
    current_question = 0
    quiz_type = open_adjust_menu.options_listbox.get(tk.ACTIVE)
    quiz_limit = int(open_adjust_menu.scale.get())
    questions = load_questions(f'Japan_Quiz_Data\\{quiz_type}.txt', quiz_limit)
    display_question(current_question)
    reset_quiz()


def quiz_initiate_advance():
    global questions, current_question
    questions.clear()
    current_question = 0
    questions = load_questions('Japan_Quiz_Data\\default_questions.txt', None)
    display_question(current_question)
    reset_quiz()


# Function to check the answer
def check_answer(selected, correct, btns):
    global score
    for btn in btns:
        btn.config(state='disabled')  # Disable all buttons after answering
        if btn['text'] == correct:
            btn.config(bg='lightgreen')  # Correct answer in green
        elif btn['text'] == selected:
            btn.config(bg='red')  # Wrong answer in red
    if selected == correct:
        score += 1
    update_score_jpn()


def game_over():
    messagebox.showinfo("Quiz Completed",
                        f"Your final score is {score}/{len(questions)}")
    next_btn.config(state='disabled')


# Function to move to the next question
def next_question():
    global current_question
    current_question += 1
    if current_question < len(questions):
        display_question(current_question)
    else:
        game_over()


#Update the score display
def update_score_jpn():
    jp_score_label.config(text=f"Score: {score}/{len(questions)}")
    if current_question < len(questions):
        answered.config(text=f'Question No: {current_question+1}')
    elif current_question == len(questions):
        answered.config(text=f'Question No: {current_question}')


# Function to display the current question
def display_question(index):
    question, choice1, choice2, choice3, correct = questions[index]
    question_label.config(text=question)
    # Reset button colors and enable them
    for btn in [btn1, btn2, btn3]:
        btn.config(state='normal', bg='lightgray')

    #to shuffle
    choices = [choice1, choice2, choice3]
    random.shuffle(choices)
    shuffled_choices = []
    for choice in choices:
        shuffled_choices.append(choice)

    # Update the buttons with choices and their commands
    btn1.config(text=shuffled_choices[0],
                command=lambda: check_answer(shuffled_choices[0], correct,
                                             [btn1, btn2, btn3]))
    btn2.config(text=shuffled_choices[1],
                command=lambda: check_answer(shuffled_choices[1], correct,
                                             [btn1, btn2, btn3]))
    btn3.config(text=shuffled_choices[2],
                command=lambda: check_answer(shuffled_choices[2], correct,
                                             [btn1, btn2, btn3]))


#__________________________________Timer Logic________________________________________
def set_button_second():
    global type_mode_globe
    timer('normal')
    type_mode_globe = 'normal'


def revoke_status_for_set():
    global play_button_clicked, challenge_task, type_mode_globe
    if type_mode_globe == 'normal':
        quote = random.choice(quotes_related_with_study_and_music)
    elif type_mode_globe == 'challenge':
        quote = f'You are working on {challenge_task}'
    label_music_status.config(text=quote)


def timer(type, task_name=None):
    global remaining_time, timerrunning, cancel_id, challenge_task, type_mode_globe, exist_task
    timerrunning = False

    if cancel_id:
        tab3.after_cancel(cancel_id)
        cancel_id = None

    if not timerrunning:
        try:
            # if timer_detect == 1 and remaining_time == 0:  #1 mean challenge mode
            #     messagebox.showinfo("Fact", "Will you cancel the challenge??")
            if type == 'normal':
                remaining_time = int(scale_set.get()) * 60
                #(remaining_time)
            elif type == 'challenge':
                remaining_time_challenge = return_remaining_time(task_name)
                #(f'Challenge Mode: {remaining_time} seconds')
        except ValueError:
            #("Please enter a valid time in minutes.")
            return
    #(scale_set.get())
    timerrunning = True

    if type == 'challenge':
        if exist_task == 0:
            challenge_task = task_name
        #('here')
        #(task_name)
        type_mode_globe = 'challenge'
        countdown(type)

    elif type == 'normal':
        exist_task = 0
        type_mode_globe = 'normal'
        countdown(type)


type_mode_globe = 'normal'


def spent_time():
    global spent_time_data
    with open('spent_time.txt', 'w') as to_input:
        to_input.write(f'{spent_time_data}')


with open('spent_time.txt', 'r') as output:
    spent_time_data = int(output.readline())


def spent_time_status():
    global spent_time_data
    current_tab_index = notebook.index("current")
    minutes = int(spent_time_data / 60)
    level_name = levels_definer(spent_time_data)
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    spent_time_top_level = tk.Toplevel(window, bg=(color[current_tab_index]))
    spent_time_top_level.geometry(f"254x260+{x-30}+{y-20}")
    spent_time_top_level.resizable(False, False)
    spent_time_top_level.title("Your Score")
    spent_time_label = tk.Label(
        spent_time_top_level,
        text=f"You had spent {minutes} minutes and your level is {level_name}",
        bg=(color[current_tab_index]),
        font=(font_style1, 10, 'bold'),
        wraplength=180)

    spent_time_label.pack(pady=100)


timer_detect = 0


def countdown(type_mode):
    global remaining_time, timer_detect, timerrunning, cancel_id, spent_time_data, challenge_task, type_mode_globe, exist_task
    #('remaining_time', remaining_time)
    if type_mode_globe == 'challenge':
        remain_time = return_remaining_time(challenge_task)
        timer_detect = 1
        exist_task = 1
    elif type_mode_globe == 'normal':
        remain_time = remaining_time
    if remain_time > 0 and timerrunning:
        minutes = remain_time // 60
        seconds = remain_time % 60
        label_timer.config(text=f"{minutes:02}:{seconds:02}")
        spent_time_data += 1  #need to fix
        if type_mode_globe == 'challenge':
            remain_time -= 1
            update_remaining_time(challenge_task, remain_time)
        elif type_mode_globe == 'normal':
            remaining_time -= 1
        #('remaining_time', remain_time)

        cancel_id = tab3.after(1000, lambda: countdown(type_mode_globe))
    elif remain_time == 0 and timerrunning:
        pygame.mixer.music.load("song_effect\\Time_up.mp3")

        label_timer.config(text='00:00')
        pygame.mixer.music.play()  #fix need
        messagebox.showinfo('Attention',
                            'Congrats you have completed the challenge')
        timerrunning = False
        cancel_id = None
        if type_mode_globe == 'challenge':
            update_active_status(challenge_task, 0)
            update_remaining_time(challenge_task, 0)
            timer_detect = 0
            challenge_task = None
            type_mode_globe = None
            exist_task = 0

    # if remaining_time > 0 and timerrunning:
    #     minutes = remaining_time // 60
    #     seconds = remaining_time % 60
    #     label_timer.config(text=f"{minutes:02}:{seconds:02}")
    #     spent_time_data += 1
    #     spent_time()
    #     remaining_time -= 1
    #     #(challenge_task)
    #     update_remaining_time(challenge_task, remaining_time)
    #     cancel_id = tab3.after(1000, countdown)
    # elif remaining_time == 0 and timerrunning:
    #     pygame.mixer.music.load("song_effect\\Time_up.mp3")
    #     label_timer.config(text='00:00')
    #     pygame.mixer.music.play()
    #     messagebox.showinfo('Attention', 'Time Up')
    #     timerrunning = False
    #     cancel_id = None


def pause_resume(
):  #you can just simply use cancel id to pause without interpreting the timerrunning
    global timerrunning, pause_status, cancel_id, type_mode_globe, timer_detect
    if timer_detect == 1:
        remaining_time = return_remaining_time(challenge_task)
    if remaining_time == 0 and timer_detect == 0:
        messagebox.showinfo('Attention', 'Please set the alarm first')
    elif pause_status == 0:
        # timerrunning = False
        button_pause.config(text="Resume")
        pause_status = 1
        button_set.config(state='disabled')
        play_button.config(state='disabled')
        tab3.after_cancel(cancel_id)
        pygame.mixer.music.pause()
        return
    elif pause_status == 1 and remaining_time > 0:
        # timerrunning = True
        countdown(type_mode_globe)
        button_pause.config(text="Pause")
        button_set.config(state='normal')
        play_button.config(state='normal')
        pause_status = 0
        pygame.mixer.music.unpause()


def activated_music_play_button():
    global play_button_clicked, challenge_task, type_mode_globe
    if type_mode_globe == 'normal':
        quote = random.choice(quotes_related_with_study_and_music)
    elif type_mode_globe == 'challenge':
        quote = f'You are working on {challenge_task}'
    play_button_clicked += 1
    to_play_song = songs_listbox.get(tk.ACTIVE)
    # to catch 1st click and 2nd click of play button
    if play_button_clicked % 2 == 1:
        play_button.config(text='Stop')
        play_specific_music_file(to_play_song)
    elif play_button_clicked % 2 == 0:
        play_button.config(text='Play')
        pygame.mixer.music.stop()
        label_music_status.config(text=quote)


def play_specific_music_file(song):
    global type_mode_globe, challenge_task
    if type_mode_globe == 'challenge':
        label_music_status.config(text=f'You are working on {challenge_task}')
    else:
        label_music_status.config(text=(f'Playing: {song}'))
    pygame.mixer.music.load(f"music_files\\{song}.mp3")
    pygame.mixer.music.play()


#_________to fix potential error while closing
def on_closing():
    # This function handles the close event
    window.quit()  # Stops the mainloop
    window.destroy()  # Destroys the window


# _______________________________Main Gui__________________
# The main window
window = tk.Tk()

#Menu Bar
menu_bar = Menu(window)
# adjust_menu = Menu(menu_bar, tearoff=0)
# quiz_menu = Menu(adjust_menu, tearoff=0)

# menu_bar.add_cascade(label="More", menu=quiz_menu)
# menu_bar.add_cascade(label="Adjust", menu=quiz_menu)
# quiz_menu.add_command(label="Manual", command=lambda: open_adjust_menu())
# quiz_menu.add_command(label="Your Score", command=lambda: spent_time_status())
window.config(menu=menu_bar)

#___________________Todo-Menu_____________________

main_menu1 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="ToDo", menu=main_menu1)
main_menu1.add_command(label="Score", command=lambda: spent_time_status())
sub_menu1 = Menu(main_menu1, tearoff=0)
main_menu1.add_cascade(label="Sort todo", menu=sub_menu1)
sub_menu1.add_command(
    label="A-Z",
    command=lambda:
    (load_to_gui("tasks", "A-Z"),
     load_to_gui_completed("completed_tasks", "A-Z"), sort_mode_memory(0)))
sub_menu1.add_command(
    label="Z-A",
    command=lambda:
    (load_to_gui("tasks", "Z-A"),
     load_to_gui_completed("completed_tasks", "Z-A"), sort_mode_memory(1)))
sub_menu1.add_command(
    label="New-Old",
    command=lambda:
    (load_to_gui("tasks", "New-Old"),
     load_to_gui_completed("completed_tasks", "New-Old"), sort_mode_memory(2)))
sub_menu1.add_command(
    label="Old-New",
    command=lambda:
    (load_to_gui("tasks", "Old-New"),
     load_to_gui_completed("completed_tasks", "Old-New"), sort_mode_memory(3)))
#___________________Quiz Menu_____________________
sub_menu2 = Menu(main_menu1, tearoff=0)
main_menu1.add_cascade(label="Quiz-Initialize", menu=sub_menu2)
sub_menu2.add_command(label="Integrated", command=lambda: open_adjust_menu())
sub_menu2.add_command(label="Advanced", command=lambda: advanced_questions())

#___________________Menu_____________________

window.protocol("WM_DELETE_WINDOW",
                on_closing)  #catches X (close) command at title bar
window.title("Solo Pushing")
window.geometry(width_height)
window.resizable(False, False)
style = ttk.Style()
style.configure('Custom1.TFrame', background=color2)
style.configure('Custom2.TFrame', background=jp_quiz_background)
style.configure('Custom3.TFrame', background=timer_color1)
# Create a Notebook widget (the tabbed interface)
notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")

# Create frames for each tab
tab1 = ttk.Frame(notebook, style='Custom1.TFrame')
tab2 = ttk.Frame(notebook, style='Custom2.TFrame')
tab3 = ttk.Frame(notebook, style='Custom3.TFrame')

# Add frames as tabs in the notebook
notebook.add(tab1, text="ToDo")
notebook.add(tab2, text="Jp Quiz")
notebook.add(tab3, text="Pomodoro Timer")

#__________________________TODO GUI START______________________________

# Entry box
entry = tk.Entry(tab1, width=30, font=(font_style, 12), bg=color1)
entry.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Button Frame
button_frame = tk.Frame(tab1, bg=color2)  # Matches the background
button_frame.grid(row=0, column=3, columnspan=4, padx=5, pady=10)

# Add Button
add_button = tk.Button(button_frame,
                       text="Add",
                       command=lambda: (add_task(), update_score()),
                       bg=color_for_button,
                       fg="white",
                       relief=tk.RIDGE,
                       width=6,
                       font=(font_style, 10))
add_button.pack(side=tk.LEFT, padx=5)

# Complete Button
complete_button = tk.Button(button_frame,
                            text="Done",
                            command=lambda:
                            (completed_task_mark(), update_score()),
                            bg=color_for_button2,
                            relief=tk.RIDGE,
                            fg="white",
                            width=6,
                            font=(font_style, 10))
complete_button.pack(side=tk.LEFT, padx=5)

# Uncheck Button
uncheck_button = tk.Button(button_frame,
                           text="Uncheck",
                           command=lambda:
                           (uncheck_task_mark(), update_score()),
                           relief=tk.RIDGE,
                           bg=color_for_button3,
                           fg="white",
                           width=6,
                           font=(font_style, 10))
uncheck_button.pack(side=tk.LEFT, padx=5)

# Remove Button
remove_button = tk.Button(button_frame,
                          text="Remove",
                          command=lambda: (remove_task(), update_score()),
                          relief=tk.RIDGE,
                          bg=color_for_button3,
                          fg="white",
                          width=6,
                          font=(font_style, 10))
remove_button.pack(side=tk.LEFT, padx=5)
complete_button.config(state='disabled')
uncheck_button.config(state='disabled')

# Listbox for Todo Tasks
todo_frame = tk.Frame(tab1, bg=color3)
todo_frame.grid(row=1, column=0, columnspan=3, rowspan=3, padx=10, pady=10)
todo_label = tk.Label(todo_frame,
                      text="Todo",
                      fg="white",
                      bg=color3,
                      font=(font_style, 16, "bold"))
todo_label.pack(pady=5)
listbox = tk.Listbox(todo_frame,
                     height=8,
                     width=30,
                     font=(font_style, 12),
                     fg=color_text_slightly_red,
                     bg=color3)
listbox.pack()

# Listbox for Completed Tasks
completed_frame = tk.Frame(tab1, bg=color4)
completed_frame.grid(row=1,
                     column=3,
                     columnspan=3,
                     rowspan=3,
                     padx=10,
                     pady=10)
completed_label = tk.Label(completed_frame,
                           text="Done",
                           fg="white",
                           bg=color4,
                           font=(font_style, 16, "bold"))
completed_label.pack(pady=5)
completed_listbox = tk.Listbox(completed_frame,
                               height=8,
                               width=30,
                               font=(font_style, 12),
                               fg=color_text_slightly_green,
                               bg=color4)
completed_listbox.pack()
listbox.bind("<Motion>", hover_to_detect_todo)
completed_listbox.bind("<Motion>", hover_to_detect_todo)

# Status Labels
todo_count_label = tk.Label(tab1,
                            text="To do: 5",
                            bg=color2,
                            fg=color_text_slightly_red,
                            font=(font_style1, 10))
todo_count_label.grid(row=4,
                      column=0,
                      columnspan=3,
                      pady=(10),
                      sticky="w",
                      padx=3)

completed_count_label = tk.Label(tab1,
                                 text="Complete: 6",
                                 bg=color2,
                                 fg=color_text_slightly_green,
                                 font=(font_style1, 10))
completed_count_label.grid(row=4,
                           column=3,
                           columnspan=3,
                           pady=(10),
                           padx=4,
                           sticky="e")

# Load data
load_to_gui('tasks')
load_to_gui_completed('completed_tasks')
update_score()

#__________________________JP Quiz Start_______________________________

# Initialize quiz data
questions = load_questions('Japan_Quiz_Data\\default_questions.txt', None)
score = 0
current_question = 0

# Score and question number
header_frame = tk.Frame(tab2, bg=jp_quiz_background)
header_frame.grid(row=0, column=0, columnspan=3, pady=(10, 90))

answered = tk.Label(header_frame,
                    text="Question No: 1",
                    bg=jp_quiz_background,
                    font=(font_style1, 10))
answered.grid(row=0, column=0, padx=(20, 10))

jp_score_label = tk.Label(header_frame,
                          text="Score: 0/0",
                          font=(font_style1, 10),
                          bg=jp_quiz_background)
jp_score_label.grid(row=0, column=1, padx=10)

# Question label
question_label = tk.Label(tab2,
                          text="",
                          font=(None, 20, 'bold'),
                          wraplength=550,
                          bg=jp_quiz_background)
question_label.grid(row=0, column=0, columnspan=6, pady=(50, 20))

# Frame for answer buttons
btn_frame = tk.Frame(tab2, bg=jp_quiz_background)
btn_frame.grid(row=2, column=0, columnspan=6, padx=55)

# Answer choice buttons
btn1 = tk.Button(btn_frame,
                 width=15,
                 font=(font_style, 12),
                 relief=tk.RIDGE,
                 takefocus=False)
btn1.grid(row=1, column=0, padx=10, pady=5)

btn2 = tk.Button(btn_frame,
                 width=15,
                 font=(font_style, 12),
                 relief=tk.RIDGE,
                 takefocus=False)
btn2.grid(row=1, column=2, padx=10, pady=5)

btn3 = tk.Button(btn_frame,
                 width=15,
                 font=(font_style, 12),
                 relief=tk.RIDGE,
                 takefocus=False)
btn3.grid(row=1, column=4, padx=10, pady=5)

# Frame for Next and Reset buttons
nav_frame = tk.Frame(tab2, bg=jp_quiz_background)
nav_frame.grid(row=3, column=0, columnspan=9, pady=80)

# Next and Reset buttons
next_btn = tk.Button(nav_frame,
                     text="Next",
                     font=("Arial", 10),
                     width=12,
                     bg=color_for_button4,
                     relief=tk.RIDGE,
                     command=lambda: (next_question(), update_score_jpn()),
                     takefocus=False)
next_btn.grid(row=0, column=0, padx=80)

reset_btn = tk.Button(nav_frame,
                      text="Reset",
                      font=("Arial", 10),
                      width=12,
                      bg=color_for_button4,
                      relief=tk.RIDGE,
                      command=reset_quiz,
                      takefocus=False)
reset_btn.grid(row=0, column=1, padx=90)

display_question(current_question)
update_score_jpn()

#______________________________Timer Gui_____________________________________

quotes_related_with_study_and_music = [
    "Music makes studying enjoyable.", "Tunes can boost your focus.",
    "Studying flows with the rhythm.", "Music is fuel for the mind.",
    "A good song makes study easier.", "Notes inspire focused learning.",
    "Music turns pages with ease.", "Studying is smoother with melody.",
    "Beats can sharpen concentration.", "Songs add joy to study hours.",
    "Music helps thoughts stay clear.", "A soundtrack for each study hour.",
    "Studying feels lighter with music.", "Melodies lift study spirits high.",
    "Rhythms help thoughts flow well.", "Music helps ideas take root.",
    "Study deepens with a soft tune.", "Notes bring calm to learning.",
    "Music enriches the study mood.", "A melody makes knowledge grow."
]


def return_quote():
    global type_mode_globe, challenge_task
    if type_mode_globe == 'challenge':
        return f'You are working on {challenge_task}'
    elif type_mode_globe == 'normal':
        random_quote_related_with_study_and_music = random.choice(
            quotes_related_with_study_and_music)
        return random_quote_related_with_study_and_music


play_button_clicked = 0
pygame.mixer.init()  #initialize music player

timerrunning = False
remaining_time = 0
cancel_id = None  #to avoid overlap while using multiple time
pause_status = 0
# Create frame_right
frame_right = tk.Frame(tab3, width=250, bg=timer_color1)
frame_right.grid(column=0, row=0, padx=(0, 0), pady=0, sticky="nsew")

label_timer = tk.Label(frame_right,
                       text='00:00',
                       font=(font_style1, 40, 'bold'),
                       bg=timer_color1,
                       fg=timer_color_darker1)
label_timer.pack(padx=60, pady=(60, 30))

scale_set = tk.Scale(frame_right,
                     orient='horizontal',
                     to=45,
                     from_=5,
                     resolution=5,
                     length=160,
                     bd=0,
                     troughcolor=timer_color_darker1,
                     highlightthickness=0,
                     bg=timer_color1)
scale_set.pack(pady=20)

# entry_set = tk.Entry(frame_right, width=26)
# entry_set.pack(pady=20)

# Create Right_Sub_Frame
right_sub_frame = tk.Frame(frame_right, bg=timer_color1)
right_sub_frame.pack(pady=20)
button_set = tk.Button(right_sub_frame,
                       text='Set',
                       width=7,
                       command=lambda:
                       (timer('normal'), revoke_status_for_set()),
                       relief=tk.RIDGE,
                       bg=timer_color1,
                       takefocus=False,
                       fg=timer_color_darker1)
button_set.pack(side='left', padx=(0, 20))
button_pause = tk.Button(right_sub_frame,
                         text='Pause',
                         width=7,
                         command=pause_resume,
                         relief=tk.RIDGE,
                         bg=timer_color1,
                         takefocus=False,
                         fg=timer_color_darker1)
button_pause.pack(side='right', padx=(20, 0))

# Create frame_left
frame_left = tk.Frame(tab3, width=250, bg=timer_color1)
frame_left.grid(column=1, row=0, padx=(0, 0), pady=10, sticky="nsew")

# Add Listbox
songs_listbox = tk.Listbox(frame_left,
                           height=4,
                           bg=timer_color2,
                           fg=timer_color_darker1,
                           font=(font_style, 10))
songs_listbox.pack(pady=(55, 30), padx=90)
play_button = tk.Button(frame_left,
                        text='Play',
                        width=8,
                        command=lambda: (activated_music_play_button()),
                        relief=tk.RIDGE,
                        bg=timer_color2,
                        takefocus=False,
                        fg=timer_color_darker1)
play_button.pack(pady=(25, 10))
label_music_status = tk.Label(frame_left,
                              text=return_quote(),
                              bg=timer_color1,
                              fg=timer_color_darker1,
                              font=(font_style, 9, 'bold'),
                              wraplength=200)
label_music_status.pack(pady=20)

#Insert Music
music_list = ["Anime Lofi", "Coffee Lofi ☕", "Game Lofi", "Nintendo Music"]

for music in music_list:
    songs_listbox.insert(tk.END, music)

listbox.bind("<Button-3>", on_right_click)
listbox.bind("<Button-1>", on_left_click)
window.mainloop()

#pygame.mixer.music.get_busy():
#Return True if playing(busy) and false if not
