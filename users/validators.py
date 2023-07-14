import re


def user_name_validator(user_name: str) -> dict:
    if len(user_name) < 3:
        return {'Error': 'the username is too short'}
    

def first_name_validator(first_name: str) -> dict:
    if len(first_name) == 0:
        return {'Error': 'the name field cannot be empty'}
    

def last_name_validator(last_name: str) -> dict:
    if len(last_name) == 0:
        return {'Error': 'the last_name field cannot be empty'}
    
def password_validator(password, password_check):
    if password != password_check:
        print('asdadasdasdas')
        return {'Error': 'Erorr'}
    

def email_validator(email: str) -> dict:
    if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
        return {'Error': 'the email is invalid'}
