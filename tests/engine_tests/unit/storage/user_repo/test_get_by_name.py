from tests import run_async
from tests.engine_tests.unit.storage.user_repo import (
    TestUserRepo,
    user_data
)

from engine.models.user import User

import engine.storage.user_repo as users


class TestGetByName(TestUserRepo):

    @run_async
    async def test_get_user_by_name(self):
        expected_id = user_data[User.__id_attr__]
        expected_name = user_data[User.__name_attr__]

        db = TestGetByName.db
        result = await users.get_by_name(db, expected_name)

        _id = result[User.__id_attr__]
        name = result[User.__name_attr__]

        self.assertIsNotNone(result)
        self.assertEqual(name, expected_name)
        self.assertEqual(_id, expected_id)



