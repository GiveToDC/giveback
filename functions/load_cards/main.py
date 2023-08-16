import base64
import functions_framework
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv("../../.env")  # Load environment variables if being tested locally
bearer_token = f'Bearer {os.getenv("BEARER_TOKEN")}'


@functions_framework.cloud_event
def load_cards(cloud_event):
    data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode())
    payload = {"cardIds": get_card_ids(), "amount": data["amount"]}
    url = "https://api.dev.givecard.dev/api/v1/cards/load"
    headers = {
        "accept": "*/*",
        "Authorization": bearer_token,
        "content-type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)


def get_card_ids():
    url = "https://api.dev.givecard.dev/api/v1/cards"
    headers = {
        "accept": "*/*",
        "Authorization": bearer_token,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)

    cards = response.json()["cards"]
    card_ids = list(map(lambda card: card["id"], cards))
    return card_ids
