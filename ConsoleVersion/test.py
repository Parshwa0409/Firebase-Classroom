""" DO NOT TOUCH """
NAME_KEY = 'name'
PHONE_NUM_KEY = 'phone_number'
EMAIL_KEY = 'email'
UNIQUE_ID_KEY = 'unique_id'
ADMIN_KEY = 'admin'
""" DO NOT TOUCH """

"""

########################## REGISTRATION TEST ##########################

name = input("Enter your FullName : ").strip().lower()
email = input("Enter your Email-ID : ").strip().lower()
phone_number = '+91' + input("Enter your PhoneNumber : ").strip()

admin_input = input("Are you a teacher , True/False  (Default False) : ").strip().lower()
admin = True if admin_input == 'true' else False

unique_id = None
if not admin:
    unique_id = input("Enter your USN : ").strip().lower()

# CREATE THE USER
new_user = UserModel(name=name, phone_number=phone_number, email=email, admin=admin, uid=unique_id)
# CONVERT THE 'USER_DATA' TO 'USER_JSON_DATA'
user_json = new_user.user_data_json
print(f"{user_json} \n")

# DEBUG
# print(user_json)

if not admin:
    # CREATE THE 'STUDENT_INSTANCE', PASS IN THE 'USER_INSTANCE'
    # new_student = StudentModel()
    # ADD THE 'student_JSON_DATA' TO 'CLOUD FIRESTORE'
    StudentModel.add_student_to_cloud_firestore(student_user_object=new_user)
    # ADD THE 'student_JSON_DATA' TO 'REALTIME DATABASE'
    StudentModel.add_student_to_realtime_db(student_user_object=new_user)
else:
    # CREATE THE 'TEACHER_INSTANCE', PASS IN THE USER_INSTANCE
    new_teacher = TeacherModel()
    # ADD THE 'teacher_JSON_DATA' TO 'CLOUD FIRESTORE'
    TeacherModel.add_teacher_to_cloud_firestore(teacher_user_object=new_user)
    # ADD THE 'teacher_JSON_DATA' TO 'REALTIME DATABASE'
    TeacherModel.add_teacher_to_realtime_db(teacher_user_object=new_user)
    upload_true = input("Do you want to upload a file , y/n ? ").lower()
    if upload_true == 'y':
        TeacherModel.teacher_upload_file()
        new_teacher.get_all_students_email()


########################## STUDENT ON LOGIN DATA SYNC TEST ##########################
user_email = input("Enter your Email-ID : ").strip().lower()
try:
    student_data = firebase_setup.db_student_node_reference.order_by_child(EMAIL_KEY).equal_to(user_email).get()  # => The returned data is of type OrderedDict , since it is not subscript-able , we must either convert it into tuple() or list()
    student_data_values = tuple(student_data.values())
    print(student_data_values)
    if student_data_values:
        student_data_dict = student_data_values[0]
        email = student_data_dict[EMAIL_KEY]
        name = student_data_values[NAME_KEY]
        uid = student_data_dict[UNIQUE_ID_KEY]
        print('Success')
except FirebaseError as e:
    print(e)
except Exception as e:
    print(str(e).title())


# STUDENT LOGIN
try:
    auth = firebase_setup.pyrebase_auth
    email = input("Enter your Email-ID : ").strip()
    password = input('Enter your Password : ').strip()
    user_logged_in = auth.sign_in_with_email_and_password(email=email,password=password) # ReturnType is dict/dictionary and then printout and get the key_names / grab hold of all the attributes/keys using '.keys()' method
    # Attributes of this returned data type =>
    user_attributes = user_logged_in.keys()
    print(f"All the attributes of the UserRecord are : {user_attributes} ")
    print(f"Complete UserRecord as Dictionary : {user_logged_in}")
    print(f"Complete UserRecord as DictionaryItems 👇")
    for item in user_logged_in.items():
        print(item)
    print(f'UserEmail extracted from the UserRecord = {user_logged_in["email"]}')
except Exception as e:
    # ReturnType of the exception => <class 'requests.exceptions.HTTPError'>
    print(e)


data = {
        'admin': True,
        'email': "aratikittur77@gmail.com",
        'name': "Arati Patil",
        'phone_number': "+919449518797",
        'unique_id': None
        }

user_returned_details = teacher_ref.push(data)
print(user_returned_details.key)

all_students_data = db_student_node_reference.get()
for student_id in all_students_data:
    student = db_student_node_reference.child(path=student_id).get()
    student_email = student['email']
    print(student_email)
"""

"""
DOWNLOAD ALL
all_files = pyrebase_storage.list_files()
for file in all_files:
    file_name = str(file.name)
    if not file_name.endswith('/'):
        only_file_name = file_name.split('/')[-1]
        file.download_to_filename(f"Downloads/{only_file_name}")  # download_to_filename works for individual_item of the iterable_object returned by the method 'list_files()'
        # pyrebase_storage.child(file_name).download("", only_file_name) 
        #we are able to use 'list_files()' because of service key attribute in the config_dict , 
        but we are not able to download because of that , so what we can do is list_all_files , manually filter out the file we need and download that , 
        else remove the service_account_key.json and then ask user for exact path and use it to download the file 
"""
import urllib  # the lib that handles the url stuff

# from urllib.request import urlopen
# # import json
# import json
# # store the URL in Variable
# # parameter for urlopen
target_url = 'https://firebasestorage.googleapis.com/v0/b/fir-classroom-d3688.appspot.com/o/Submissions%2FASDASD%2Fasdasd?alt=media'
# # store the response of URL
# response = urlopen(target_url)
# # storing the JSON response
# # from url in data
# data_json = json.loads(response.read())
# # print the json response
# print(data_json)


