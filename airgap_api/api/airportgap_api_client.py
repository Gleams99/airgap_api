from airgap_api.api.api_client import BaseAPIClient


class Airports:
    def __init__(self, *, parent):
        self.parent = parent

    def get(self, *, page: int | None = None, **kwargs):
        endpoint = "airports"
        return self.parent.get(url=endpoint, page=page, **kwargs)

    def get_by_id(self, *, airport_id: str, **kwargs):
        endpoint = f"airports/{airport_id}"
        return self.parent.get(url=endpoint, **kwargs)

    def distance(self, *, from_id: str, to_id: str, **kwargs):
        endpoint = "airports/distance"
        payload = {
            "from": from_id,
            "to": to_id
        }
        return self.parent.post(url=endpoint, json=payload, **kwargs)

    def get_all(self, **kwargs):
        endpoint = "airports"
        return self.parent.get_all_pages(url=endpoint, **kwargs)


class Tokens:
    def __init__(self, *, parent):
        self.parent = parent

    def get(self, *, email: str, password: str, **kwargs):
        endpoint = "tokens"
        payload = {
            "email": email,
            "password": password
        }
        return self.parent.post(url=endpoint, json=payload, **kwargs)


class Favorites:
    def __init__(self, *, parent):
        self.parent = parent

    @staticmethod
    def auth_headers(*, token: str):
        return {
            "Authorization": f"Bearer token={token}"
        }

    def get(self, *, token: str, **kwargs):
        endpoint = "favorites"
        return self.parent.get(url=endpoint, headers=self.auth_headers(token=token), **kwargs)

    def get_by_id(self, *, fav_id: int, token: str, **kwargs):
        endpoint = f"favorites/{fav_id}"
        return self.parent.get(url=endpoint, headers=self.auth_headers(token=token), **kwargs)

    def add(self, *, airport_id: str, note: str = "", token: str, **kwargs):
        endpoint = "favorites"
        payload = {
            "airport_id": airport_id,
            "note": note
        }
        return self.parent.post(url=endpoint, json=payload, headers=self.auth_headers(token=token), **kwargs)

    def update_note(self, *, fav_id: str, note: str = "", token: str, **kwargs):
        endpoint = f"favorites/{fav_id}"
        payload = {
            "note": note
        }
        return self.parent.patch(url=endpoint, json=payload, headers=self.auth_headers(token=token), **kwargs)

    def remove(self, *, fav_id: str, token: str, **kwargs):
        endpoint = f"favorites/{fav_id}"
        return self.parent.delete(url=endpoint, headers=self.auth_headers(token=token), **kwargs)

    def remove_all(self, *, token: str, **kwargs):
        endpoint = "favorites/clear_all"
        return self.parent.delete(url=endpoint, headers=self.auth_headers(token=token), **kwargs)


class AirportGapAPIClient(BaseAPIClient):
    def __init__(self):
        base_url = "https://airportgap.com/api/"
        headers = {
            "Content-Type": "application/json"
        }
        super().__init__(base_url=base_url, headers=headers)

    @property
    def airports(self):
        return Airports(parent=self)

    @property
    def tokens(self):
        return Tokens(parent=self)

    @property
    def favorites(self):
        return Favorites(parent=self)
