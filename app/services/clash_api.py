import os
import requests
from dotenv import load_dotenv
from app.logger import get_logger

logger = get_logger("clash_api")

_override_api_key = None

def set_override_api_key(key: str | None):
    global _override_api_key
    _override_api_key = key
    logger.info("ClashAPI override key %s", "set" if key else "cleared")

def _resolve_api_key():
    if _override_api_key:
        return _override_api_key
    load_dotenv()
    return os.getenv("CR_API_KEY")

class ClashAPI:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://api.clashroyale.com/v1"
        self.api_key = _resolve_api_key()
        logger.info("ClashAPI initialized")

    def _get(self, url, endpoint_name=""):
        self.api_key = _resolve_api_key()
        headers = {"Authorization": f"Bearer {self.api_key}"}
        logger.debug("Calling %s: %s", endpoint_name, url)
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if not resp.ok:
                err = resp.json()
                msg = err.get("reason", err.get("message", "unknown error"))
                logger.error("%s failed with status %d: %s", endpoint_name, resp.status_code, msg)
                raise Exception(f"API error {resp.status_code}: {msg}")
            data = resp.json()
            logger.info("%s returned %d items", endpoint_name, len(data) if isinstance(data, list) else 1)
            return data
        except Exception as e:
            logger.error("%s failed: %s", endpoint_name, str(e))
            raise

    def get_player(self, tag: str):
        tag = tag.replace("#", "%23")
        return self._get(f"{self.base_url}/players/{tag}", "get_player")

    def get_player_cards(self, tag: str):
        tag = tag.replace("#", "%23")
        return self._get(f"{self.base_url}/players/{tag}", "get_player_cards")

    def get_recent_battles(self, tag: str):
        tag = tag.replace("#", "%23")
        return self._get(f"{self.base_url}/players/{tag}/battlelog", "get_recent_battles")

    def get_clan(self, tag: str):
        tag = tag.replace("#", "%23")
        return self._get(f"{self.base_url}/clans/{tag}", "get_clan")
