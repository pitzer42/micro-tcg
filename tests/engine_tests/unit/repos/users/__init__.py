from engine.repos.schemas.user import (
    uid_attr,
    name_attr,
    token_attr,
    password_attr
)

user_data = {
    uid_attr: '123',
    name_attr: 'tester',
    token_attr: 'some_token',
    password_attr: 'secret_password'
}

user_data_without_id = {
    uid_attr: None,
    name_attr: 'tester',
    token_attr: 'some_token',
    password_attr: 'secret_password'
}