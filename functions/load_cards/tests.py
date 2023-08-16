import base64
import main
import json
from unittest import mock


class AmountMessage:
    def __init__(self, amount):
        self.data


def test_get_card_ids():
    card_ids = main.get_card_ids()
    assert isinstance(card_ids, list)


def test_load_cards():
    data = base64.b64encode(json.dumps({"amount": 1}).encode())
    mock_event = mock.Mock()
    mock_event.data = {"message": {"data": data}}
    main.load_cards(mock_event)
