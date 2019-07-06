from tests import run_async

from tests.engine_tests.unit.storage.mongo.users import (
    TestUsers,
    user_data
)

from engine.models.user import User


class TestGetById(TestUsers):

    @run_async
    async def test_get_user_by_id(self):
        expected_id = user_data[User.__id_attr__]
        expected_name = user_data[User.__name_attr__]

        result = await self.users.get_by_id(expected_id)

        _id = result[User.__id_attr__]
        name = result[User.__name_attr__]

        self.assertIsNotNone(result)
        self.assertEqual(name, expected_name)
        self.assertEqual(_id, expected_id)



