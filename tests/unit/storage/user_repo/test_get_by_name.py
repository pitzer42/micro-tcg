from tests import run_async
from tests.unit.storage.user_repo import (
    TestUserRepo,
    user_data
)

from micro_tcg.storage.user_repo import get_by_name


class TestGetByName(TestUserRepo):

    @run_async
    async def test_fetch_the_correct_record(self):
        expected_id = user_data['_id']
        expected_name = user_data['name']
        result = await get_by_name(TestGetByName.__db__, expected_name)
        _id = result['_id']
        name = result['name']
        self.assertIsNotNone(result)
        self.assertEqual(name, expected_name)
        self.assertEqual(_id, expected_id)



