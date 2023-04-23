import argparse
from urls import Urls
from sessionHandler import SessionHandler
from utils import hostid_to_hostname


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
        "-p",
        "--path",
        metavar="path",
        type=str,
        required=False,
        help="the path to save the file",
    )
    args = parser.parse_args()
    urls = Urls(args.ip)
    with SessionHandler(args.token, urls) as session:
        hostid_to_hostname(urls, session)


if __name__ == "__main__":
    main()
