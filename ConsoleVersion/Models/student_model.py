import firebase_setup
from ConsoleVersion.Models.user_model import UserModel

""" DO NOT TOUCH """
NAME_KEY = 'name'
PHONE_NUM_KEY = 'phone_number'
EMAIL_KEY = 'email'
UNIQUE_ID_KEY = 'unique_id'
ADMIN_KEY = 'admin'
""" DO NOT TOUCH """


class StudentModel:
    def __init__(self, email, name, uid):
        self.name = name
        self.email = email
        self.uid = uid
        self.func_dict = {
            1: "Upload The Assignment Solution.",
            2: "Download The Given Assignment."
        }

    @staticmethod
    def add_student_to_cloud_firestore(student_user_object: UserModel):
        """Add the student's document with usn as id to CLOUD_FIRESTORE"""
        # GET THE USN OF STUDENT
        student_uid = student_user_object.uid

        collection_path = 'student_collection'

        # GET ACCESS TO THE 'CLOUD_FIRESTORE'
        cloud_firestore = firebase_setup.cloud_firestore

        # ADD DATA TO CLOUD FIRESTORE , student_collection/student_document (Document Name = USN) =>json_data
        cloud_firestore.collection(collection_path).document(student_uid).set(student_user_object.user_data_json)

        # DEBUG ROUTINE
        # print("STUDENT USER DATA SUCCESSFULLY STORED IN CLOUD FIRESTORE")

    @staticmethod
    def add_student_to_realtime_db(student_user_object: UserModel):
        """Add the student's data in JSON format into the REALTIME_DATABASE under student_node"""

        # GET ACCESS TO THE 'REALTIME_DATABASE' , GET THE REFERENCE TO THE 'STUDENT_NODE' IN THE DATABASE
        student_node_ref = firebase_setup.db_student_node_reference

        # GET HOLD OF THE STUDENT 'USER_DATA_JSON'
        student_json_data = student_user_object.user_data_json

        # 'PUSH()' THE DATA INTO THE NODE AND THE 'UNIQUE-ID' FOR THE 'NEWLY PUSHED CHILD_NODE' IS 'AUTO GENERATED'
        student_node_ref.push(value=student_json_data)

        # DEBUG ROUTINE
        # print("STUDENT USER DATA SUCCESSFULLY STORED IN REALTIME DATABASE")

    def student_upload_assignment(self):
        # # FOR NOW , DEBUGGING
        # user_email = input("Enter your registered email :  ").strip().lower()
        # self.on_login_sync_user(user_email=user_email)

        common_student_submission_path = "/Submissions/"

        print('THE ASSIGNMENT BEING SUBMITTER MUST HAVE THE SAME NAME AS THE ASSIGNMENT GIVEN BY TEACHER , FOR EASIER IDENTIFICATION.')
        student_file = input("Enter the file which is being uploaded , (absolute path of the file on your machine) : ")
        file_name = student_file.split('/')[-1]  # For windows , change the slash
        final_path = common_student_submission_path+self.uid+'/'+file_name

        # NOW UPLOAD THE FILE INTO THE FIREBASE_STORAGE

        # get the reference to the storage,
        storage = firebase_setup.pyrebase_root_storage
        storage.child(final_path).put(student_file)

    @staticmethod
    def student_download_assignment():
        storage = firebase_setup.pyrebase_root_storage
        # Get the full path for the uploaded assignment
        file_path = input('ENTER THE PATH OF THE FILE SENT BY YOUR TEACHER : ')
        download_path = 'Downloads/'+file_path.split('/')[-1]
        storage.child(file_path).download("", download_path)
        # get directory where to download and then download it there with same name as it was uploaded
        print("THE FILE HAS BEEN SUCCESSFULLY DOWNLOADED.")
        pass

    # def on_login_sync_user(self, user_email):
    #     # GET THE REFERENCE TO THE REALTIME_DATABASE
    #     db_student_node_reference = firebase_setup.db_student_node_reference
    #
    #     # Get all the data in the 'STUDENTS-NODE' , we get all the 'keys/child_node_id' & 'child_node => student_data'
    #     student_data = db_student_node_reference.order_by_child(EMAIL_KEY).equal_to(user_email).get()  # => The returned data is of type OrderedDict , since it is not subscript-able , we must either convert it into tuple() or list()
    #     # If while searching query , if the email is not registered , was deleted , or anything else , then we get and empty value like () , [] , {}
    #     student_data_values = tuple(student_data.values())
    #     if student_data_values:
    #         student_data_dict = student_data_values[0]
    #         self.name = student_data_dict[NAME_KEY]
    #         self.email = student_data_dict[EMAIL_KEY]
    #         self.uid = student_data_dict[UNIQUE_ID_KEY]
    #
    #     else:
    #         self.email = self.name = 'Anonymous User'
    #         self.uid = input("Enter your USN : ").strip().lower()



