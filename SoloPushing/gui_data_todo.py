width_height = '595x335'
color1 = '#E7E8D8'
color2 = '#f1dfb6'
color3 = '#ffd09b'
color4 = '#ffba91'
green_color_for_text = '#474838'

color_for_button = '#7fd1ae'
color_for_button2 = '#e6b9cb'
color_for_button3 = '#d2a538'
color_for_button4 = '#b6dbce'
color_for_button5 = '#ccb49a'
color_text_slightly_red = '#bf5748'
color_text_slightly_green = '#00755d'
font_style = "Helvetica"
font_style1 = "Courier"
#relief=tk.RIDGE

matching_dark1 = '#1b3d2f'
matching_dark2 = '#55433b'

#
jp_quiz_background = '#aca9bb'
jp_quiz_match = '#d3d3d3'
jp_quiz_dark_text = '#474554'
jp_quiz_match2 = '#80a498'

#Timer Colors
timer_color1 = '#e6f4f1'
timer_color2 = '#e9fdfd'
timer_color3 = '#00aaae'
timer_color4 = '#00acad'
timer_color5 = '#95f7b2'

timer_color_darker1 = '#324b4b'
timer_color_darker2 = '#975739'

color = [color2, jp_quiz_background, timer_color1]
matching_color = [color1, jp_quiz_match, timer_color1]


def center_text(item, width):
    spaces_needed = (width - len(item)) // 2
    centered_item = ' ' * spaces_needed + item
    return centered_item


def levels_definer(seconds):
    if seconds >= 86400:
        return "Hero"  # Level 10
    elif seconds >= 69120:
        return "Legend"  # Level 9
    elif seconds >= 60480:
        return "Grandmaster"  # Level 8
    elif seconds >= 51840:
        return "Master"  # Level 7
    elif seconds >= 43200:
        return "Expert"  # Level 6
    elif seconds >= 34560:
        return "Adept"  # Level 5
    elif seconds >= 25920:
        return "Journeyman"  # Level 4
    elif seconds >= 17280:
        return "Apprentice"  # Level 3
    elif seconds >= 8640:
        return "Novice"  # Level 2
    else:
        return "Beginner"  # Level 1
