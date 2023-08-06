<h1 align="center">Wuddz Port Scanner</h1>

## Description
 - Asynchronously Scan A Host(s)/Network(s)/IPRange(s) For Open TCP Ports, Using Specified Connection Timeout & Task Limit Amount.
 - Cleaned Up An Old PortScanner I Wrote Some Time Ago, Thought I'd Share Even Though There Are A Multitude Of Them Around.

## Prerequisites
 - Python : 3.7

## Installation
Install using [PyPI](https://pypi.org/project/wuddz-pscan):
```
$ pip install wuddz-pscan
```
Install locally by cloning or downloading and extracting the repo, then cd into 'dist' directory and execute:
```
$ pip install wuddz_pscan-1.0.0.tar.gz
```
Then to run it, execute the following in the terminal:
```
$ wudz-pscan
```

### Usage
Port Formats:
```
80 | 1-443 | 25,80,445
```
Host Formats:
```
1.1.1.1 | 1.1.1.0/24 | 1.1.1.1-1.1.2.2 | 2.2.2.2,1.1.1.1
```
Scan Host "1.1.1.1" For Ports "80,443" Using 200 Asynchronous Task Limit, 1second Timeout & Save Results To "output.txt".
```
$ wudz-pscan -i 1.1.1.1 -p 80,443 -o output.txt -t 200 -m 1
```
Scan All 65535 Ports On Both Hosts & Print Open Ports To Screen.
```
$ wudz-pscan -i 1.1.1.1,2.2.2.2  ("Scans All 65535 Ports As Default")\n'
```
Scan Host(s) In "hosts.txt" For Open Ports "80,445" & Print Results To Screen.
```
$ wudz-pscan.py -i hosts.txt -p 80-445
```

## Contact Info:
 - Email:     wuddz_devs@protonmail.com                                                              
 - Github:    https://github.com/wuddz-devs                                                          
 - Telegram:  https://t.me/wuddz_devs
 - Youtube:   https://youtube.com/@wuddz-devs
 - Reddit:    https://reddit.com/user/wuddz-devs

### Buy Me A Coffee!!
 - ERC20 Address: 0x1F1C47dD653Af628D394eac7bAA9Ccf774fd784f

#### Peace & Love Always!!
