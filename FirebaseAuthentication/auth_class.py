import firebase_setup
from ConsoleVersion.Models import user_model
from ConsoleVersion.Models.student_model import StudentModel
from ConsoleVersion.Models.teacher_model import TeacherModel
from firebase_setup import firebase_auth, pyrebase_auth

""" DO NOT TOUCH """
NAME_KEY = 'name'
PHONE_NUM_KEY = 'phone_number'
EMAIL_KEY = 'email'
UNIQUE_ID_KEY = 'unique_id'
ADMIN_KEY = 'admin'
""" DO NOT TOUCH """


class AuthenticateUser:
    def __init__(self):
        self.email = None
        self.name = None
        self.uid = None
        self.admin = None

    def login_with_email_password(self):
        email = input("Enter your Email-ID : ").strip()
        password = input('Enter your Password : ').strip()
        self.admin = True if (input('Are you a Teacher? Enter True, (Default => False) : ') == 'True') else False
        user_record = pyrebase_auth.sign_in_with_email_and_password(email=email, password=password)

        if user_record:
            self.sync_user_details(admin=self.admin, email=email)
            # print(user_record.values())
        else:
            print("User data not found, Please try again.")

    def register_new_user(self):
        name = input("Enter your FullName : ").strip().lower()
        phone_number = '+91' + input("Enter your PhoneNumber : ").strip()
        email = input("Enter your Email-ID : ").strip()
        password = input("Enter your Password : ").strip()

        self.admin = True if (input('Are you a Teacher? Enter True (Default is False) : ') == 'True') else False

        unique_id = input("Enter your USN : ").strip().lower() if not self.admin else None

        new_user = user_model.UserModel(
            name=name,
            phone_number=phone_number,
            email=email,
            admin=self.admin,
            uid=unique_id
        )

        if self.admin:
            user_record = firebase_auth.create_user(
                email=new_user.email,
                password=password,
                display_name=new_user.name,
                phone_number=new_user.phone_number
            )
            # new_teacher = TeacherModel() => IF NEEDED IN FUTURE
            TeacherModel.add_teacher_to_cloud_firestore(teacher_user_object=new_user)
            TeacherModel.add_teacher_to_realtime_db(teacher_user_object=new_user)

        else:
            user_record = firebase_auth.create_user(
                uid=new_user.uid,
                email=new_user.email,
                password=password,
                display_name=new_user.name,
                phone_number=new_user.phone_number
            )

            # new_student = StudentModel() => IF NEEDED IN FUTURE
            StudentModel.add_student_to_cloud_firestore(student_user_object=new_user)
            StudentModel.add_student_to_realtime_db(student_user_object=new_user)

        self.name = str(new_user.name).title()
        self.email = new_user.email
        self.admin = new_user.admin
        self.uid = str(new_user.uid).title() if not new_user.admin else None

    def sync_user_details(self, admin: bool, email: str):
        # IF ADMIN==TRUE GET 'TEACHER_DB' REFERENCE , ELSE 'STUDENT_DB' REFERENCE
        if not admin:
            db_node_reference = firebase_setup.db_student_node_reference
        else:
            db_node_reference = firebase_setup.db_teacher_node_reference

        user_data = db_node_reference.order_by_child(EMAIL_KEY).equal_to(email).get()
        data_value_as_tuple = tuple(user_data.values())
        if data_value_as_tuple != ():
            data_dict = data_value_as_tuple[0]
            self.name = str(data_dict[NAME_KEY]).title()
            self.email = data_dict[EMAIL_KEY]
            self.uid = str(data_dict[UNIQUE_ID_KEY]).upper() if not admin else None
        else:
            print("User data not found, Please try again.")
        # print(f"{self.name}, Signed-In successfully.")
        # print(f"Your Email-ID : {self.email}")
        # if self.uid:
        #     print(f"Your Unique-ID : {self.uid}")


# new_auth = AuthenticateUser()
# new_auth.login_with_email_password()
# if user_record_dict:
#     self.email = user_record_dict['email']
#     self.name = str(user_record_dict['displayName']).title()
#     self.admin = admin
#
# if not admin:
#     current_student = StudentModel()
#     current_student.on_login_sync_user(user_email=self.email)
#     print('\nENTER THE TASK TO BE PERFORMED.\n')
#     for (k, v) in current_student.func_dict.items():
#         print(f'{k}) {v}')
#     task_num = int(input('Enter your choice , Type the number of the task : '))
#     if task_num == 1:
#         current_student.student_upload_assignment()
#     elif task_num == 2:
#         current_student.student_download_assignment()
