python-ssh
==========

The Python based paralleling ssh tool, useful for batch executing ssh remote command against a bunch of servers.

It has some features you may be interested:
* use compressed hostname ranges, it tool will expand for you
* get server list from file
* support regex match of output, useful to indentify which servers is you wanted. (for example: list servers installed openssl-1.0.1a, Heartbleed impacted !) 
* able to use jumpbox, with ```--extra-arg='-At jumpbox-hostname ssh'```
* max number of parallel threads control


TODO
==========
create a user friendly install package


Commandline Help
==========

```
Usage: python-ssh [ -p <max parallel thread number> ] (-f filename | -r range)     [ -l login_name ] command

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PARALLEL, --parallel=PARALLEL
                        max number of parallel threads ,default is 10
  -r RANGE, --range=RANGE
                        Range of nodes to operate on
  -f FILENAME, --file=FILENAME
                        the host file which stores the host list
  -l LOGIN_NAME, --login_name=LOGIN_NAME
                        Specifies the user to log in as on the remote machine.
                        This also may be specified on a per-host basis in the
                        configuration file
  -X EXTRA_ARGUMENT, --extra-arg=EXTRA_ARGUMENT
                        Extra command-line argument. for example: -o
                        ConnectTimeOut=10
  -e PATTERN, --regexp=PATTERN
                        Use PATTERN as the pattern;    useful to protect
                        patterns beginning with -.
  -v, --invert-match    Invert the sense of matching, to select non-matching
                        lines.

Report any bugs to lichun.william@gmail.com
```

Hostname Ranges
============
The utility include er.py for expanding range expressiong, for example
```
www01-99.google.com
db01-3.demonware.net
www1-2.demonware.net,mysql01-9.mysql.com
```

```
er www1-2.demonware.net,mysql01-9.mysql.com
www2.demonware.net
mysql08.mysql.com
mysql02.mysql.com
mysql03.mysql.com
mysql04.mysql.com
mysql05.mysql.com
mysql06.mysql.com
mysql07.mysql.com
mysql09.mysql.com
www1.demonware.net
mysql01.mysql.com
```

help
```
Usage: er expr1 [expr2 ...]

Expand host ranges with given expressions

positional arguments:
  expr                  expressions to be expanded

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s, --sort            sort the out put?
  -f, --shuffle         shuffle list?
  -d DELIMITER, --delimiter DELIMITER
                        delimiter of the output, default is space
  -n, --newline         same as --delimiter='\n'

Report any bugs to lichun.william@gmail.com
```

Examples
============
Executing ```uname``` on 123 servers with default parrelling thread of 10.

```pssh -lwilliam -r www001-123.github.com -- uname```

Check ```ntpd``` status, dry run, with maximun 2 executing simultaneously.

```pssh -lroot -r db01-2.github.com,web2-9.github.com  --dry-run -P 2 -- /etc/init.d/ntpd status```

```
 1 of 10 : ===============  db01.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no db01.github.com /etc/init.d/ntpd status
 2 of 10 : ===============  db02.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no db02.github.com /etc/init.d/ntpd status
 3 of 10 : ===============  web3.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web3.github.com /etc/init.d/ntpd status
 4 of 10 : ===============  web4.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web4.github.com /etc/init.d/ntpd status
 5 of 10 : ===============  web8.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web8.github.com /etc/init.d/ntpd status
 6 of 10 : ===============  web5.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web5.github.com /etc/init.d/ntpd status
 7 of 10 : ===============  web2.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web2.github.com /etc/init.d/ntpd status
 8 of 10 : ===============  web7.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web7.github.com /etc/init.d/ntpd status
 9 of 10 : ===============  web9.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web9.github.com /etc/init.d/ntpd status
 10 of 10 : ===============  web6.github.com  ===============
ssh -l root -o StrictHostKeyChecking=no web6.github.com /etc/init.d/ntpd status
```
