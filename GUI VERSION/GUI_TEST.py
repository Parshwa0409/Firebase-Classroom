from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import GUI_UTILS as utilities
import requests
import json
import firebase_setup

directory_path = ''


def main():

    def choose_dir():
        global directory_path
        directory_path = filedialog.askdirectory()

    def download_solution():
        global directory_path
        storage = firebase_setup.pyrebase_root_storage
        usn = usn_entry.get().upper().strip()
        file_name = file_name_entry.get().strip()
        storage_download_path = f'Submissions/{usn}/{file_name}'
        download_path = f'{directory_path}/{usn}_{file_name}'
        storage.child(storage_download_path).download("", filename=download_path)
        messagebox.showinfo(message=f'FILE DOWNLOADED AS {usn}_{file_name} => FULL PATH = {download_path}')


    def download_file():
        file_entry_name = file_name_entry.get().strip()
        usn = usn_entry.get().strip().upper()
        if len(directory_path) == 0:
            messagebox.showwarning(
                title='Location Not Specified',
                message='Please choose t he path/location where to download the file.'
            )
        elif len(file_entry_name) == 0 or len(usn) == 0:
            messagebox.showwarning(
                title='Data-Incomplete',
                message='Please make sure to correctly fill all the input fields.'
            )
        else:
            download_solution()
            # usn_entry.delete(0, END)
            # file_name_entry.delete(0, END)

    # KEY NAME
    NAME_KEY = 'name'
    EMAIL_KEY = 'email'

    def upload_file():
        file = filedialog.askopenfile()
        if file:
            file_path = file.name
            delimiter = '/' if '/' in file_path else "\\"
            file_name = file_path.split(delimiter)[-1]
            confirm = messagebox.askyesno(
                title='Confirmation',
                message=f'Selected File : {file_name} , Do You Want To Upload It?'
            )
            messagebox.showinfo(
                title='UPLOADING FILE',
                message='Please Wait For The Confirmation Of File Being Uploaded'
            )
            if confirm:
                try:
                    final_upload_path = f"/{subject_list[subject_value.get()]}/{work_list[work_value.get()]}/{file_name}"
                    storage = firebase_setup.pyrebase_root_storage
                    storage.child(final_upload_path).put(file_path)
                    messagebox.showinfo(
                        title="SUCCESS",
                        message=f"\"{file_name}\"\nSuccessfully Uploaded."
                    )
                    file_link = storage.child(final_upload_path).get_url(None)
                    link_of_file.delete(0, END)
                    link_of_file.insert(0, file_link)
                except requests.exceptions.HTTPError as e:
                    error_json = e.args[1]
                    error_message = json.loads(error_json)['error']['message']
                    print(error_message)
                    messagebox.showerror(
                        title="STORAGE ERROR",
                        message=f"ERROR\n{str(error_message).replace('_', ' ')}"
                    )
                except requests.exceptions.ConnectionError as c:
                    messagebox.showerror(
                        title="CONNECTION ERROR",
                        message=f"Looks like there is some problem with the connection.\nCheck the network connection on your device."
                    )
                except Exception as e:
                    messagebox.showerror(
                        title="ERROR",
                        message=f"{e}"
                    )

    teacher_window = Tk()
    teacher_window.title('User - Teacher')
    teacher_window.configure(padx=24, pady=24)

    upload_frame = LabelFrame(
        master=teacher_window,
        text=' Upload ',
        font=(utilities.FONT_NAME, 16, 'bold'),
        # pady=24,
        padx=24,
        fg=utilities.PRIMARY_COLOR
    )
    upload_frame.grid(row=0)

    # Subject RadioButtons
    subject_label = Label(
        master=upload_frame,
        text='Choose The Subject Of Document Being Uploaded 👇',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    )
    subject_label.grid(row=0, column=0, columnspan=4, pady=16)

    subject_list = ['Physics', 'Chemistry', 'Mathematics', 'Biology']
    subject_value = IntVar()

    for index, sub in enumerate(subject_list):
        Radiobutton(
            master=upload_frame,
            text=sub,
            font=(utilities.FONT_NAME, 18),
            fg=utilities.PRIMARY_COLOR,
            variable=subject_value,
            value=index,
        ).grid(row=1, column=index, pady=16)

    # Work RadioButton , Notes/Assignment/etc.
    work_label = Label(
        master=upload_frame,
        text='Choose The Type Of Document Being Uploaded 👇',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    )
    work_label.grid(row=3, column=0, columnspan=4, pady=16)

    work_list = ['Assignment', 'Practice Questions', 'Question Papers', 'Subject Notes']
    work_value = IntVar()

    for index, work in enumerate(work_list):
        Radiobutton(
            master=upload_frame,
            text=work,
            font=(utilities.FONT_NAME, 18),
            fg=utilities.PRIMARY_COLOR,
            variable=work_value,
            value=index,
        ).grid(row=4, column=index, pady=16)

    # Chose The File To Upload ...
    upload_button_label = Label(
        master=upload_frame,
        text='Choose The Document / File Being Uploaded 👉 ',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    )
    upload_button_label.grid(row=5, column=0, columnspan=3, pady=16, sticky=W)

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
    upload_file_button.grid(row=5, column=3, pady=16, sticky=E)

    Label(
        master=upload_frame,
        text='Link Of Uploaded File 👇 , {Copy & Use It If Necessary}',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    ).grid(row=6, column=0, columnspan=4, pady=16, sticky=W)

    link_of_file = Entry(
        master=upload_frame,
        font=(utilities.FONT_NAME, 16),
        fg='light blue',
        width=78
    )
    link_of_file.grid(row=7, column=0, pady=8, sticky=W, columnspan=4)

    # Download Section
    download_frame = LabelFrame(
        master=teacher_window,
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
        text='ENTER THE DETAILS & DOWNLOAD THE SUBMITTED ASSIGNMENT/WORK 👇',
        font=(utilities.FONT_NAME, 20, 'bold'),
        fg=utilities.PRIMARY_COLOR
    )
    download_title.grid(row=0, column=0, columnspan=2, pady=16)

    # ------------------------------------------------------------------------------------------- USN ROW(LABEL + ENTRY)
    file_name_label = Label(
        master=download_frame,
        text='Enter the File / Assignment Name : ',
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

    # ------------------------------------------------------------------------------------------- USN ROW(LABEL + ENTRY)
    usn_label = Label(
        master=download_frame,
        text='Enter registered USN of Student : ',
        font=(utilities.FONT_NAME, 22, 'bold'),
        padx=12,
        pady=16,
        fg=utilities.PRIMARY_COLOR
    )
    usn_label.grid(row=2, column=0, sticky=W)
    usn_entry = Entry(
        master=download_frame,
        font=(utilities.FONT_NAME, 16),
        fg=utilities.PRIMARY_COLOR,
        width=30
    )
    usn_entry.grid(row=2, column=1, sticky=E)

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
    choose_dir_button.grid(row=3, column=0, sticky=W, pady=16)
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
    download_file_button.grid(row=3, column=1, sticky=E, pady=16, columnspan=2)
    teacher_window.mainloop()


if __name__ == '__main__':
    main()
