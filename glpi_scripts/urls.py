import urllib.parse


# TODO: fix adjust this file with commnets and only vales needed
class Urls:
    def __init__(self, ip):
        p = urllib.parse.urlparse(ip, "http")
        netloc = p.netloc or p.path
        path = p.path if p.netloc else ""
        p = urllib.parse.ParseResult("https", netloc, path, *p[3:])
        self.HOME_URL = p.geturl()
        self.BASE_URL = self.HOME_URL + "/apirest.php/"
        self.INIT_URL = self.BASE_URL + "initSession"
        self.KILL_URL = self.BASE_URL + "killSession"

        self.SEARCH_URL = self.BASE_URL + "search/"
        self.SEARCH_COMPUTER_URL = self.SEARCH_URL + "Computer/"

        self.COMPUTER_URL = self.BASE_URL + "Computer/"
        self.RESERVATION = self.BASE_URL + "Reservation/"

        self.SEARCH_OPTIONS = self.BASE_URL + "listSearchOptions/"
        self.SEARCH_OPTIONS_COMPUTER = self.SEARCH_OPTIONS + "Computer/"

        self.USER_URL = self.BASE_URL + "User/"

        self.RESERVATION_ITEM = self.BASE_URL + "ReservationItem/"
