import subprocess
import json
import getpass
import time

print("Enter your moodle username and password")
username = input("Username: ")
password = getpass.getpass()

subprocess.run("rm moodle.json", 
               shell=True, 
               stdout=subprocess.DEVNULL,
               )
subprocess.run("scrapy crawl moodle -o moodle.json -a u='{}' -a p='{}'".format(username, password), 
               shell=True, 
               stdout=subprocess.DEVNULL, 
               stderr=subprocess.DEVNULL,
               )
try:
    moodle = open('moodle.json')
    data = json.loads(moodle.read())
    while True:
        print('\n'*100)
        for entry in data:
            name = entry['name']
            date = entry['date']
            date = int(date)
            date = date - time.time()
            m, s = divmod(date, 60)
            h, m = divmod(m, 60)
            if date > 0:
                print('{:40.40}  {}:{:0>2}:{:0>2}\n'.format(name, int(h), int(m), int(s)))
        time.sleep(1)
except:
    print('Error.')
