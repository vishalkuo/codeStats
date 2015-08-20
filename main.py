import requests, getpass

name = raw_input("Enter your Github username: ")
password = getpass.getpass("Enter your Github password: ")
r = requests.get('https://api.github.com', auth=(name, password))
while r.status_code != 200:
    print("Bad Credentials!")
    name = raw_input("Enter your Github username: ")
    password = getpass.getpass("Enter your Github password: ")
    r = requests.get('https://api.github.com', auth=(name, password))

