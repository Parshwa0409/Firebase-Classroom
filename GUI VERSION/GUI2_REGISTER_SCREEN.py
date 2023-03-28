import re
from tkinter import *
from tkinter import messagebox
from firebase_admin.exceptions import FirebaseError
import DB_CLOUD_FIRESTORE as cloud_db
import DB_REALTIME as realtime_db
import GUI_UTILS as utilities
from firebase_setup import firebase_auth
import GUI2_LOGIN_SCREEN as login_gui


# TODO : Clear fields after the operation
def main():
    # KEY NAME
    NAME_KEY = 'name'
    PHONE_NUM_KEY = 'phone_number'
    EMAIL_KEY = 'email'
    UNIQUE_ID_KEY = 'unique_id'
    ADMIN_KEY = 'admin'

    def check_invalid_email(user_email: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, user_email):
            # IF THE EMAIL IS INVALID RETURN TRUE
            return True

    def check_if_not_empty(username: str, user_ph_num: str, user_email: str, user_password: str,user_confirm_password: str,usn_entry: str, admin: bool):
        # RETURN TRUE IF EVEN ONE FIELD IS EMPTY
        if admin:
            if not (username and user_ph_num and user_email and user_password and user_confirm_password):
                return True
        else:
            if not (username and user_ph_num and user_email and user_password and user_confirm_password and usn_entry):
                return True

    def check_confirm_password():
        if password_entry.get().strip() == confirm_password_entry.get().strip():
            # IF BOTH PASSWORD MATH RETURN TRUE
            return True

    def valid_phone_number():
        phone_num = phone_num_entry.get().strip()
        if len(phone_num) > 9 and phone_num.isnumeric():
            return True

    def check_admin():
        if designation_value.get():
            student_usn_entry.delete(0, END)
            student_usn_entry.configure(state=DISABLED)
        else:
            student_usn_entry.configure(state=NORMAL)

    def register_new_user(username, user_ph_num, user_email, user_password, student_usn, admin_info):
        user_record = firebase_auth.create_user(
            email=user_email,
            password=user_password,
            display_name=username,
            phone_number='+91' + user_ph_num
        )
        user_dict = {
            NAME_KEY: username.lower(),
            PHONE_NUM_KEY: user_ph_num,
            EMAIL_KEY: user_email,
            ADMIN_KEY: admin_info,
            UNIQUE_ID_KEY: student_usn
        }
        return user_dict

    def sign_up():
        username = username_entry.get().strip()
        user_ph_num = phone_num_entry.get().strip()
        user_email = email_entry.get().strip()
        user_password = password_entry.get().strip()
        user_confirm_password = confirm_password_entry.get().strip()
        student_usn = student_usn_entry.get().strip().lower()
        admin_info = True if designation_value.get() else False

        # Rather than showing message in method , we can show it here......
        if check_if_not_empty(username, user_ph_num, user_email, user_password, user_confirm_password, student_usn,admin_info):
            messagebox.showwarning(
                title="Oops",
                message="Please make sure if you haven't left any field empty."
            )
        elif check_invalid_email(user_email=user_email):
            messagebox.showwarning(
                title="Invalid Email",
                message="The given Email-Address is invalid.\n\nVALID FORMAT : username@mail.com"
            )
        elif not valid_phone_number():
            messagebox.showwarning(
                title="Oops",
                message="Please make sure the Phone Number is valid."
            )
        elif not check_confirm_password():
            messagebox.showwarning(
                title="Oops",
                message="Please make sure the Password's match."
            )
        else:
            try:
                user_dict = register_new_user(username, user_ph_num, user_email, user_password, student_usn, admin_info)
                realtime_db.register_user_db(admin=admin_info, user_data=user_dict)
                cloud_db.register_user_cloud_firestore(admin=admin_info, user_data=user_dict)
                # register_window.destroy()
                login_gui.main()
            except FirebaseError as e:
                messagebox.showwarning(
                    title="Oops",
                    message=f"{e}"
                )

    # ------------------------------------------------------------------------------------------------------------GUI WINDOW
    register_window = Toplevel()
    register_window.title('Register As A New User')
    register_window.config(padx=24, pady=24)

    # ---------------------------------------------------------------------------------------------------------RegisterFrame
    register_frame = LabelFrame(
        master=register_window,
        text=' Sign Up ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        pady=24,
        padx=22,
        fg=utilities.PRIMARY_COLOR,
    )
    register_frame.grid(row=0, pady=16)

    register_title_label = Label(
        master=register_frame,
        text='Enter Your Details & Get Started',
        font=(utilities.FONT_NAME, 34, 'bold'),
        padx=24,
        pady=12,
        fg=utilities.PRIMARY_COLOR,
    )
    register_title_label.grid(row=0)

    # -----------------------------------------------------------------------------------------------------UserDetails Frame
    user_details_frame = LabelFrame(
        master=register_window,
        text=' User Details ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        padx=12,
        fg=utilities.PRIMARY_COLOR,
    )
    user_details_frame.grid(row=1, pady=16)

    # -----------------------------------------------------------------------------------Name Row (Label + Entry) => ROW = 0
    username_label = Label(
        master=user_details_frame,
        text='Enter your Full Name : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    username_label.grid(row=0, column=0, sticky=W)

    username_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    username_entry.grid(row=0, column=1, sticky=E)

    # ----------------------------------------------------------------------------PhoneNumber Row (Label + Entry) => ROW = 1
    phone_num_label = Label(
        master=user_details_frame,
        text='Enter your Phone Number : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    phone_num_label.grid(row=1, column=0, sticky=W)

    phone_num_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    phone_num_entry.grid(row=1, column=1, sticky=E)

    # ----------------------------------------------------------------------------------Email Row (Label + Entry) => ROW = 2
    email_label = Label(
        master=user_details_frame,
        text='Enter your Email-ID : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    email_label.grid(row=2, column=0, sticky=W)

    email_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    email_entry.grid(row=2, column=1, sticky=E)

    # -------------------------------------------------------------------------------Password Row (Label + Entry) => ROW = 3
    password_label = Label(
        master=user_details_frame,
        text='Enter your Password : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    password_label.grid(row=3, column=0, sticky=W)

    password_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30,
        show='*'
    )
    password_entry.grid(row=3, column=1, sticky=E)

    # -----------------------------------------------------------------------Confirm Password Row (Label + Entry) => ROW = 4
    confirm_password_label = Label(
        master=user_details_frame,
        text='Confirm your Password : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    confirm_password_label.grid(row=4, column=0, sticky=W)

    confirm_password_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30,
        show='*'
    )
    confirm_password_entry.grid(row=4, column=1, sticky=E)

    # -------------------------Designation Row (Label + RadioButton) => ROW = 5 (LABEL ROW_SPAN=2) and RadioButtons(R5 & R6)
    designation_label = Label(
        master=user_details_frame,
        text='Are you a Student/Teacher : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    designation_label.grid(row=5, column=0, sticky=W, rowspan=2)

    designation_list = ['Student', 'Teacher']
    designation_value = IntVar()

    for index, val in enumerate(designation_list):
        Radiobutton(
            master=user_details_frame,
            text=val,
            font=(utilities.FONT_NAME, 18),
            fg=utilities.PRIMARY_COLOR,
            variable=designation_value,
            value=index,
            command=check_admin
        ).grid(row=5 + index, column=1, sticky=W)

    # ----------------------------------------------------------------------------------------------Student USN => ROW = 7
    student_usn_label = Label(
        master=user_details_frame,
        text='Enter your U.S.N :',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    student_usn_label.grid(row=7, column=0, sticky=W)

    student_usn_entry = Entry(
        master=user_details_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30,
    )
    student_usn_entry.grid(row=7, column=1, sticky=E)

    # ----------------------------------------------------------------------------------------------SignUp Button => ROW = 8
    register_user_button = Button(
        master=user_details_frame,
        text='Sign Up',
        font=(utilities.FONT_NAME, 24, 'bold'),
        padx=12,
        pady=6,
        fg=utilities.PRIMARY_COLOR,
        activeforeground=utilities.COLOR_WHITE,
        command=sign_up,
    )
    register_user_button.grid(row=8, column=0, columnspan=3, pady=32)

    register_window.mainloop()


if __name__ == '__main__':
    main()
