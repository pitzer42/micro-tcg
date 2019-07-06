from engine.models.user import User

user_data = {
    User.__id_attr__: '123',
    User.__name_attr__: 'tester',
    User.__token_attr__: 'some_token',
    User.__password_attr__: 'secret_password'
}

user_data_without_id = {
    User.__id_attr__: None,
    User.__name_attr__: 'tester',
    User.__token_attr__: 'some_token',
    User.__password_attr__: 'secret_password'
}