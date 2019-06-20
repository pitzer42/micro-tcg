from tests.engine_tests import run_async
from tests.engine_tests.unit.storage.user_repo import (
    TestUserRepo,
    user_data
)

from engine.storage.user_repo import get_by_id


class TestGetById(TestUserRepo):

    @run_async
    async def test_get_user_by_id(self):
        expected_id = user_data['_id']
        expected_name = user_data['name']
        db = TestGetById._db
        result = await get_by_id(db, expected_id)
        _id = result['_id']
        name = result['name']
        self.assertIsNotNone(result)
        self.assertEqual(name, expected_name)
        self.assertEqual(_id, expected_id)



