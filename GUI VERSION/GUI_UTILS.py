import darkdetect

FONT_NAME = 'Courier'
COLOR_WHITE = '#F9F9F9'
if darkdetect.isLight():
    PRIMARY_COLOR = '#645CAA'  # PURPLE
else:
    PRIMARY_COLOR = "#AEFEFF"  # "#B9FFF8"TEAL
COLOR_LIGHT_BLACK = "#686D76"
COLOR_BLACK = "#072227"


"""
pyrebase exception =>   class : type(error/exception) => requests.exceptions.HTTPError
                        solution_link : https://stackoverflow.com/questions/43725448/httperror-handling-python3-firebase-db

"""