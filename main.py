import IpChecker
import RecordUpdater

if __name__ == "__main__":
    current_ip = IpChecker.find_current_ip_address()

    if current_ip == IpChecker.failed_ip_req:
        exit(-1)

    godaddy_ip = IpChecker.find_godaddy_ip()

    if IpChecker.is_same(godaddy_ip, current_ip):
        exit(0)

    RecordUpdater.update_records(current_ip)
