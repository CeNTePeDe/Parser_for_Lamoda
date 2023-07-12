import logging

logger = logging.getLogger(__name__)


def test_get_item(dao_streamer_test, streamer):
    dao_streamer_test.collection.find_one.return_value = streamer
    result = dao_streamer_test.get_item(streamer["id"])

    assert result == streamer


def test_create_item(dao_streamer_test, streamer_build, streamer):
    data_streamer = streamer_build()
    data_streamer_dict = data_streamer.dict()
    dao_streamer_test.collection.find_one.return_value = data_streamer_dict

    data = dao_streamer_test.create_item(data_streamer)

    assert data_streamer_dict["id"] == data["id"]
    assert data_streamer_dict["user_id"] == data["user_id"]


def test_update_item(dao_streamer_test, streamer, streamer_build):
    item_id = streamer["id"]
    update_data = streamer_build()
    dao_streamer_test.collection.update_one.return_value.modified_count = 1
    count = dao_streamer_test.update_item(item_id, update_data)

    assert count == 1


def test_delete_item(dao_streamer_test, streamer):
    item_id = streamer["id"]
    dao_streamer_test.collection.delete_one.return_value.deleted_count = 1
    result = dao_streamer_test.delete_item(item_id)
    dao_streamer_test.collection.delete_one.assert_called_once_with({"id": item_id})

    assert result == 1
