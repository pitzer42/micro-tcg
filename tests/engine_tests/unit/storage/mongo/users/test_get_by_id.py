from tests import run_async

from tests.engine_tests.unit.storage.mongo.users import (
    TestUsers,
    user_data
)

from engine.repos.schemas.user import (
    uid_attr,
    name_attr
)


class TestGetById(TestUsers):

    @run_async
    async def test_get_user_by_id(self):
        expected_id = user_data[uid_attr]
        expected_name = user_data[name_attr]

        result = await self.users.get_by_id(expected_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.uid, expected_id)



