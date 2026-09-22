import time

import requests
import logging

from logging_config import BASIC_CONFIG

logger = logging.getLogger(__name__)


class StopGameClient:
    def __init__(self):
        self.base_url = "https://stopgame.ru/"
        self.headers = {
            "accept": "application/json",
            "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Google Chrome\";v=\"151\", \"Chromium\";v=\"151\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
        }
        self.delay = 1

    def fetch_tags(self) -> list[dict]:
        response = self._get("/ajax/games/tags")
        tags = response.json().get("tags")
        return tags

    def fetch_platforms(self) -> list[dict]:
        response = self._get("/ajax/games/platforms")
        platforms = response.json().get("platforms")
        return platforms

    def fetch_catalog_page(self, tag_slugs: list[str],
                           platform_codes: list[str], page: int = 1) -> str:
        params = {
            "genre[]": tag_slugs,
            "platform[]": platform_codes,
            "p": page,
        }
        html = self._get("/games/catalog", params).text
        return html

    def _get(self, url: str, params: dict | None = None):
        logger.debug(f"GET {url=} {params=}")
        logger.info(f"Вежливо жду {self.delay}с.")
        time.sleep(self.delay)
        response = requests.get(
            self.base_url + url,
        )
        logger.debug(response)

        response.raise_for_status()
        return response


if __name__ == "__main__":
    logging.basicConfig(**BASIC_CONFIG)
    client = StopGameClient()
    print(client.fetch_tags())
