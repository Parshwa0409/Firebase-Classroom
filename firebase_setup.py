import firebase_admin
import pyrebase
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

""" DO NOT TOUCH """
cred = credentials.Certificate("/Users/parshwapatil/PycharmProjects/FirebaseClassroom/service_account_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-classroom-d3688-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://fir-classroom-d3688.appspot.com',
})

firebaseConfig = {
  'apiKey': "AIzaSyCGI1uMUdo4yqle7DbOOwirYlKK-LkNF8M",
  'authDomain': "fir-classroom-d3688.firebaseapp.com",
  'projectId': "fir-classroom-d3688",
  'storageBucket': "fir-classroom-d3688.appspot.com",
  'messagingSenderId': "19827441152",
  'appId': "1:19827441152:web:0bd7e5772f417b4ae362e5",
  'databaseURL': 'https://fir-classroom-d3688-default-rtdb.firebaseio.com/',
  # 'serviceAccount': '/Users/parshwapatil/PycharmProjects/FirebaseClassroom/service_account_key.json'
}

# PATH VARIABLE's- ROUTE's
STUDENT_NODE = '/student_node'
TEACHER_NODE = '/teacher_node'

# INITIALIZE CLOUD_FIRESTORE
cloud_firestore = firestore.client()

# INITIALIZE REALTIME_DB AND GET THE REQUIRED_NODE's_REFERENCE
db_student_node_reference = db.reference(STUDENT_NODE)
db_teacher_node_reference = db.reference(TEACHER_NODE)

# INITIALIZE FIREBASE_ADMIN AUTH_SERVICE , FOR BETTER REGISTRATION OF USER
firebase_auth = auth

# INITIALIZE PYREBASE APP FOR ACCESS OF VARIOUS MODULES FUNCTION OF FIREBASE THROUGH PYREBASE_MODULE
pyrebase_app = pyrebase.initialize_app(firebaseConfig)

# INITIALIZE STORAGE
pyrebase_root_storage = pyrebase_app.storage()

# INITIAL AUTH_SERVICE OF PYREBASE FOR EASIER LOGIN
pyrebase_auth = pyrebase_app.auth()

""" DO NOT TOUCH """