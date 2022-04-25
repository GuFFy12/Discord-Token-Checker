<div align="center">
    
# Discord-Token-Checker
![](https://img.shields.io/github/downloads/GuFFy12/Discord-Token-Checker/total?color=blue&style=for-the-badge) 
![](https://img.shields.io/github/commit-activity/w/GuFFy12/Discord-Token-Checker?style=for-the-badge)
![](https://img.shields.io/tokei/lines/github/GuFFy12/Discord-Token-Checker?style=for-the-badge)
![](https://img.shields.io/github/license/GuFFy12/Discord-Token-Checker?color=blue&style=for-the-badge)
    
Telegram Bot with same functionality: [@Discord_Token_Checker_bot](https://t.me/Discord_Token_Checker_bot)

![image](https://user-images.githubusercontent.com/49491499/164704463-b54eca93-a6b7-4ca5-9d9d-c581e58e5edd.png)

## QUESTIONS
</div>

1) Q: Why my tokens checked so long... in console writing wait 2 minutes, but i wait an hour and nothing!

   A: There is a queue in the backend. Since you are sending tokens for verification, other tokens from other people can be checking on the server before you.

2) Q: Why is the sum of valid + unverified + invalid tokens less than the sum of parsed tokens?

   A: The checker records all id tokens. If the new token contains an id from the list of verified ones, it is removed. Don't worry if one token becomes invalid another token with the same id too.

3) Q: Why do I have 1000 tokens in the file, but the parser found only 580?

   A: The code uses an advanced token parser. The fact is that ordinary parsers check only the token pattern, but it also needs to check headers. (More info: https://jwt.io/introduction)
In short, there are tokens that were created by some kind of token generator. They contain a header. If you decrypt it (base64), then for natural discord tokens it represents json value, while for generated ones it will be different. Check it out for yourself: https://jwt.io/#debugger-io.
<div align="center">   

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
