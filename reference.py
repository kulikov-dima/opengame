import os
import logging
import csv
from models import Tag, Platform

logger = logging.getLogger(__name__)

CONFIG_DIR = "config"
TAGS_FILE = os.path.join(CONFIG_DIR, "tags.csv")
PLATFORMS_FILE = os.path.join(CONFIG_DIR, "platforms.csv")


def save_tags(data: list[dict]) -> None:
    """Выгружает информацию о доступных тегах в каталоге"""
    if not os.path.exists(TAGS_FILE):
        logger.info(f"Директория {CONFIG_DIR} не найдена и будет создана")
        os.makedirs(CONFIG_DIR)
    with open(TAGS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["slug", "name_singular"], extrasaction='ignore')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    logger.info(f"Записано в файл {TAGS_FILE}, {len(data)} тегов")


def save_platforms(data: list[dict]) -> None:
    """Выгружает информацию о доступных платформах в каталоге"""
    if not os.path.exists(CONFIG_DIR):
        logger.info(f"Директория {CONFIG_DIR} не найдена и будет создана")
        os.makedirs(CONFIG_DIR)
    with open(PLATFORMS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["code", "title"], extrasaction='ignore')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    logger.info(f"Записано в файл {PLATFORMS_FILE}, {len(data)} тегов")


def load_tags() -> list[Tag]:
    with open(TAGS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tags = []
        for row in reader:
            tags.append(
                Tag(slug=row["slug"], name=row["name_singular"])
            )

    logger.debug(f"Прочитано {len(tags)} тегов")
    return tags


def load_platforms() -> list[Platform]:
    with open(PLATFORMS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        platforms = []
        for row in reader:
            platforms.append(
                Platform(code=row["code"], title=row["title"])
            )
    logger.debug(f"Прочитано {len(platforms)} платформ")
    return platforms






if __name__ == "__main__":
    from client import StopGameClient
    from logging_config import BASIC_CONFIG

    logging.basicConfig(**BASIC_CONFIG)
    client = StopGameClient()
    # save_tags(client.fetch_tags())
    # save_platforms(client.fetch_platforms())
    print(load_platforms())

