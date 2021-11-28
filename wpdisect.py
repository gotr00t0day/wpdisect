from colorama import Fore
from builtwith import builtwith
import os
import requests
import concurrent.futures
import json

banner = f"""



██╗    ██╗██████╗ ██████╗ ██╗███████╗███████╗ ██████╗████████╗    
██║    ██║██╔══██╗██╔══██╗██║██╔════╝██╔════╝██╔════╝╚══██╔══╝    
██║ █╗ ██║██████╔╝██║  ██║██║███████╗█████╗  ██║        ██║       
██║███╗██║██╔═══╝ ██║  ██║██║╚════██║██╔══╝  ██║        ██║       
╚███╔███╔╝██║     ██████╔╝██║███████║███████╗╚██████╗   ██║       
 ╚══╝╚══╝ ╚═╝     ╚═════╝ ╚═╝╚══════╝╚══════╝ ╚═════╝   ╚═╝
                            {Fore.CYAN} V1.0

                        {Fore.WHITE}Author:   {Fore.CYAN}c0d3Ninja
                        {Fore.WHITE}IG:      {Fore.CYAN} @gotr00t0day
                        {Fore.WHITE}GitHub:   {Fore.CYAN}gotr00t0day



"""

# Target to scan

target = "http://blog.thm"

# wpdisect current directory

filepath = os.path.abspath(os.getcwd())

# Medium Payload list

with open(f"{filepath}/Payloads/medium_payload.txt", "r") as m:
    Medium_payload = (x.strip() for x in m.readlines())

# Small Payload List

with open(f"{filepath}/Payloads/small_payload.txt", "r") as s:
    Small_payload = (x.strip() for x in  s.readlines())
    

Filter_Out = [".jpg", ".css", ".png", "gif"]

# Fecth the Wordpress Directory

current_directory = os.getcwd()
os.chdir(f"{current_directory}/wordpress")
path2 = []

# Scans the wordpress directory thoroughly 

for root, _, files in os.walk("."):
    for fname in files:
        if os.path.splitext(fname)[1] in Filter_Out:
            continue
        path = os.path.join(root, fname)
        if path.startswith("."):
            path = path[1:]
            path2.append(path)

def get_requests(url: str):
    s = requests.Session()
    r = s.get(f"{url}")
    if r.status_code == 200:
        print(f"{Fore.Green} Found {Fore.CYAN} - {Fore.WHITE} {url} {Fore.GREEN} [{r.status_code}]")
    else:
        if r.status_code == 403:
            print(f"{Fore.GREEN} [STATUS] {Fore.CYAN} - {Fore.WHITE} {url} {Fore.RED} [{r.status_code}]")
        else:
            print(f"{Fore.GREEN} [STATUS] {Fore.CYAN} - {Fore.WHITE} {url} {Fore.BLUE} [{r.status_code}]")


def Thorough_Scan(path2):
    check = "".join((target, path2))
    get_requests(check)

def Medium_Scan(Medium_payload):
    check = "".join((f"{target}/{Medium_payload}"))
    get_requests(check)

def Small_Scan(Small_payload):
    check = "".join((f"{target}/{Small_payload}"))
    get_requests(check)

# Scan for wordpress
def Wordpress_Scan(target):
    try:
        print("\n")
        print(Fore.CYAN + "Checking fo wordpress..." + "\n")
        info = builtwith(f"{target}")
        cms = info["cms"]
        blog = info["blogs"]
        if "WordPress" in cms and blog:
            print("Found Wordpress Installation..")
        else:
            print("I couldn't find the WordPress blog")        
    except UnicodeDecodeError:
        pass

def Users():
    r = requests.get(f"{target}/wp-json/wp/v2/users")
    json = r.json()
    for data in json:
        print()
        print(f"{data['name']}: {data['link']}")



def start():
    while True: 
        print(banner)
        print()
        print (Fore.CYAN + "[" + Fore.WHITE + "01" + Fore.CYAN + "] " + Fore.WHITE + "Check For Wordpress")
        print (Fore.CYAN + "[" + Fore.WHITE + "02" + Fore.CYAN+ "] " + Fore.WHITE + "Thorough Scan")
        print (Fore.CYAN + "[" + Fore.WHITE+ "03" + Fore.CYAN + "] " + Fore.WHITE + "Medium Scan")
        print (Fore.CYAN + "[" + Fore.WHITE + "04" + Fore.CYAN + "] " + Fore.WHITE + "Small Scan")
        print (Fore.CYAN + "[" + Fore.WHITE + "05" + Fore.CYAN + "] " + Fore.WHITE + "Users")
        print ("\n")
        prompt = input(Fore.WHITE + "WPDisect~" + Fore.WHITE + "# ")
        if prompt == "1":
            Wordpress_Scan(target)
        if prompt == "2":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(Thorough_Scan, path2)
        if prompt == "3":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(Medium_Scan, Medium_payload)
        if prompt == "4":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(Small_Scan, Small_payload)
        if prompt == "5":
            Users()



if __name__ == "__main__":
    start()