from engine.models.user import User

user_data = {
    User._id_attr: '123',
    User._name_attr: 'tester',
    User._token_attr: 'some_token',
    User._password_attr: 'secret_password'
}

user_data_without_id = {
    User._id_attr: None,
    User._name_attr: 'tester',
    User._token_attr: 'some_token',
    User._password_attr: 'secret_password'
}