python-ssh
==========


Commandline Help
==========

```
Usage: python-ssh [ -p <max parallel thread number> ] (-f filename |-i igor_range | -r range)     [ -l login_name ] command

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PARALLEL, --parallel=PARALLEL
                        max number of parallel threads ,default is 10
  -r RANGE, --range=RANGE
                        Range of nodes to operate on
  -i IGOR, --igor=IGOR  Igor Range of nodes to operate on
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

