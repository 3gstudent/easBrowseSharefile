# easBrowseSharefile
Use to browse the share file by eas(Exchange Server ActiveSync)

Reference:

https://github.com/FSecureLABS/peas

https://github.com/solbirn/pyActiveSync

Usage:

```
easBrowseSharefile.py <host> <user> <password> <mode> <path>
```

Eg.

```
easBrowseSharefile.py 192.168.1.1 user1 password1 listfile \\dc1\SYSVOL
easBrowseSharefile.py 192.168.1.1 user1 password1 readfile \\dc1\SYSVOL\test.com\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\GPT.INI
```
