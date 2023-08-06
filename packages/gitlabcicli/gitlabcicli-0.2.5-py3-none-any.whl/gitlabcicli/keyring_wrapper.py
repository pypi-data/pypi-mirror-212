import keyring

from .script_helpers import error


class KeyringWrapper:

    _pseudo_user = "_token"

    def __init__(self, service_name: str = "gitlabcicli"):
        self._service_name = service_name

    def _get_keyring_username(self, server_url: str) -> str:
        return f"{self._pseudo_user}:{server_url}"

    def get_token(self, server_url: str) -> str | None:
        try:
            return keyring.get_password(
                self._service_name, self._get_keyring_username(server_url)
            )
        except keyring.errors.KeyringError as err:
            error(
                f"Failed to get token for {server_url} from keyring: {err!s}",
                exit_code=500,
            )

            return None

    def set_token(self, server_url: str, token: str) -> None:
        try:
            keyring.set_password(
                self._service_name,
                self._get_keyring_username(server_url),
                token,
            )
        except keyring.errors.KeyringError as err:
            error(f"Failed to save token in keyring: {err!s}", exit_code=500)
