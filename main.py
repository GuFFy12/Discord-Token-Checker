import json
import os
import pathlib
import re
import time

import jwt
import requests
from colorama import Fore


class Checker(object):
    @staticmethod
    def cls():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def fast_exit(message):
        print()
        print(message)
        print()
        input("Press Enter button for exit.")
        exit()

    def __init__(self):
        self.url = "https://lililil.xyz/checker"
        self.version = "3.5.3"
        self.file_types = [".txt", ".html", ".json", ".log", ".ldb", ".sqlite"]
        self.param = {}

        self.tokens_parsed = []
        self.res = {}

    def get_param(self):
        try:
            self.param = requests.get(self.url).json()
            self.res = self.param["res"]
            if self.param["latest_version"] != self.version:
                print(f"New version {Fore.CYAN}{self.param['latest_version']}{Fore.RESET} available! Download: "
                      f"{Fore.CYAN}https://github.com/GuFFy12/Discord-Token-Checker/releases{Fore.RESET}")
        except Exception as error:
            Checker.fast_exit(f"An error occurred while trying connect to the server. {error.__doc__}")

    def main(self):
        Checker.cls()

        print(fr"""
   ___  _                     __  ______     __              _______           __                  ___ 
  / _ \(_)__ _______  _______/ / /_  __/__  / /_____ ___    / ___/ /  ___ ____/ /_____ ____  _  __|_  |
 / // / (_-</ __/ _ \/ __/ _  /   / / / _ \/  '_/ -_) _ \  / /__/ _ \/ -_) __/  '_/ -_) __/ | |/ / __/ 
/____/_/___/\__/\___/_/  \_,_/   /_/  \___/_/\_\\__/_//_/  \___/_//_/\__/\__/_/\_\\__/_/    |___/____/ 
                                                                                           {Fore.CYAN}by GuFFy_OwO
{Fore.RESET} 
Telegram Bot with same functionality: {Fore.CYAN}https://t.me/Discord_Token_Checker_bot{Fore.RESET}
Site with table and excel output: {Fore.CYAN}https://lililil.xyz{Fore.RESET}
""")

        print(f"{Fore.RESET}[{Fore.CYAN}1{Fore.RESET}] Enter token")
        print(f"{Fore.RESET}[{Fore.CYAN}2{Fore.RESET}] Check file")
        print()
        check_type = input(f"{Fore.CYAN}>{Fore.RESET}Select An Option{Fore.CYAN}:{Fore.RESET} ")

        if "1" in check_type:
            print()
            self.parse_tokens(input(f"{Fore.CYAN}>{Fore.RESET}Enter tokens{Fore.CYAN}:{Fore.RESET} "))
        elif "2" in check_type:
            print()
            token_file_name = input(
                f"{Fore.CYAN}>{Fore.RESET}Enter the directory of the files or file in which are the unchecked tokens"
                f" (supported types: txt, html, json and etc){Fore.CYAN}:{Fore.RESET} "
            )
            self.check_file(token_file_name)
        else:
            Checker.fast_exit("Invalid Option.")

        self.send_tokens()
        Checker.fast_exit("All tokens saved!")

    def check_file(self, token_file_name):
        if not os.path.exists(token_file_name):
            Checker.fast_exit(f"{token_file_name} directory not exist.")

        if os.path.isfile(token_file_name):
            with open(token_file_name, "r", errors="ignore") as file:
                self.parse_tokens(file.read())
        else:
            for path in pathlib.Path(token_file_name).rglob("*.*"):
                if path.suffix in self.file_types:
                    try:
                        with open(path, "r", errors="ignore") as file:
                            self.parse_tokens(file.read())
                    except IOError as error:
                        print(error)
            self.tokens_parsed = list(dict.fromkeys(self.tokens_parsed))

    def parse_tokens(self, text):
        pre_parsed = []
        for token in re.findall(self.param["regexp"], text):
            pre_parsed.append(token)
        pre_parsed = list(dict.fromkeys(pre_parsed))

        for token in pre_parsed:
            try:
                jwt.decode(token, options={"verify_signature": False})
            except Exception as error:
                if str(error) == "Invalid header string: must be a json object" or str(error) == "Not enough segments":
                    self.tokens_parsed.append(token)

    def send_tokens(self):
        if len(self.tokens_parsed) > self.param["max_tokens"]:
            Checker.fast_exit(
                f"The current API limit is {Fore.CYAN}{self.param['max_tokens']}{Fore.RESET} tokens. "
                f"Amount of sorted tokens - {Fore.CYAN}{len(self.tokens_parsed)}{Fore.RESET}."
            )
        elif len(self.tokens_parsed) == 0:
            Checker.fast_exit("Parser did not found tokens.")

        print()
        print(f"Found {Fore.CYAN}{len(self.tokens_parsed)}{Fore.RESET} tokens!")

        parts = [self.tokens_parsed[d:d + self.param["tokens_part"]] for d in
                 range(0, len(self.tokens_parsed), self.param["tokens_part"])]

        for i in range(len(parts)):
            tokens_time = self.param["tokens_time"] * len(parts[i]) // 1000

            print()
            print(
                f"Sending {Fore.CYAN}{i + 1}{Fore.RESET}/{Fore.CYAN}{len(parts)}{Fore.RESET} part of tokens... "
                f"{Fore.CYAN}{len(parts[i])}{Fore.RESET} tokens - {Fore.CYAN}{tokens_time}{Fore.RESET} sec."
            )

            req_successful = False
            try:
                req = {}
                while not req_successful:
                    req = requests.post(self.url, json=parts[i])

                    if req.status_code == 429:
                        print(
                            f"Too many tokens check requests, retry after "
                            f"{Fore.CYAN}{req.headers['RateLimit-Reset']}{Fore.RESET} seconds..."
                        )
                        time.sleep(float(req.headers['RateLimit-Reset']))
                    elif req.status_code != 200:
                        Checker.fast_exit(f"Status code is {Fore.CYAN}{req.status_code}{Fore.RESET}. {req.json()}")
                    else:
                        req_successful = True

                for tokens_type in self.res["tokensInfo"]:
                    self.res["tokensInfo"][tokens_type] += req.json()["tokensInfo"][tokens_type]
                self.res["tokensData"].update(req.json()["tokensData"])
            except Exception as error:
                Checker.fast_exit(f"An error occurred while trying to send tokens to the server. {error.__doc__}")

            self.save_res()

    def save_res(self):
        stats = ""
        for token_type in self.res["tokensInfo"].keys():
            if self.res["tokensInfo"][token_type]:
                stats += f"{token_type} - {Fore.CYAN}{len(self.res['tokensInfo'][token_type])}{Fore.RESET}, "
                with open(token_type + ".txt", "w") as file:
                    file.write("\n".join(self.res["tokensInfo"][token_type]))

        with open("tokens_data.json", "w") as file:
            json.dump(self.res, file, indent=4)

        print(f"Stats: {stats[:-2]}")


if __name__ == "__main__":
    checker = Checker()
    checker.get_param()
    checker.main()
    checker.send_tokens()
