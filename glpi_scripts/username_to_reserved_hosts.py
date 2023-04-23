import argparse
from glpi_scripts.urls import Urls
from glpi_scripts.sessionHandler import SessionHandler
from glpi_scripts.utils import get_reservations_from_user


def main():
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
        "-u",
        "--user",
        metavar="user",
        type=str,
        required=False,
        help="the username that we want to get all the reserved hosts related to him",
    )
    args = parser.parse_args()
    urls = Urls(args.ip)
    with SessionHandler(args.token, urls) as session:
        reserved_hosts = get_reservations_from_user(urls, session, args.user)
        for host in reserved_hosts:
            print(host)


if __name__ == "__main__":
    main()
