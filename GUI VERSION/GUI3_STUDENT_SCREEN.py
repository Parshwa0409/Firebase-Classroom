import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import firebase_setup
import GUI_UTILS as utilities
import json
import requests

file_name = ''
directory_path = ''


# TODO : Clear fields after the operation
def main(user_dict=None):
    user_details = user_dict
    NAME_KEY = 'name'
    EMAIL_KEY = 'email'
    UNIQUE_ID_KEY = 'unique_id'

    def choose_file():
        global file_name
        file_chose = filedialog.askopenfile()
        if file_chose:
            confirm = messagebox.askyesno(
                title='Are You Sure?',
                message=f'Is this the "{file_chose.name}" to be uploaded?'
            )
            if confirm:
                file_name = file_chose.name
        else:
            file_name = None

    def update_gSheet(submitted_file_name: str):
        url = 'https://api.sheety.co/45f3d9566494068f0241115075f7ee5f/miniProjectStudentSubmission/records'
        header = {
            'Authorization': 'Basic cGFyc2h3YV9wYXRpbF9taW5pX3Byb2plY3Q6ZmlyZWJhc2VfY2xhc3Nyb29t'
        }
        now = datetime.datetime.now()
        date = now.strftime('%d-%m-%Y')
        time = now.strftime('%H:%M:%S')
        data = {'record': {
            'name': str(user_dict[NAME_KEY]).title(),
            'usn': str(user_dict[UNIQUE_ID_KEY]).upper(),
            'filename': submitted_file_name,
            'date': date,
            'time':time
        }}
        res = requests.post(url=url, headers=header, json=data)
        print(res.text)

    def upload_in_storage(file_path: str):
        student_usn = usn_entry.get().strip().upper()
        delimiter = '/' if '/' in file_path else '\\'
        only_filename = file_path.split(delimiter)[-1]
        upload_path = f'/Submissions/{student_usn}/{only_filename}'
        print(only_filename)
        update_gSheet(submitted_file_name=only_filename)
        storage = firebase_setup.pyrebase_root_storage
        storage.child(upload_path).put(file_path)

    def upload_file():
        global file_name
        if len(usn_entry.get()) == 0:
            messagebox.showwarning(
                title='Oops',
                message='Please make sure you have filled in USN filed.'
            )
        elif not file_name:
            messagebox.showwarning(
                title='Oops',
                message='You need to select / choose a file to upload it.'
            )
            return
        else:
            try:
                upload_in_storage(file_path=file_name)
                messagebox.showinfo(
                    title="SUCCESS",
                    message=f"File was successfully uploaded."
                )
                usn_entry.delete(0, END)
            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error_message = json.loads(error_json)['error']['message']
                print(error_message)
                messagebox.showerror(
                    title="STORAGE ERROR",
                    message=f"ERROR\n{str(error_message).replace('_', ' ')}"
                )

    def choose_dir():
        global directory_path
        directory_path = filedialog.askdirectory()

    def download_file():
        global directory_path
        file_path = file_name_entry.get().strip()
        if len(file_path) == 0:
            messagebox.showinfo(
                message='PLEASE MAKE SURE YOU SPECIFY THE EXACT FILE-PATH SENT TO YOU VIA EMAIL.\nDO NOT LEAVE THE FIELD EMPTY'
            )
        elif len(directory_path) == 0:
            messagebox.showwarning(
                message='PLEASE MAKE SURE TO CHOOSE THE DIRECTORY WHERE YOU WANT TO DOWNLOAD FILE.'
            )
        else:
            storage = firebase_setup.pyrebase_root_storage
            full_path = f"{directory_path}/{file_path.split('/')[-1]}"
            print(full_path)
            storage.child(file_path).download("", full_path)

    student_window = Toplevel()
    student_window.title('User - Student')
    student_window.config(pady=24, padx=24)

    welcome_label_frame = LabelFrame(
        master=student_window,
        text=' Welcome ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        pady=24,
        padx=12,
    )
    welcome_label_frame.grid(row=0)

    Label(
        master=welcome_label_frame,
        text=f"Name : {str(user_details[NAME_KEY]).title()}\tUSN : {str(user_details[UNIQUE_ID_KEY]).upper()}",
        font=(utilities.FONT_NAME, 28, 'bold'),
        padx=24,
        pady=12,
        fg=utilities.PRIMARY_COLOR
    ).grid(row=0, pady=8, sticky=W)

    Label(
        master=welcome_label_frame,
        text=f"Email - ID: {user_details[EMAIL_KEY]}",
        font=(utilities.FONT_NAME, 28, 'bold'),
        padx=24,
        pady=12,
        fg=utilities.PRIMARY_COLOR
    ).grid(row=1, pady=8, sticky=W)

    # ------------------------------------------------------------------------------------------------------UPLOAD FRAME
    upload_frame = LabelFrame(
        master=student_window,
        text=' Upload ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        pady=24,
        padx=24,
        fg=utilities.PRIMARY_COLOR
    )
    upload_frame.grid(row=1, padx=16, pady=16)

    # -------------------------------------------------------------------------------------------------------TITLE LABEL
    upload_title = Label(
        master=upload_frame,
        text='SELECT THE FILE & UPLOAD YOUR ASSIGNMENT-SOLUTION/WORK',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    )
    upload_title.grid(row=0, column=0, columnspan=2, pady=16)

    # --------------------------------------------------------------------------------------------USN ROW(LABEL + ENTRY)
    usn_label = Label(
        master=upload_frame,
        text='Enter your registered USN : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    usn_label.grid(row=1, column=0, sticky=W)
    usn_entry = Entry(
        master=upload_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    usn_entry.grid(row=1, column=1, sticky=E)

    # ------------------------------------------------------------------------------------------------------- Button Row
    choose_file_button = Button(
        master=upload_frame,
        text='Choose File',
        font=(utilities.FONT_NAME, 24, 'bold'),
        padx=12,
        pady=6,
        fg=utilities.PRIMARY_COLOR,
        activeforeground=utilities.COLOR_WHITE,
        command=choose_file,
    )
    choose_file_button.grid(row=2, column=0, sticky=W, pady=16)

    upload_file_button = Button(
        master=upload_frame,
        text='Upload File',
        font=(utilities.FONT_NAME, 24, 'bold'),
        padx=12,
        pady=6,
        fg=utilities.PRIMARY_COLOR,
        activeforeground=utilities.COLOR_WHITE,
        command=upload_file,
    )
    upload_file_button.grid(row=2, column=1, sticky=E, pady=16)

    download_frame = LabelFrame(
        master=student_window,
        text=' Download ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        pady=24,
        padx=20,
        fg=utilities.PRIMARY_COLOR
    )
    download_frame.grid(row=2, padx=16, pady=16)

    # -------------------------------------------------------------------------------------------------------TITLE LABEL
    download_title = Label(
        master=download_frame,
        text='TYPE THE FILE NAME & DOWNLOAD YOUR ASSIGNMENT/WORK',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    )
    download_title.grid(row=0, column=0, columnspan=2, pady=16)

    # ------------------------------------------------------------------------------------------- USN ROW(LABEL + ENTRY)
    file_name_label = Label(
        master=download_frame,
        text='Enter the File-Path / Name : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    file_name_label.grid(row=1, column=0, sticky=W)
    file_name_entry = Entry(
        master=download_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    file_name_entry.grid(row=1, column=1, sticky=E)

    # ------------------------------------------------------------------------------------------------------- Button Row
    choose_dir_button = Button(
        master=download_frame,
        text='Choose Location To Download File',
        font=(utilities.FONT_NAME, 16, 'bold'),
        padx=12,
        pady=6,
        fg=utilities.PRIMARY_COLOR,
        activeforeground=utilities.COLOR_WHITE,
        command=choose_dir,
    )
    choose_dir_button.grid(row=2, column=0, sticky=W, pady=16)
    download_file_button = Button(
        master=download_frame,
        text='Download File',
        font=(utilities.FONT_NAME, 24, 'bold'),
        padx=12,
        pady=6,
        fg=utilities.PRIMARY_COLOR,
        activeforeground=utilities.COLOR_WHITE,
        command=download_file,
    )
    download_file_button.grid(row=2, column=1, sticky=E, pady=16, columnspan=2)

    student_window.mainloop()


if __name__ == '__main__':
    main()
