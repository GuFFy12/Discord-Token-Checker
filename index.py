import requests, colorama, os, ctypes
from colorama import Fore, init
from sys import exit

init()

def doIntro():
    os.system("cls")
if __name__ == '__main__':
    os.system('cls')
    ctypes.windll.kernel32.SetConsoleTitleW("Discord Token Checker by GuFFy_OwO")
    colorama.init()

print(f"{Fore.MAGENTA}Discord Token Checker by GuFFy_OwO\n")
tokenFileName = input(f"{Fore.GREEN}Enter the name of the file in wich are the unchecked tokens (without .txt) : ")
checkNitro = input(f"{Fore.GREEN}Check nitro and payments on tokens? [Y/N] : ")
checkInfo = input(f"{Fore.GREEN}Create and save info about token to another file? [Y/N] : ")
if not os.path.exists("./output"):
    os.makedirs("./output")
if (not os.path.exists(tokenFileName + ".txt")):
    print(tokenFileName + ".txt" + " not exist.")
    input(f"{Fore.MAGENTA}Press Enter button for exit")
    exit()
else:
    txt = sum(1 for line in open(tokenFileName + ".txt", 'r'))

dirValidTokens = "./output/Valid Tokens.txt"
dirUnverifiedTokens = "./output/Unverified Tokens.txt"
dirNitroTokens = "./output/Nitro Tokens.txt"
dirInfoValidTokens = "./output/info_Valid Tokens.txt"
dirInfoUnverifiedTokens = "./output/info_Unverified Token.txt"
dirInfoNitroTokens = "./output/info_Nitro Tokens.txt"
dirInvalidTokens = "./output/Invalid Tokens.txt"

def main():
    doIntro()
    try:
        os.remove(dirValidTokens)
        os.remove(dirUnverifiedTokens)
        os.remove(dirInvalidTokens)
        os.remove(dirNitroTokens)
        os.remove(dirInfoValidTokens)
        os.remove(dirInfoUnverifiedTokens)
        os.remove(dirInfoNitroTokens)
    except: None
    open(dirValidTokens, 'a+')
    open(dirUnverifiedTokens, 'a+')
    open(dirInvalidTokens, 'a+')
    if checkNitro.lower() == "y":
        open(dirNitroTokens, 'a+')
    if checkInfo.lower() == "y":
        open(dirInfoNitroTokens, 'a+')
        open(dirInfoValidTokens, 'a+')
        open(dirInfoUnverifiedTokens, 'a+')
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
    if len(token) > 59:
        lenght = " 2fa: Yes"
        lenghtToken = f"{token}"
    else:
        lenght = " 2fa: No"
        lenghtToken = f"{token}                             "
    req = requests.get("https://discordapp.com/api/v7/users/@me?verified", headers={'authorization': token})
    if req.status_code == 401:
        #Invalid tokens
        with open(dirInvalidTokens, "a", encoding='utf-8') as f:
            f.write(token + "\n")
            print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.RED}Invalid")
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
        #Write file (SHIIIT CODE MOMENT)
        if checkNitro.lower() == "y":
            if ((plan is "Nitro" or plan is "Classic") or (pay is "Valid" or pay is "Invalid")):
                with open(dirNitroTokens, "a", encoding='utf-8') as f:
                    if checkInfo.lower() == "y":
                        f.write(token + nitro + username + discriminator + locale + email + phone + lenght + "\n")
                        with open(dirInfoNitroTokens, "a", encoding='utf-8') as f:
                            f.write(token + "\n")
                    else: 
                        f.write(token + "\n")
        if verified is not "False":
            with open(dirValidTokens, "a", encoding='utf-8') as f:
                if checkInfo.lower() == "y":
                    f.write(token + id + nitro + username + discriminator + locale + email + phone + lenght + "\n")
                    with open(dirInfoValidTokens, "a", encoding='utf-8') as f:
                        f.write(token + "\n")
                else: 
                    f.write(token + "\n")
            if checkNitro.lower() == "y":
                if  (plan is "Nitro" or plan is "Classic") or (pay is "Valid" or pay is "Invalid"):
                    print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.MAGENTA}Nitro")
                else:
                    print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.GREEN}Valid")
            else:
                print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.GREEN}Valid")
        else:
            with open(dirUnverifiedTokens, "a", encoding='utf-8') as f:
                if checkInfo.lower() == "y":
                    f.write(token + id + nitro + username + discriminator + locale + email + phone + lenght + "\n")
                    with open(dirInfoUnverifiedTokens, "a", encoding='utf-8') as f:
                        f.write(token + "\n")
                else:
                    f.write(token + "\n")
            print(f"{Fore.WHITE}{lenghtToken}   |  {Fore.YELLOW}Unverified")          
    else:
        print("An unexepted error occurred !")
        input(f"{Fore.MAGENTA}Press Enter button for exit")
        exit()
    println()

def println():
    verify = sum(1 for line in open(dirValidTokens, 'r', encoding='utf-8'))
    unverify = sum(1 for line in open(dirUnverifiedTokens, 'r', encoding='utf-8'))
    inv = sum(1 for line in open(dirInvalidTokens, 'r', encoding='utf-8'))
    if checkNitro.lower() == "y":
        nit = sum(1 for line in open(dirNitroTokens, 'r', encoding='utf-8'))
        ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Token Checker by GuFFy_OwO  |  Checked: {verify + unverify + inv}/{txt}  |  Valid: {verify}  |  Unverified: {unverify}  |  Invalid: {inv}  |  NITRO: {nit}')
    else:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Token Checker by GuFFy_OwO  |  Checked: {verify + unverify + inv}/{txt}  |  Valid: {verify}  |  Unverified: {unverify}  |  Invalid: {inv}')
main()
