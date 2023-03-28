import firebase_setup

teacher_node_ref = firebase_setup.db_teacher_node_reference
student_node_ref = firebase_setup.db_student_node_reference


def register_user_db(admin: bool, user_data: dict):
    if admin:
        teacher_node_ref.push(user_data)
    else:
        student_node_ref.child(user_data['unique_id']).set(user_data)


def get_student_usn_by_email(email: str):
    node_ref = student_node_ref
    user_details = node_ref.order_by_child('email').equal_to(email).get()
    if user_details:
        for key in user_details:
            # TODO: THINK OF RETURNING DATA TO CALLING FUNCTION
            print(key)
            print(user_details[key]['unique_id'])
    else:
        pass
