from datetime import datetime
import os
import logging
import csv
from models import Tag, Platform, Game
from client import StopGameClient
from bs4 import BeautifulSoup as bs
import models
from build_parser import build_parser
import csv

logger = logging.getLogger(__name__)

CONFIG_DIR = "config"
TAGS_FILE = os.path.join(CONFIG_DIR, "tags.csv")
PLATFORMS_FILE = os.path.join(CONFIG_DIR, "platforms.csv")

def export_games(games: list[Game], output="games.csv") -> str:
    games_headers = [
        "Ссылка",
        "Название",
        "Дата выхода",
        "Рейтинг"
    ]
    with open(output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=games_headers, extrasaction='ignore')
        writer.writeheader()
        result_dict = []
        for game in games:
            result_dict.append(
                {
                    "Ссылка": game.url,
                    "Название": game.name,
                    "Дата выхода": game.year,
                    "Рейтинг": game.rating
                }
            )
        writer.writerows(result_dict)
    return os.path.abspath(output)
def save_tags(data: list[dict]) -> None:
    """Выгружает информацию о доступных тегах в каталоге"""
    if not os.path.exists(TAGS_FILE):
        logger.info(f"Директория {CONFIG_DIR} не найдена и будет создана")
        os.makedirs(CONFIG_DIR, exist_ok=True)
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

# def find_tag(user_input: str, tags: list[Tag]) -> Tag:

def get_games(page: str = 1, tags: list = None, platforms: list = None, verbose: bool = False, count: int = 10, args: str = build_parser().parse_args()) -> list[Game]:
    client = StopGameClient()
    parser = build_parser()
    resp: list = list([])
    zzzzzzz = False
    verbose = True
    for w in range(page):
        params = {
            "p": w + 1
        }
        if tags: params['tags'] = tags
        if platforms: params['platforms'] = platforms
        #print(params)
        response = client._get("/games/catalog", params=params)
        if response["status"] == 0:
            html = response["content"].text
        else:
            logger.warning(f"Ошибка {response["error"]["type"]}: {response['error']['message']}")
            html = None
        #print(params)
        #print(response["content"].url)

        if html:
            print(response["content"].url)
            soup = bs(html, "html.parser")
            games_class = soup.find("div", class_="list-view _section-with-pagination_82nn8_509").find("div", class_="_games-grid_fl71g_283")
            games_all = soup.find_all("div")
            games_parsed = 0
            for i in range(len(games_all)):
                game = games_all[i]
                if game.get("data-key"):
                    #print(type(games_all[i]))
                    a = games_all[i].find_all("a")
                    #print(f"\nGame №{i + 1}:")
                    #print(f"    {a[0]['href']}")
                    url = a[0]['href']
                    res = client._get(url, None)
                    if res["status"] == 0:
                        soup = bs(res["content"].text, "html.parser")
                        #print(url)

                        result = info_by_soup(soup, show=verbose, url=url)
                        resp.append(result)
                        games_parsed += 1
                        if games_parsed >= count:
                            zzzzzzz = True
                            break
                        else:
                            zzzzzzz = False


            if not zzzzzzz:
                break
    if args.out:
        export_games(resp, args.out)
    return resp
                    
def info_by_soup(soup, show: bool = False, _step: str = "", _start: str = "\n", url: str = '') -> models.Game:
    date_of_out = soup.find("div", class_="_game-info_1bso0_696").find("dl", class_="_game-info__grid_1bso0_993").find_all("dd")[0].text
    name = soup.find('h1', class_="_game-title_1bso0_702").text
    try:
        rating = soup.find("div", class_="_left-column__user-ratings_1bso0_1").find("span").text
    except AttributeError:
        rating = "Отсутствует"
    if show:
        print(f"{_start}{_step}Информация о игре {name}:")    
        print(f"{_step}    Имя: {name}")
        print(f"{_step}    Дата выхода: {date_of_out}")
        print(f'{_step}    Рейтинг: {rating}')
    return models.Game(url, name, year=date_of_out, rating=rating)
if __name__ == "__main__":
    # from client import StopGameClient
    # from logging_config import BASIC_CONFIG
    #
    # logging.basicConfig(**BASIC_CONFIG)
    # client = StopGameClient()
    # # save_tags(client.fetch_tags())
    # # save_platforms(client.fetch_platforms())
    # print(load_platforms())
    get_games()