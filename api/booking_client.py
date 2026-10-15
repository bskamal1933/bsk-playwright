from playwright.sync_api import APIResponse

from api.base_client import BaseClient


class BookingClient(BaseClient):
    """Client for https://restful-booker.herokuapp.com (public practice API)."""

    def health(self) -> APIResponse:
        return self._send("GET", "/ping")

    def create_token(self, username: str, password: str) -> APIResponse:
        return self._send("POST", "/auth", data={"username": username, "password": password})

    def get_booking_ids(self, **filters) -> APIResponse:
        return self._send("GET", "/booking", params=filters or None)

    def get_booking(self, booking_id: int) -> APIResponse:
        return self._send("GET", f"/booking/{booking_id}")

    def create_booking(self, payload: dict) -> APIResponse:
        return self._send("POST", "/booking", data=payload)

    def update_booking(self, booking_id: int, payload: dict, token: str | None) -> APIResponse:
        return self._send("PUT", f"/booking/{booking_id}", data=payload, headers=self._auth(token))

    def patch_booking(self, booking_id: int, fields: dict, token: str | None) -> APIResponse:
        return self._send("PATCH", f"/booking/{booking_id}", data=fields, headers=self._auth(token))

    def delete_booking(self, booking_id: int, token: str | None) -> APIResponse:
        return self._send("DELETE", f"/booking/{booking_id}", headers=self._auth(token))

    @staticmethod
    def _auth(token: str | None) -> dict:
        # Static method: pure helper, needs neither self nor cls.
        return {"Cookie": f"token={token}"} if token else {}
