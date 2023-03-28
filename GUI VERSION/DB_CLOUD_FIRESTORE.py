import firebase_setup


def register_user_cloud_firestore(admin: bool, user_data: dict):
    cloud_firestore_teacher_collection_path = 'teacher_collection'
    cloud_firestore_student_collection_path = 'student_collection'

    cloud_firestore = firebase_setup.cloud_firestore
    if not admin:
        cloud_firestore.collection(cloud_firestore_student_collection_path).document(user_data['unique_id']).set(user_data)
    else:
        cloud_firestore.collection(cloud_firestore_teacher_collection_path).document(user_data['email']).set(user_data)