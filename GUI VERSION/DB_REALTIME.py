from email.mime.text import MIMEText

import firebase_setup
import datetime as dt
import smtplib
import os

teacher_node_ref = firebase_setup.db_teacher_node_reference
student_node_ref = firebase_setup.db_student_node_reference


def register_user_db(admin: bool, user_data: dict):
    if admin:
        teacher_node_ref.push(user_data)
    else:
        student_node_ref.child(user_data['unique_id']).set(user_data)


def get_details_by_email(email: str, admin: bool):
    node_ref = student_node_ref if not admin else teacher_node_ref
    user_details = node_ref.order_by_child('email').equal_to(email).get()
    if user_details:
        value = user_details.values()
        value_as_tuple = tuple(value)
        user_dict = value_as_tuple[0]
        return user_dict
    else:
        print('Not Found')
        return False

# nvtmmjfaqrgskvoi

def send_emails(file_link: str, file_path: str, teacher_name: str):
    # Get The Date
    now = str(dt.datetime.now()).split()[0]
    # GETTING THE FINAL EMAIL_TEMPLATE READY
    with open(file='email_template') as email_template:
        temp = email_template.read()
        temp = temp.replace('[DATE]', str(now))
        temp = temp.replace('[FILE PATH]', file_path)
        temp = temp.replace('[LINK]', file_link)
        temp = temp.replace('[TEACHER NAME]', teacher_name.title())
        final_template = temp

    # GETTING EMAIL OF ALL THE REGISTERED STUDENTS
    all_students_email = []
    returned_value = student_node_ref.get()
    all_items = returned_value.items()
    for key, value in all_items:
        all_students_email.append(value['email'])

    # GETTING MY EMAIL + PASSWORD
    my_email = os.environ.get('PYTHON_ACCOUNT_EMAIL')
    password = 'nvtmmjfaqrgskvoi'

    # CREATING A 'CONNECTION_OBJECT' # GIVING A PROVIDER
    connection = smtplib.SMTP('smtp.gmail.com', 587)

    # SECURING THE CONNECTION
    connection.starttls()

    # LOGGING IN WITH EMAIL + PASSWORD
    connection.login(my_email, password)

    msg = MIMEText(final_template, 'plain', 'utf-8')
    # ITERATING THROUGH EVERY 'STUDENT_EMAIL'
    for student_email in all_students_email:
        # SENDING EMAIL TO EAC STUDENT
        connection.sendmail(
            from_addr=my_email,
            to_addrs=student_email,
            msg=msg.as_string()
        )
    # ONCE EVERYTHING IS DONE CLOSE THE CONNECTION
    connection.quit()

# print(get_details_by_email('parshwapatil9@gmail.com',True))

# send_emails(file_link='link', file_path='path', teacher_name='Arati Patil')
print('Hello World')
