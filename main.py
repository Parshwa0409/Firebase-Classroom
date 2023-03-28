from FirebaseAuthentication.auth_class import AuthenticateUser

# a boolean value to know when to stop the program.
from ConsoleVersion.Models.student_model import StudentModel
from ConsoleVersion.Models.teacher_model import TeacherModel
from ConsoleVersion.Models.user_model import UserModel

continue_the_program = True


def print_menu(user_function_dict: dict):
    print('\nENTER THE TASK TO BE PERFORMED.\n')
    for (k, v) in user_function_dict.items():
        print(f'{k}) {v}')
    task = int(input('Enter your choice , Type the number of the task {1 OR 2}: '))
    return task


# First is to log-in/sign-up and authenticate
current_user = AuthenticateUser()

user_choice = int(input("1)Already a user? Sign-In.\n2)Not a user? Sign-Up now.\nEnter your choice {1 OR 2} : "))
if user_choice == 1:
    current_user.login_with_email_password()
elif user_choice == 2:
    current_user.register_new_user()
else:
    print("INVALID USER INPUT, PLEASE TRY AGAIN!!!")
    continue_the_program = False

# If the input was valid and current user is admin a teacher, continue with functionality
if continue_the_program and current_user.admin:
    current_teacher = TeacherModel(name=current_user.name, email=current_user.email)
    task_num = print_menu(current_teacher.func_dict)
    if task_num == 1:
        current_teacher.teacher_upload_file()
    elif task_num == 2:
        current_teacher.download_solution()
    else:
        print('Invalid Option')
elif continue_the_program and not current_user.admin:
    current_student = StudentModel(name=current_user.name, email=current_user.email, uid=current_user.uid)
    task_num = print_menu(current_student.func_dict)
    if task_num == 1:
        current_student.student_upload_assignment()
    elif task_num == 2:
        current_student.student_download_assignment()
    else:
        print('Invalid Option')

"""
# print(f"Current UserName : {current_user.name}")
# print(f"Current UserName Email-ID : {current_user.email}")
# print(f"Current UserName Unique-ID : {current_user.uid}")
"""