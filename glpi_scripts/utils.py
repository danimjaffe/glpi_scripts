import pandas as pd
from datetime import datetime
from glpi_scripts.urls import Urls
from requests.sessions import Session


def check_fields(session: Session, url: str) -> list:
    """Method for getting the glpi fields at the given url

    Args:
        session (Session object): The requests session object
        url (str): The url to get the fields

    Returns:
        glpi_fields_list (list): The list of glpi fields at the URL
    """
    glpi_fields_list = []
    api_range = 0
    api_increment = 50
    more_fields = True
    while more_fields:
        range_url = (
                url + "?range=" + str(api_range) + "-" + str(api_range + api_increment)
        )
        glpi_fields = session.get(url=range_url)
        if glpi_fields.json() and glpi_fields.json()[0] == "ERROR_RANGE_EXCEED_TOTAL":
            more_fields = False
        else:
            glpi_fields_list.append(glpi_fields)
            api_range += api_increment
    return glpi_fields_list


def get_reservation_from_host(urls: Urls, session: Session, hostname: str) -> None:
    """Method for checking if a host is reserved in GLPI system if the hostname is reserved prints the following
    information: reservation id, user who created the reservation, end time of the reservation, comment related to
    the reservation

        Args:
            urls: (Urls object)
            session (Session object): The requests session object
            hostname: the hostname which we want to search if it is reserved

        Returns:
            None
        """
    output = ""
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    reservations_json = check_fields(session, urls.RESERVATION)
    for reservation_list in reservations_json:
        for reservation in reservation_list.json():
            reservationitems_id = str(reservation["reservationitems_id"])
            reservation_item = session.get(url=urls.RESERVATION_ITEM + reservationitems_id)
            reservation_item = reservation_item.json()
            if reservation_item["itemtype"] == "Computer":
                glpi_hostid = str(reservation_item["items_id"])
                computer = session.get(url=urls.COMPUTER_URL + glpi_hostid)
                computer = computer.json()
                if computer["name"] == hostname and reservation["end"] > dt_string:
                    user_id = str(reservation["users_id"])
                    user = session.get(url=urls.USER_URL + user_id)
                    user = user.json()
                    output += "Reservation {reservation_id}:\n".format(reservation_id=reservation["id"])
                    output += "\tUser: {user_name}\n".format(user_name=user["name"])
                    output += "\tComputer: {host_name}\n".format(host_name=hostname)
                    output += "\tEnds: {ends}\n".format(ends=reservation["end"])
                    output += "\tcomment: {comment}\n".format(comment=reservation["comment"])

    if output:
        print(output)
    else:
        print("No reservation found with hostname {hostname}".format(hostname=hostname))
    return


def get_reservations_from_user(urls: Urls, session: Session, username: str) -> list:
    """Method that returns all hosts related to a user.

         Args:
             urls: (Urls object)
             session (Session object): The requests session object
             username: the username which we want to search all related hosts

         Returns:
             all hosts related to a user. Returns an empty list if no related hosts.
         """
    reserved_hosts = []
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    reservations_json = check_fields(session, urls.RESERVATION)
    for reservation_list in reservations_json:
        for reservation in reservation_list.json():
            reservationitems_id = str(reservation["reservationitems_id"])
            reservation_item = session.get(url=urls.RESERVATION_ITEM + reservationitems_id)
            reservation_item = reservation_item.json()
            if reservation_item["itemtype"] == "Computer":
                user_id = str(reservation["users_id"])
                user = session.get(url=urls.USER_URL + user_id)
                user = user.json()
                if user["name"] == username and reservation["end"] > dt_string:
                    glpi_hostid = str(reservation_item["items_id"])
                    computer = session.get(url=urls.COMPUTER_URL + glpi_hostid)
                    computer = computer.json()
                    reserved_host = ""
                    reserved_host += "Reservation {reservation_id}:\n".format(reservation_id=reservation["id"])
                    reserved_host += "\tUser: {user_name}\n".format(user_name=user["name"])
                    reserved_host += "\tComputer: {host_name}\n".format(host_name=computer["name"])
                    reserved_host += "\tEnds: {ends}\n".format(ends=reservation["end"])
                    reserved_host += "\tcomment: {comment}\n".format(comment=reservation["comment"])
                    reserved_hosts.append(reserved_host)

    return reserved_hosts


def hostid_to_hostname(urls: Urls, session: Session, path: str = "") -> None:
    """Mapping between computer ids in GLPI system to hostnames

    Args:
        urls: (Urls object)
        session: (Session object)
        path: (Path to save the file)

    Returns:
        Writes a csv with the mapping between computer ids in GLPI system to hostnames named path + "hostid_to_hostname.csv"
    """
    glpi_hostid = "glpi_hostid"
    host_name = "host_name"
    rows_list = []
    csv_name = path + "hostid_to_hostname.csv"
    computer_json = check_fields(session, urls.COMPUTER_URL)
    for computer_list in computer_json:
        for computer in computer_list.json():
            row = {}
            row.update([(glpi_hostid, computer["id"]), (host_name, computer["name"])])
            rows_list.append(row)

    df = pd.DataFrame(rows_list)
    df.to_csv(csv_name, index=False)
