NAME_KEY = 'name'
PHONE_NUM_KEY = 'phone_number'
EMAIL_KEY = 'email'
UNIQUE_ID_KEY = 'unique_id'
ADMIN_KEY = 'admin'


class UserModel:
    def __init__(self, name, phone_number, email, uid, admin):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.uid = uid
        self.admin = admin
        self.user_data_json = None
        self.user_to_json()

    def user_to_json(self):
        """Convert the user data to JSON format , and store it as attribute of UserModel class, also return the JSON_Format of data."""
        user_data = {
            NAME_KEY: self.name,
            PHONE_NUM_KEY: self.phone_number,
            EMAIL_KEY: self.email,
            UNIQUE_ID_KEY: self.uid,
            ADMIN_KEY: self.admin
        }

        self.user_data_json = user_data
        return user_data
