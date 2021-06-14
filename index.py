import requests, colorama, os
from colorama import Fore, init

init()

def doIntro():
    os.system("cls")
if __name__ == '__main__':
    os.system('cls')
    os.system('title Discord Token Checker by GuFFy_OwO')
    colorama.init()

print(f"{Fore.MAGENTA}Discord Token Checker by GuFFy_OwO")
tokenFileName = input(f"{Fore.GREEN}Enter the name of the file in wich are the unchecked tokens (without .txt) : ")
checkNitro = input(f"{Fore.GREEN}Check nitro and payments on tokens? [Y/N] : ")
if (not os.path.exists(tokenFileName + ".txt")):
    print(tokenFileName + ".txt" + " not exist.")
    input(f"{Fore.MAGENTA}Press Enter button for exit")
    exit()
else:
    txt = sum(1 for line in open(tokenFileName + ".txt", 'r'))

def main():
    doIntro()
    if (not os.path.exists(tokenFileName + ".txt")):
        open(tokenFileName + ".txt", 'a+')
    try:
        os.remove("Verified Tokens.txt")
        os.remove("Unverified Tokens.txt")
        os.remove("Invalid Tokens.txt")
        os.remove("Nitro Tokens.txt")
    except: None
    open("Verified Tokens.txt", 'a+')
    open("Unverified Tokens.txt", 'a+')
    open("Invalid Tokens.txt", 'a+')
    if checkNitro.lower() == "y":
        open("Nitro Tokens.txt", 'a+')
    try:
        for item in open(tokenFileName + ".txt", "r").readlines():
            CheckToken(item.strip())
        print("Every token have been checked.")
        input(f"{Fore.MAGENTA}Press Enter button for exit")
        exit()
    except Exception as e:
        print(e)
        print("An unexepted error occurred !")
        input(f"{Fore.MAGENTA}Press Enter button for exit")
        exit()


#Check Nitro
def get_plan_id(token: str):
    for json in requests.get('https://discord.com/api/v7/users/@me/billing/subscriptions', headers={'authorization': token}).json():
        try:            
            if json['plan_id'] == "511651880837840896":
                return True
            else:
                return False
        except:
            return None
#Check Payments
def get_payment_id(token: str):
    for json in requests.get('https://discordapp.com/api/v7/users/@me/billing/payment-sources', headers={'authorization': token}).json():
        try:
            if json['invalid'] == True:
                return True
            else:
                return False
        except:
            return None

def CheckToken(token):
    req = requests.get("https://discordapp.com/api/v7/users/@me?verified", headers={'authorization': token})
    if req.status_code == 401:
        #Invalid tokens
        with open("Invalid Tokens.txt", "a", encoding='utf-8') as f:
            f.write(token + "\n")
    elif req.status_code == 200:
        #Parse data
        json_response = req.json()
        id = (f' ID: {json_response["id"]}') 
        username = (f' Username: {json_response["username"]}') 
        discriminator = (f'#{json_response["discriminator"]}') 
        locale = (f' Language: {json_response["locale"]}') 
        email = (f' Email: {json_response["email"]}') 
        phone = (f' Phone: {json_response["phone"]}') 
        verified = (f'{json_response["verified"]}')
        #Nitro Checker
        if checkNitro.lower() == "y":
            planid = get_plan_id(token)
            if planid is not None:
                if planid is True:
                    plan = "Nitro"                 
                else: 
                    plan = "Classic" 
            else:
                plan = "No"  
            payid = get_payment_id(token)  
            if payid is not None:
                if payid is True:
                    pay = "Invalid"
                else:
                    pay = "Valid"  
            else:
                pay = "No"  
            nitro = (f" Nitro: {plan} Billing: {pay}")
        else:
            nitro = ""
        #Write file
        if (checkNitro.lower() == "y"):
            if ((plan is "Nitro" or plan is "Classic") or (pay is "Valid" or pay is "Invalid")) and (checkNitro.lower() == "y"):
                with open("Nitro Tokens.txt", "a", encoding='utf-8') as f:
                    f.write(token + nitro + username + discriminator + locale + email + phone + "\n")
        if verified is not "False":
            with open("Verified Tokens.txt", "a", encoding='utf-8') as f:
                f.write(token + id + nitro + username + discriminator + locale + email + phone + "\n")
        else:
            with open("Unverified Tokens.txt", "a", encoding='utf-8') as f:
                f.write(token + id + nitro + username + discriminator + locale + email + phone + "\n")              
    else:
        print("An unexepted error occurred !")
        input(f"{Fore.MAGENTA}Press Enter button for exit")
        exit()
    println()

def println():
    os.system('cls')
    verify = sum(1 for line in open("Verified Tokens.txt", 'r', encoding='utf-8'))
    unverify = sum(1 for line in open("Unverified Tokens.txt", 'r', encoding='utf-8'))
    inv = sum(1 for line in open("Invalid Tokens.txt", 'r', encoding='utf-8'))
    if (checkNitro.lower() == "y"):
        nit = sum(1 for line in open("Nitro Tokens.txt", 'r', encoding='utf-8'))
        print(f"{Fore.CYAN}Checked: {verify + unverify + inv}/{txt} {Fore.WHITE}| {Fore.GREEN}Verify: {verify} {Fore.WHITE}| {Fore.YELLOW}Unverify: {unverify} {Fore.WHITE}| {Fore.RED}Invalid: {inv} {Fore.WHITE}| {Fore.MAGENTA}NITRO: {nit}")
    else:
        print(f"{Fore.CYAN}Checked: {verify + unverify + inv}/{txt} {Fore.WHITE}| {Fore.GREEN}Verify: {verify} {Fore.WHITE}| {Fore.YELLOW}Unverify: {unverify} {Fore.WHITE}| {Fore.RED}Invalid: {inv} {Fore.WHITE}")
main()
