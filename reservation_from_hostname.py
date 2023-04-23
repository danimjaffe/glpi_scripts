import argparse
from sessionHandler import SessionHandler
from urls import Urls
from utils import get_reservation_from_host


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--ip",
        metavar="ip",
        type=str,
        required=True,
        help='the IP of the GLPI instance ip',
    )
    parser.add_argument(
        "-t",
        "--token",
        metavar="user_token",
        type=str,
        required=True,
        help="the user token string for authentication with GLPI",
    )

    parser.add_argument(
        "-H",
        "--host",
        metavar="host_name",
        type=str,
        required=True,
        help="the desired hostname",
    )

    args = parser.parse_args()
    urls = Urls(args.ip)

    with SessionHandler(args.token, urls) as session:
        get_reservation_from_host(urls, session, args.host)


if __name__ == "__main__":
    main()
