import argparse
import logging
import reference
from build_parser import build_parser
from client import StopGameClient
from web import app as web

from logging_config import BASIC_CONFIG

logger = logging.getLogger(__name__)



def cmd_update(args):
    logger.info(f"command update {args}")
    client = StopGameClient()
    tags_json = client.fetch_tags()
    res_tags = []
    for tag in tags_json:
        res_tags.append(tag)
    reference.save_tags(res_tags)
    platforms_json = client.fetch_platforms()
    res_platforms = []
    for platform in platforms_json:
        res_platforms.append(platform)
    reference.save_platforms(res_platforms)

def cmd_genres(args):
    logger.info(f"command genres {args}")


def cmd_platforms(args):
    logger.info(f"command platforms {args}")


def cmd_games(args):

    platforms = reference.load_platforms()
    platform_codes = []
    for user_input in args.platforms:
        for platform in platforms:
            if platform.matches(user_input):
                platform_codes.append(platform.code)

    tags = reference.load_tags()
    tag_slugs = []
    for user_input in args.genres:
        for tag in tags:
            if tag.matches(user_input):
                tag_slugs.append(tag.slug)

    logger.debug(f"{platform_codes=}, {tag_slugs=}")

    resp = reference.get_games(page=args.pages, verbose=args.verbose, tags=tag_slugs, platforms=platform_codes, args=args)
def cmd_web(args):
    logger.info(f"Open{' not' if not args.threaded else ''} threaded web-server at {args.host}:{args.port}")
    web.main(args.host, args.port, args.threaded, args.debug)
    logger.info(f"Open{' not' if not args.threaded else ''} threaded web-server at {args.host}:{args.port}")
def main():
    commands = {
        "update": cmd_update,
        "genres": cmd_genres,
        "platforms": cmd_platforms,
        "games": cmd_games,
        "web": cmd_web
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
