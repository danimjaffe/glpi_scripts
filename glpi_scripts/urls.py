import urllib.parse


class Urls:
    def __init__(self, ip):
        p = urllib.parse.urlparse(ip, "http")
        netloc = p.netloc or p.path
        path = p.path if p.netloc else ""
        p = urllib.parse.ParseResult("https", netloc, path, *p[3:])

        self.HOME_URL = p.geturl()
        self.BASE_URL = self.HOME_URL + "/apirest.php/"

        # session urls
        self.INIT_URL = self.BASE_URL + "initSession"
        self.KILL_URL = self.BASE_URL + "killSession"

        # computer url
        self.COMPUTER_URL = self.BASE_URL + "Computer/"

        # reservation url
        self.RESERVATION = self.BASE_URL + "Reservation/"

        # user url
        self.USER_URL = self.BASE_URL + "User/"

        # reservation item url
        self.RESERVATION_ITEM = self.BASE_URL + "ReservationItem/"
