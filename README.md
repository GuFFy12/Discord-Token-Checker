<div align="center">
    
# Discord-Token-Checker
![](https://img.shields.io/github/downloads/GuFFy12/Discord-Token-Checker/total?color=blue&style=for-the-badge) 
![](https://img.shields.io/github/commit-activity/w/GuFFy12/Discord-Token-Checker?style=for-the-badge)
![](https://img.shields.io/tokei/lines/github/GuFFy12/Discord-Token-Checker?style=for-the-badge)
![](https://img.shields.io/github/license/GuFFy12/Discord-Token-Checker?color=blue&style=for-the-badge)

![image](https://user-images.githubusercontent.com/49491499/161088450-cb291390-baec-4456-a330-7caa83805bba.png)
    
## OUTPUT
</div>
Standart output with valid, invalid, etc txt files.

Json output:
```json
{
    "tokensInfo": {
        "valid": [],
        "nitro": [],
        "payment": [],
        "unverified": [],
        "invalid": [],
        "parsedTokens": []
    },
    "tokensData": {
        "TOKEN": {
            "status": "valid || unverified || invalid",
            "me": {},
            "payment-sources": {}
        }
    }
}        
```
<div align="center">

## UPDATE
</div>
Firstly, now the tokens data is processed on a remote server. This is due to the fact that I have been writing a telegram bot for checking tokens for a long time and I did not want to rewrite the backend for python.

In this regard, the speed increased from 1 token per second to 40. I achieved this with the help of parallel requests and proxies, it was difficult to implement in python. Also, when I finish the nuker, it will probably be the fastest, since the 429 error handler with limit checking will be used.

As soon as I complete the backend (checker, info, idTracker, webhookSpammer, nitroBuyer, serverNuker, userNuker, messageSearcher) I will publish it in the public.

Since 1 more request is needed for the final verification of tokens, then you get the payment sources as a side to discord.gg/users/@me.
Also due to the fact that you send tokens to the server, to avoid spam, there are one request per minute otherwise 429 error.
