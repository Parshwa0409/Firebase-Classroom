from tkinter import *
from tkinter import messagebox
import GUI_UTILS as utilities
from firebase_setup import pyrebase_auth
import DB_REALTIME as realtime_db
import GUI3_STUDENT_SCREEN as student_gui
import GUI3_TEACHER_SCREEN as teacher_gui
import re
import requests
import json


# TODO : Clear fields after the operation
def main():
    # Enclosing all the function's and UI under one_func : 'main()'
    # Function To Validate

    def validate(user_email: str, user_password: str):
        email_check = True
        password_check = True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, user_email):
            messagebox.showerror(
                title="Invalid Email",
                message="The given Email-Address is invalid.\n\nVALID FORMAT : username@mail.com"
            )
            email_check = False
        elif not user_password:
            messagebox.showerror(
                title="Password Not Specified",
                message="Please enter your Password."
            )
            password_check = False
        return email_check and password_check

    # Function To SignIn Using PYREBASE
    def pyrebase_login(email: str, password: str):
        auth = pyrebase_auth
        user_record = auth.sign_in_with_email_and_password(email=email, password=password)
        """
        # Either store the returned value , a dictionary with signed-in user_details ... and grab the required data using key
        # SAMPLE OUTPUT => {'kind': 'identitytoolkit#VerifyPasswordResponse', 'localId': '1nh20cs151', 'email': 'parshwapatil9@gmail.com', 'displayName': 'parshwa b patil', 'idToken': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjIxZTZjMGM2YjRlMzA5NTI0N2MwNjgwMDAwZTFiNDMxODIzODZkNTAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoicGFyc2h3YSBiIHBhdGlsIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2Zpci1jbGFzc3Jvb20tZDM2ODgiLCJhdWQiOiJmaXItY2xhc3Nyb29tLWQzNjg4IiwiYXV0aF90aW1lIjoxNjYzOTA5NTUzLCJ1c2VyX2lkIjoiMW5oMjBjczE1MSIsInN1YiI6IjFuaDIwY3MxNTEiLCJpYXQiOjE2NjM5MDk1NTMsImV4cCI6MTY2MzkxMzE1MywiZW1haWwiOiJwYXJzaHdhcGF0aWw5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfbnVtYmVyIjoiKzkxODE5NzQ2Mjk4OCIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsicGhvbmUiOlsiKzkxODE5NzQ2Mjk4OCJdLCJlbWFpbCI6WyJwYXJzaHdhcGF0aWw5QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.dD1DaKGQJgnWtfodFutdytVDbOca8IosYKuAjL0oqjJhav20Ex172xvtltKVR4eukD32sYdddLGjiKvns8ZOkQLYk8hbSMYxA7X8IMnMof0zaTWyhdC9nvkWzI2Fa71uj2A7fMdAywJFSVCywQvbZTyeU7pRpzGPKnLgWmVTCutVAyLSW0edH73ADW2EOAwwjgpuTVpgqYvjdFfoLsISRW-9UUR9rsDmO7Ae9vA5mTTj4tbdKdF3-LjF74vU-Af6IrBdfJ0NTuJ9RqpGkrBZrO29J1p_Z2jLhiBA9Ucww4EsaU5dnoUy6784ZmwdLjOwA__37PPYSKb84_-xFl8Gfg', 'registered': True, 'refreshToken': 'AOEOulZiAmkwW3pUxmWveKwc4x6toFBFjasi0WwSFvajwZeNQWnPJT7jsbISaQu6YMSvTOHdlYeDMEwuvIlq_-u7LZ3d2_PigUG74226eOt9dhoRna-nvfbm4uZkzhRECs1kMZEmlnCFi46pA7OMv-zC42ynVWIvOyb0VME0oHQelA8z--vaQnSmNX3wH5e5IuLYhj1-mAtirDprAqbLnFuQMcxc3qVafSdAZlcCKTI5xfkROGoLHts', 'expiresIn': '3600'}
        # print(user_record['displayName'].title()) # print(user_record['email'])
        """
        # OR ELIF, login/sign-in successful => tap into current_user attribute, and we get the same details as mentioned above.
        current_user = auth.current_user


    def sign_in():
        user_email = email_entry.get().strip()
        user_password = password_entry.get().strip()
        validation_check = validate(user_email=user_email, user_password=user_password)
        admin = designation_value.get()
        if validation_check:
            try:
                # Get user info from db, if found continue login ,else error.
                user_details = realtime_db.get_details_by_email(email=user_email, admin=admin)
                # print(user_details)
                if user_details:
                    pyrebase_login(email=user_email, password=user_password)
                    email_entry.delete(0, END)
                    password_entry.delete(0, END)
                    if admin:
                        teacher_gui.main(user_dict=user_details)
                    else:
                        student_gui.main(user_dict=user_details)
                else:
                    messagebox.showerror(
                        title="SIGN-IN ERROR",
                        message=f"SIGN-IN ERROR : USER DETAILS NOT FOUND IN RECORDS."
                    )
            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error_message = json.loads(error_json)['error']['message']
                messagebox.showerror(
                    title="SIGN-IN ERROR",
                    message=f"SIGN-IN ERROR : {str(error_message).replace('_', ' ')}"
                )

    login_window = Toplevel()
    login_window.title('Sign-In With Email & Password')
    login_window.config(padx=24, pady=24)

    # LoginFrame
    login_frame = LabelFrame(
        master=login_window,
        text=' Sign In ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        pady=24,
        padx=22,
        fg=utilities.PRIMARY_COLOR,
    )
    login_frame.grid(row=0, pady=16)

    login_title_label = Label(
        master=login_frame,
        text='Sign In With Email & Password',
        font=(utilities.FONT_NAME, 36, 'bold'),
        padx=64,
        pady=12,
        fg=utilities.PRIMARY_COLOR,
    )
    login_title_label.grid(row=0, column=0)

    # User Details Frame
    user_details_frame = LabelFrame(
        master=login_window,
        text=' User Details ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        padx=12,
        fg=utilities.PRIMARY_COLOR,
    )
    user_details_frame.grid(row=1, pady=16)

    # Email Row (Label + Entry)
    email_label = Label(
        master=user_details_frame,
        text='Enter your registered Email-ID : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    email_label.grid(row=0, column=0, sticky=W)  # W = tKinter built-in constant for 'w'-west

    email_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    email_entry.grid(row=0, column=1, sticky=E)

    # Password Row (Label + Entry)
    password_label = Label(
        master=user_details_frame,
        text='Enter your Password : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    password_label.grid(row=1, column=0, sticky=W)

    password_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30,
        show='*'
    )
    password_entry.grid(row=1, column=1, sticky=E)

    designation_label = Label(
        master=user_details_frame,
        text='Are you a Student/Teacher : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    designation_label.grid(row=3, column=0, sticky=W, rowspan=2)

    print_value = lambda: print(designation_value.get())

    # designation_dict = {'Student': False, 'Teacher': True}
    designation_value = BooleanVar()
    designation_value = BooleanVar()
    Radiobutton(
        master=user_details_frame,
        text='Student',
        font=(utilities.FONT_NAME, 18),
        fg=utilities.PRIMARY_COLOR,
        variable=designation_value,
        value=False,
        # command=print_value
    ).grid(row=3, column=1, sticky=W)
    Radiobutton(
        master=user_details_frame,
        text='Teacher',
        font=(utilities.FONT_NAME, 18),
        fg=utilities.PRIMARY_COLOR,
        variable=designation_value,
        value=True,
        # command=print_value
    ).grid(row=4, column=1, sticky=W)
    # for key, val in designation_dict.items():
    #     Radiobutton(
    #         master=user_details_frame,
    #         text=key,
    #         font=(utilities.FONT_NAME, 18),
    #         fg=utilities.PRIMARY_COLOR,
    #         variable=designation_value,
    #         value=val,
    #         command=print_value
    #     ).grid(row=3 + index, column=1, sticky=W)
    #     index += 1

    # SignIn Button
    login_user_button = Button(
        master=user_details_frame,
        text='Sign In',
        font=(utilities.FONT_NAME, 24, 'bold'),
        padx=12,
        pady=6,
        fg=utilities.PRIMARY_COLOR,
        activeforeground=utilities.COLOR_WHITE,
        command=sign_in,
    )
    login_user_button.grid(row=5, column=0, columnspan=3, pady=32)
    login_window.mainloop()


if __name__ == '__main__':
    main()
