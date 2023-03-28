from tkinter import *

import GUI2_LOGIN_SCREEN as login_gui
import GUI2_REGISTER_SCREEN as register_gui
import GUI_UTILS as utilities


def sign_in():
    login_gui.main()


def sign_up():
    register_gui.main()


window = Tk()
window.title('Welcome Screen')
window.config(padx=24, pady=24)

# WELCOME FRAME
welcome_label_frame = LabelFrame(
    master=window,
    text=' Welcome To ',
    font=(utilities.FONT_NAME, 16, 'bold'),
    fg=utilities.PRIMARY_COLOR,
    pady=24,
    padx=12,
)
welcome_label_frame.grid(row=0)

welcome_label = Label(
    master=welcome_label_frame,
    text='FIREBASE CLASSROOM',
    font=(utilities.FONT_NAME, 50, 'bold'),
    padx=24,
    pady=12,
    fg=utilities.PRIMARY_COLOR
)
welcome_label.grid(row=0, pady=16)

# AUTHENTICATE FRAME
auth_label_frame = LabelFrame(
    master=window,
    text=' Authenticate ',
    font=(utilities.FONT_NAME, 16, 'bold'),
    fg=utilities.PRIMARY_COLOR,
    pady=24,
    padx=12
)
auth_label_frame.grid(row=1, pady=16)

# Ask user : if he/she is user => 'login' else 'register' as new user
ask_user_login_label = Label(
    master=auth_label_frame,
    text='Are you a Registered User? ',
    font=(utilities.FONT_NAME, 24, 'bold'),
    padx=24,
    pady=12,
    fg=utilities.PRIMARY_COLOR
)
# since it is not possible to justify the content / align content like 'Label or Entry widget' in a grid system , when placing the item in the grid along with specifying the 'row,column kwargs' , we can also specify kwarg => sticky and give 'w - west , e, n, s' as value and make those particular element stick to a given side.
ask_user_login_label.grid(row=0, column=0, sticky=W)

# Login Button
login_user = Button(
    master=auth_label_frame,
    text='Sign In',
    font=(utilities.FONT_NAME, 24, 'bold'),
    padx=12,
    pady=6,
    fg=utilities.PRIMARY_COLOR,
    activeforeground=utilities.COLOR_WHITE,
    command=sign_in
)
login_user.grid(row=0, column=1)

ask_user_label_register = Label(
    master=auth_label_frame,
    text='Not a Registered User? ',
    font=(utilities.FONT_NAME, 24, 'bold'),
    padx=24,
    pady=12,
    fg=utilities.PRIMARY_COLOR
)
# placing this 'Label' in grid() and making it stick to the 'WEST' of grid()
ask_user_label_register.grid(row=1, column=0, sticky=W)

# Register Button
register_user = Button(
    master=auth_label_frame,
    text='Sign Up',
    font=(utilities.FONT_NAME, 24, 'bold'),
    padx=12,
    pady=6,
    fg=utilities.PRIMARY_COLOR,
    activeforeground=utilities.PRIMARY_COLOR,
    command=sign_up
)
register_user.grid(row=1, column=1)

window.mainloop()
