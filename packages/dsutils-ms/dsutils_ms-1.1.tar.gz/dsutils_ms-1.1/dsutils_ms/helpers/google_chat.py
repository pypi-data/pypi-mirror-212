import requests


def send_message(webhook, message):
    return requests.post(webhook, json={"text": message})
