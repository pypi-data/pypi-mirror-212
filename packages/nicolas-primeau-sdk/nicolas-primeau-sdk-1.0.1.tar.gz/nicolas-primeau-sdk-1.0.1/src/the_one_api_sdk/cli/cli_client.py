import argparse
import pprint

from the_one_api_sdk import components


class UnknownCommand(Exception):
    pass


class InvalidCommand(Exception):
    pass


def get_client_args():
    parser = argparse.ArgumentParser(
        prog="The One API CLI Client",
        description="Queries the The One API",
    )
    parser.add_argument("command", help="Command", choices=["movies", "quotes"])
    parser.add_argument("subcommand", help="Sub Command", choices=["list", "get"])
    parser.add_argument(
        "-m",
        "--movie-id",
        help="Movie ID, when listing quotes for a movie or to fetch a single movie",
        dest="movie_id",
        required=False
    )
    parser.add_argument("-q", "--quote-id", help="Quote ID", dest="quote_id", required=False)
    parser.add_argument("-l", "--limit", help="Number of items to retrieve", dest="limit", type=int, required=False)
    return parser.parse_args()


def main():
    args = get_client_args()

    match args.command:
        case "movies":
            handle_movie_command(args)
        case "quotes":
            handle_quotes_command(args)
        case _:
            raise UnknownCommand(args.command)


def handle_movie_command(args):
    match args.subcommand:
        case "list":
            for movie in components.TheOneApiSdk().movies.list(limit=args.limit):
                pprint.pprint(movie)
        case "get":
            if not args.movie_id:
                raise InvalidCommand("Movie ID must be specified")
            pprint.pprint(components.TheOneApiSdk().movies(args.movie_id).fetch())
        case _:
            raise UnknownCommand(args.subcommand)


def handle_quotes_command(args):
    match args.subcommand:
        case "list":
            for quote in components.TheOneApiSdk().quotes.list(movie_id=args.movie_id, limit=args.limit):
                pprint.pprint(quote)
        case "get":
            if not args.quote_id:
                raise InvalidCommand("Quote ID must be specified")
            pprint.pprint(components.TheOneApiSdk().quotes(args.quote_id).fetch())
        case _:
            raise UnknownCommand(args.subcommand)
