# Discord-Token-Checker


## Menu
![image](https://user-images.githubusercontent.com/49491499/158438363-35de8be0-ee2e-42a8-b755-04be104f2995.png)

## Update!

Firstly, now the tokens data is processed on a remote server. This is due to the fact that I have been writing a telegram bot for checking tokens for a long time and I did not want to rewrite the backend for python.

In this regard, the speed increased from 1 token per second to 40. I achieved this with the help of parallel requests and proxies, it was difficult to implement in python. Also, when I finish the nuker, it will probably be the fastest, since the 429 error handler with limit checking will be used.

As soon as I complete the backend (checker, info, idTracker, webhookSpammer, nitroBuyer, serverNuker, userNuker,messageSearcher) I will publish it in the public.

You can still download the old checker in older versions. https://github.com/GuFFy12/Discord-Token-Checker/tree/a3522d1254ea60b82afe52f976cae18041d08171

## Output

Standart output with valid, invalid, etc txt files.

Json output:
```json
{
    "tokensInfo": {
        "valid": [],
        "nitro": [],
        "payments": [],
        "unverified": [],
        "invalid": [],
        "parsedTokens": []
    },
    "tokensData": {
        "TOKEN": {
            "status": "invalid",
            "me": {},
            "payment-sources": {}
        }
    }
}        
```

Since 1 more request is needed for the final verification of tokens, then you get the payment sources as a side to discord.gg/users/@me


## OLD Menu
![cmd_mO9d4Vud3I](https://user-images.githubusercontent.com/49491499/130788540-a8d20eaa-751c-4bce-a586-f48cf4a9f6ae.png)
## OLD Checker
![browser_G49q1xqgiV](https://user-images.githubusercontent.com/49491499/130812769-e5ab2ad3-612d-4d58-8bf9-d7b66b718a62.png)
## OLD Parser
![cmd_ayxu9GSYTY](https://user-images.githubusercontent.com/49491499/130788608-2d4329d0-4571-4e26-8f79-cd7dda2046e1.png)


Disabling nitro checking on valid accounts increases speed by ~1.7 times

JS EDITION: https://github.com/amfero/DiscordTokenChecker 

TS EDITION: https://github.com/cattyngmd/DiscordTokenChecker-ts

PY EDITION: https://github.com/GuFFy12/Discord-Token-Checker
