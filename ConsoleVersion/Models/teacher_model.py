import firebase_setup
from ConsoleVersion.Models.user_model import UserModel

""" DO NOT TOUCH """
NAME_KEY = 'name'
PHONE_NUM_KEY = 'phone_number'
EMAIL_KEY = 'email'
UNIQUE_ID_KEY = 'unique_id'
ADMIN_KEY = 'admin'
""" DO NOT TOUCH """


class TeacherModel:
    def __init__(self, name, email):
        self.students_email = []
        self.upload_path = None
        self.func_dict = {
            1: "Upload Assignment/Notes.",
            2: "Download Student's Assignment's Solution."
        }
        self.email = email
        self.name = name

    # KEEPING THE METHOD STATIC , TO SAVE MEMORY & MAKE IT EASIER TO CALL THE METHOD TO REGISTER A NEW USER WITHOUT ACTUALLY HAVING TO CREATE AN OBJECT
    @staticmethod
    def add_teacher_to_cloud_firestore(teacher_user_object: UserModel):
        """Add the teacher's document with auto-generated-id to CLOUD_FIRESTORE"""
        cloud_firestore = firebase_setup.cloud_firestore
        cloud_firestore_collection_path = 'teacher_collection'
        # ADD THE TEACHER DOCUMENT TO THE TEACHERS COLLECTION , BUT AUTO GENERATED UID ...
        # METHOD 1
        cloud_firestore.collection(cloud_firestore_collection_path).document().set(teacher_user_object.user_data_json)
        # METHOD 2
        # self.cloud_firestore.collection(self.collection_path).add(self.teacher_user_object.user_data_json)

        # DEBUG ROUTINE
        # print("TEACHER USER DATA SUCCESSFULLY STORED IN CLOUD FIRESTORE")

    @staticmethod
    def add_teacher_to_realtime_db(teacher_user_object: UserModel):
        """Add the teacher's data in JSON format into the REALTIME_DATABASE under teacher_node"""
        # GET HOLD OF THE teacher 'USER_DATA_JSON'
        teacher_json_data = teacher_user_object.user_data_json

        # GET ACCESS TO THE 'REALTIME_DATABASE' , GET THE REFERENCE TO THE 'Teacher_NODE' IN THE DATABASE
        teacher_node_ref = firebase_setup.db_teacher_node_reference

        # 'PUSH()' THE DATA INTO THE NODE AND THE 'UNIQUE-ID' FOR THE 'NEWLY PUSHED CHILD_NODE' IS 'AUTO GENERATED'
        teacher_node_ref.push(value=teacher_json_data)

        # DEBUG ROUTINE
        # print("TEACHER USER DATA SUCCESSFULLY STORED IN REALTIME DATABASE")

    def teacher_upload_file(self):
        final_route = '/'
        subject_dict = {1: 'Physics', 2: 'Chemistry', 3: 'Mathematics', 4: 'Biology'}
        work_file_dict = {1: 'Assignment', 2: 'Notes'}

        # CHOOSE THE SUBJECT OF THE FILE BEING UPLOADED
        print('\nCHOOSE THE SUBJECT OF THE FILE BEING UPLOADED : ')
        for (k, v) in subject_dict.items():
            print(f"{k}) {v}")
        subject_selected_key = int(input("Enter the respective number : "))
        subject_selected_value = subject_dict[subject_selected_key]
        final_route += subject_selected_value + '/'

        # CHOOSE THE TYPE OF THE WORK_FILE BEING UPLOADED, ASSIGNMENT OR QUIZ OR NOTES ETC
        print('\nCHOOSE THE TYPE OF THE WORK_FILE BEING UPLOADED : ')
        for (k, v) in work_file_dict.items():
            print(f"{k}) {v}")
        work_file_key = int(input("Enter the respective number : "))
        work_file_value = work_file_dict[work_file_key]
        final_route += work_file_value + '/'

        user_file_path = input(
            "Enter the file which is being uploaded , (absolute path of the file on your machine) : ")
        temp_file_name = user_file_path.split('/')[-1]  # Last bit of file_path => actual file name
        final_route += temp_file_name

        pyrebase_storage = firebase_setup.pyrebase_root_storage
        pyrebase_storage.child(final_route).put(user_file_path)
        file_link = pyrebase_storage.child(final_route).get_url(None)
        print(f"Link of he uploaded file 👇\n{file_link}\n")
        self.get_all_students_email()

    def get_all_students_email(self):
        """Teacher gets all the registered student email and then email all the registered student's whenever a file is uploaded y a teacher """
        # Get the reference to the 'student_nodes'
        db_student_node_reference = firebase_setup.db_student_node_reference

        # Get all the data in the 'teachers_node' , we get all the 'keys/child_node_id' & 'child_node => student_data'
        all_students_uid = db_student_node_reference.get()
        for student_uid in all_students_uid:
            student = db_student_node_reference.child(student_uid).get()
            student_email = student[EMAIL_KEY]
            self.students_email.append(student_email)
        print(self.students_email)
        # TODO: SEND EMAIL TO ALL THE STUDENTS, 'GET_ALL_STUDENTS()'

    @staticmethod
    def download_solution():
        storage = firebase_setup.pyrebase_root_storage

        usn = input("Enter the student's registered USN, whose submission is to be downloaded : ").upper().strip()
        file_name = input('Enter the name of the file to be downloaded : ').strip()

        # The location of the file in storage.
        storage_download_path = f'/Submissions/{usn}/{file_name}'

        # The location and name wh the file will be stored when downloaded.
        download_path = f'Submissions/{usn}_{file_name}'

        storage.child(storage_download_path).download("", download_path)
        print(f'FILE DOWNLOADED AS {usn}_{file_name} => FULL PATH = {download_path}')
