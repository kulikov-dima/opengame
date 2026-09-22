import argparse
import logging
import reference
from client import StopGameClient
from reference import save_platforms, save_tags, load_tags, load_platforms
import difflib
from bs4 import BeautifulSoup

from logging_config import BASIC_CONFIG

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Уровень сообщений в логе",
    )
    parser = argparse.ArgumentParser(
        prog="stopgame",
        description="Каталог игр StopGame из командной строки",
        parents=[common_parser]
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("update", help="скачать справочники жанров и платформ", parents=[common_parser])

    p_genres = subparsers.add_parser("genres", help="показать доступные жанры", parents=[common_parser])
    p_genres.add_argument("--save", metavar="ФАЙЛ", help="записать список в файл")

    p_platforms = subparsers.add_parser("platforms", help="показать доступные платформы", parents=[common_parser])
    p_platforms.add_argument("--save", metavar="ФАЙЛ", help="записать список в файл")

    p_games = subparsers.add_parser("games", help="загрузить игры по фильтрам", parents=[common_parser])
    p_games.add_argument("--genres", nargs="+", metavar="ЖАНР",
                         help="жанры, темы, режимы (как на сайте)", default=[])
    p_games.add_argument("--platforms", nargs="+", metavar="ПЛАТФОРМА",
                         help="платформы (как на сайте)", default=[])
    p_games.add_argument("--pages", type=int, default=1, help="сколько страниц скачать")
    p_games.add_argument("--out", default="games.csv", help="куда сохранить результат")

    return parser


def cmd_update(args):
    logger.info(f"Команда update {args}")
    client = StopGameClient()
    save_tags(client.fetch_tags())
    save_platforms(client.fetch_platforms())


def cmd_genres(args):
    logger.info(f"Команда genres {args}")
    tags = load_tags()
    tags = sorted(tags, key=lambda t: t.name)
    print(*tags, sep='\n')


def cmd_platforms(args):
    logger.info(f"Команда platforms {args}")
    platforms = load_platforms()
    platforms = sorted(platforms, key=lambda p: p.title)
    print(*platforms, sep='\n')


def cmd_games(args):
    logger.info(f"Команда games {args}")
    platforms = reference.load_platforms()
    tags = reference.load_tags()

    have_input_error = False
    platform_codes = []
    platform_possibilities = [p.code for p in platforms] + [p.title for p in platforms]
    tag_slugs = []
    tag_possibilities = [t.slug for t in tags] + [t.name for t in tags]
    for user_input in args.platforms:
        for platform in platforms:
            if platform.matches(user_input):
                platform_codes.append(platform.code)
                break
        else:
            have_input_error = True
            print(f"Не найдена платформа {user_input}")
            # не нашли то что ввел пользователь
            matches = difflib.get_close_matches(user_input, platform_possibilities, cutoff=0.5)
            if matches:
                # есть похожее
                print(f"Возможно вы имели ввиду {matches[0]}?")


    for user_input in args.genres:
        for tag in tags:
            if tag.matches(user_input):
                tag_slugs.append(tag.slug)
                break
        else:
            have_input_error = True
            print(f"Не найден тег {user_input}")
            # не нашли то что ввел пользователь
            matches = difflib.get_close_matches(user_input, tag_possibilities, cutoff=0.5)
            if matches:
                # есть похожее
                print(f"Возможно вы имели ввиду {matches[0]}?")
    if have_input_error:
        exit()
    logger.debug(f"{platform_codes=}, {tag_slugs=}")

    client = StopGameClient()
    page = client.fetch_catalog_page(tag_slugs=tag_slugs, platform_codes=platform_codes)
    soup = BeautifulSoup(page, "html.parser")
    # print(soup.prettify())
    links = soup.find_all("a")
    game_links = list(filter(lambda l: l.has_attr("data-game-card"), links))
    game_hrefs = list(map(lambda l: l.attrs["href"], game_links))
    print(game_hrefs)




def main():
    commands = {
        "update": cmd_update,
        "genres": cmd_genres,
        "platforms": cmd_platforms,
        "games": cmd_games,
    }
    parser = build_parser()
    args = parser.parse_args()

    BASIC_CONFIG["level"] = args.log_level
    logging.basicConfig(
        **BASIC_CONFIG,
    )

    func = commands[args.command]  # выбираем функцию по имени команды
    func(args)


if __name__ == "__main__":
    main()
