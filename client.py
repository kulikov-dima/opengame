from bs4 import BeautifulSoup
import time
from models import Game
import requests
import logging
import re

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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        }
        self.delay = 0.2

    def fetch_tags(self) -> list[dict]:
        response = self._get("/ajax/games/tags")
        tags = response.json().get("tags")
        return tags

    def fetch_platforms(self) -> list[dict]:
        response = self._get("/ajax/games/platforms")
        platforms = response.json().get("platforms")
        return platforms

    def fetch_catalog_page(
        self, tag_slugs: list[str], platform_codes: list[str], page: int = 1
    ) -> str:
        logger.info("Гружу страницу каталог")
        params = {
            "genre[]": tag_slugs,
            "platform[]": platform_codes,
            "p": page,
        }
        html = self._get("/games/catalog", params).text
        return html

    def fetch_game_page(self, url) -> str:
        logger.info("Гружу страницу игры")
        html = self._get(url).text
        return html

    @staticmethod
    def extract_game_hrefs(html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")

        game_links = list(filter(lambda l: l.has_attr("data-game-card"), links))
        game_hrefs = list(map(lambda l: l.attrs["href"], game_links))
        logger.debug("Found %d links", len(game_hrefs))
        return game_hrefs

    @staticmethod
    def parse_game_page(html) -> Game:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("h1", class_=re.compile(r"^_game-title_")).text
        rating = soup.find("span", class_=re.compile(r"^_game-rating_"))
        tags_container = soup.find("div", class_=re.compile(r"^_tag-list"))
        tags_a = tags_container.find_all("a")
        platforms_label = soup.find("dt", string="Платформы")
        platforms_container = platforms_label.find_next("dd")
        platforms_a = platforms_container.find_all("a")
        tags = []
        for link in tags_a:
            tags.append(link.attrs['href'].split('/')[-1])

        platforms = []
        for link in platforms_a:
            platforms.append(link.attrs['href'].split('/')[-1])

        if rating:
            rating = rating.text

        year = soup.find("dd").text
        logger.debug(f"{title=}")
        logger.debug(f"{rating=}")
        logger.debug(f"{tags=}")
        logger.debug(f"{platforms=}")
        logger.debug(f"{year=}")
        return Game(name=title, year=year, rating=rating, platforms="~".join(platforms), tags="~".join(tags))

    def _get(self, url: str, params: dict | None = None):
        logger.debug(f"GET {url=} {params=}")
        logger.debug(f"Вежливо жду {self.delay}с.")
        time.sleep(self.delay)
        response = requests.get(
            self.base_url + url,
        )
        logger.debug(response)

        response.raise_for_status()
        return response


if __name__ == "__main__":
    logging.basicConfig(**BASIC_CONFIG)
    logging.basicConfig(level='debug')
    client = StopGameClient()
    html = client._get('game/grand_theft_auto_5').text
    client.parse_game_page(html)
