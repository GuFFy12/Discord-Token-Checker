import requests, os, ctypes, re
from colorama import Fore
from pathlib import Path
from sys import exit

def cls():
    os.system("cls" if os.name=="nt" else "clear")

def fexit():
    print()
    input(f"{Fore.RESET}Press Enter button for exit.")
    cls()
    exit()

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("Discord Token Checker by GuFFy_OwO")

if not os.path.exists("output"):
    os.makedirs("output")

cls()
print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Check one file")
print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Check many files")
print()
checkType = input(f"{Fore.CYAN}>{Fore.RESET}Select An Option{Fore.CYAN}:{Fore.RESET} ")
if "1" in checkType:
    print()
    tokenFileName = input(f"{Fore.CYAN}>{Fore.RESET}Enter the name of the file in wich are the unchecked tokens{Fore.CYAN}:{Fore.RESET} ")
    checkName = os.path.splitext(os.path.basename(tokenFileName))[0]
elif "2" in checkType:
    print()
    tokenDirectoryName = input(f"{Fore.CYAN}>{Fore.RESET}Enter the directory of the files in wich are the unchecked tokens{Fore.CYAN}:{Fore.RESET} ")
    checkName = os.path.basename(tokenDirectoryName)
    if not os.path.exists(tokenDirectoryName):
        print()
        print(f"{tokenDirectoryName} directory not exist.")
        fexit()
    print()
    print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Check all files")
    print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Enter files formats")
    print()
    ckeckFilesType = input(f"{Fore.CYAN}>{Fore.RESET}Select An Option{Fore.CYAN}:{Fore.RESET} ")
    if "1" in ckeckFilesType:
        None
    elif "2" in ckeckFilesType:
        print()
        fileTypes = ["." + x for x in input(f"{Fore.CYAN}>{Fore.RESET}Enter file types in wich are the unchecked tokens separated by space [txt json html ...]{Fore.CYAN}:{Fore.RESET} ").split()]
    else:
        print()
        print("Invalid Option.")
        fexit()
else:
    print()
    print("Invalid Option.")
    fexit()

print()
checkTokens = input(f"{Fore.CYAN}>{Fore.RESET}Check validity tokens? [Y/N]{Fore.CYAN}:{Fore.RESET} ")
if "y" in checkTokens.lower():
    print()
    checkNitro = input(f"{Fore.CYAN}>{Fore.RESET}Check nitro and payments on tokens? [Y/N]{Fore.CYAN}:{Fore.RESET} ")
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

dirValidTokens = f"output/{checkName}_valid.txt"
dirUnverifiedTokens = f"output/{checkName}_unverified.txt"
dirSameTokens = f"output/{checkName}_sameTokens.txt"
dirInvalidTokens =f"output/{checkName}_invalid.txt"
dirNitroTokens = f"output/{checkName}_nitro.txt"
dirDataTmp = f"output/{checkName}_data.tmp"
dirParsedTokens = f"output/{os.path.basename(checkName)}_parsed.txt"

checked = 0
verified = 0
unverified = 0
sameTokens = 0
invalid = 0
nitro = 0
idlist = []

def main():
    global found
    if "2" in checkType:
        cls()
        try:
            os.remove(dirDataTmp)
        except: None
        print("Glue files...")
        if "1" in ckeckFilesType:
            files = {p.resolve() for p in Path(tokenDirectoryName).glob("**/*.*")}
        elif "2" in ckeckFilesType:
            files = {p.resolve() for p in Path(tokenDirectoryName).glob("**/*") if p.suffix in fileTypes}
        with open(dirDataTmp, "w", encoding="utf-8") as result:
            for file_ in files:
                for line in open( file_, "r", encoding="utf-8", errors="ignore"):
                    result.write(line)
        print()
        print("Done!")
        tokenFileName = dirDataTmp
    print()
    print(f"Parse tokens...")
    try:
        os.remove(dirParsedTokens)
    except: None
    tokens = []
    for line in [x.strip() for x in open(f"{tokenFileName}", errors="ignore").readlines() if x.strip()]:
        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
            for token in re.findall(regex, line):
                tokens.append(token)
    tokens = list(dict.fromkeys(tokens))
    tokens_str = "\n".join(tokens)
    with open(dirParsedTokens, "a", encoding="utf-8") as f:
        f.write(tokens_str)
    found = len(open(dirParsedTokens).readlines())
    print()
    print(f"Done! Found {Fore.CYAN}{found}{Fore.RESET} tokens!")
    try:
        os.remove(dirDataTmp)
    except: None
    if checkTokens.lower() == "y":
        checker()
    else:
        if os.name=="nt":
            os.system(f'start {os.path.realpath("output")}') 
        fexit()   

def checker(): 
    cls()
    try:
        os.remove(dirValidTokens)
        os.remove(dirUnverifiedTokens)
        os.remove(dirInvalidTokens)
        os.remove(dirNitroTokens)
        os.remove(dirSameTokens)
    except: None
    try:
        for item in open(dirParsedTokens, "r").readlines():
            CheckToken(item.strip())
        print()
        if checkNitro.lower() == "y":
            print(f"{Fore.CYAN}Checked{Fore.RESET}: {checked}/{found}  |  {Fore.GREEN}Valid{Fore.RESET}: {verified}  |  {Fore.YELLOW}Unverified{Fore.RESET}: {unverified}  |  {Fore.RED}Invalid{Fore.RESET}: {invalid}  |  {Fore.BLUE}Same Tokens{Fore.RESET}: {sameTokens}  |  {Fore.MAGENTA}NITRO{Fore.RESET}: {nitro}")
        else:
            print(f"{Fore.CYAN}Checked{Fore.RESET}: {checked}/{found}  |  {Fore.GREEN}Valid{Fore.RESET}: {verified}  |  {Fore.YELLOW}Unverified{Fore.RESET}: {unverified}  |  {Fore.RED}Invalid{Fore.RESET}: {invalid}  |  {Fore.BLUE}Same Tokens{Fore.RESET}: {sameTokens}")
        if os.name=="nt":
            os.system(f'start {os.path.realpath("output")}')     
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
        if json_response["id"] not in idlist:
            idlist.append(json_response["id"])
            if json_response["verified"] == True:
                return True
            else:
                return False
        else:
            return "sameToken"
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
    global sameTokens
    global unverified
    global invalid
    global nitro
    if len(token) > 59:
        lenghtToken = f"{token}"
    else:
        lenghtToken = f"{token}                             "
    user_info = get_user_info(token)
    if user_info == "sameToken":
        print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.BLUE}Same User{Fore.RESET}")
        with open(dirSameTokens, "a", encoding="utf-8") as f:
                f.write(token + "\n")
        sameTokens+= 1
    else:
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
    if __name__ == "__main__":
        title()

def title():
    if checkNitro.lower() == "y":
        ctypes.windll.kernel32.SetConsoleTitleW(f"Discord Token Checker by GuFFy_OwO  |  Checked: {checked}/{found}  |  Valid: {verified}  |  Unverified: {unverified}  |  Invalid: {invalid}  |  Same Tokens: {sameTokens}  |  NITRO: {nitro}")
    else:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Discord Token Checker by GuFFy_OwO  |  Checked: {checked}/{found}  |  Valid: {verified}  |  Unverified: {unverified}  |  Invalid: {invalid}  |  Same Tokens: {sameTokens}")

main()
