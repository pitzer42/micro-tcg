from tests import run_async

from tests.engine_tests.unit.storage.mongo.users import (
    TestUsers,
    user_data
)

from engine.models.user import User


class TestGetById(TestUsers):

    @run_async
    async def test_get_user_by_id(self):
        expected_id = user_data[User._id_attr]
        expected_name = user_data[User._name_attr]

        result = await self.users.get_by_id(expected_id)

        _id = result[User._id_attr]
        name = result[User._name_attr]

        self.assertIsNotNone(result)
        self.assertEqual(name, expected_name)
        self.assertEqual(_id, expected_id)



