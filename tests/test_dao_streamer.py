from tests.factories import StreamerInFactory


def test_get_item(dao_streamer_test, streamer):
    dao_streamer_test.collection.find_one.return_value = streamer
    result = dao_streamer_test.get_item(streamer["id"])

    assert result == streamer


def test_create_item(dao_streamer_test, streamer_build):
    data_streamer = StreamerInFactory.build()
    data_streamer_dict = data_streamer.dict()

    data = dao_streamer_test.create_item(data_streamer)

    assert data_streamer_dict["id"] == data["id"]
    assert data_streamer_dict["user_id"] == data["user_id"]
    assert data_streamer_dict["game_id"] == data["game_id"]
    assert data_streamer_dict["type"] == data["type"]
    assert data_streamer_dict["viewer_count"] == data["viewer_count"]


def test_update_item(dao_streamer_test, streamer, streamer_build):
    item_id = streamer["id"]
    update_data = streamer_build()

    update_streamer = dao_streamer_test.update_item(item_id, update_data)

    assert update_streamer["id"] == update_data.dict()["id"]
    assert update_streamer["user_id"] == update_data.dict()["user_id"]
    assert update_streamer["game_id"] == update_data.dict()["game_id"]
    assert update_streamer["type"] == update_data.dict()["type"]
    assert update_streamer["viewer_count"] == update_data.dict()["viewer_count"]


def test_delete_item(dao_streamer_test, streamer, streamer_build):
    dao_streamer_test.collection.find_one.return_value = streamer
    result = dao_streamer_test.delete_item(streamer["id"])

    assert result == 1
