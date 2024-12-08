import requests


def validate_breed(breed):
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    if response.status_code == 200:
        breeds = response.json()
        return any(b["name"].lower() == breed.lower() for b in breeds)
    return False
