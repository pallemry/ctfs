At `/robots.txt` I found:
```
User-agent: *
Disallow: /lib
Disallow: /secret
```
at `/lib` I found: `/lib/hash`:
![[Pasted image 20260919173034.png]]
and the file hash was an executable.

I got also found in `/secret` the following:
![[Pasted image 20260919202904.png]]
and the hash:
```
c48d533a6c5b270ef9334eb999f4d932
```
which is md4, most probably.
I found in an online DB that it is the hash of:
```
66778
```
Therefore I succeeded and I got past it to the next level.
