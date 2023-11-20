from requests import get

failed_ip_req = "-1.-1.-1.-1"


def find_current_ip_address():
    try:
        external_ip = get('https://api.ipify.org').content.decode('utf8')
    except ValueError:
        external_ip = failed_ip_req
        print("Retrieve of external ip did not work")

    return failed_ip_req
