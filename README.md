# CC3067-P1-XMPPCHAT
CLI-Based chat program using XMPP made on Python.

Server running on Openfire.

## Requirements
```
blessed==1.18.1
pyOpenSSL==19.0.0
requests==2.6.0
slixmpp==1.7.1
```

## Running

**NOTE: MUST BE RUN IN A LINUX SYSTEM. WSL works fine.**
1. cd into installation directory
2. Run the equivalent command* for your installation of python3: `python3 -m pip install -r requirements.txt`
3. Run the equivalent command for your installation of python3: `python3 main.py`
4. Input username, password, and nickname. If user does not exist, it will be created. Otherwise, it will login as long as password is correct.
5. Follow instructions on-screen for different commands. Command reference sheet can also be found in the next section.


\*For some systems, python, python3.6, or py can be default for python3

## Command reference sheet
| Function | / command | arguments | usage |
| --- | --- | --- | --- |
| Send message | leave empty | message | message |
| Set message recipient | /set_contact | JID | /set_contact HID |
| Show friends | /friends | none | /friends |
| Add friend | /add | JID | /add JID |
| Show user info | /whois | JID | /whois JID |
| Change status | /stattus | status | /status status |
| Join room | /join | room | /join room |
| Leave room | /leave | message | /leave "bye" |
| Exit | /exit | none | /exit |
| Delete account | /death | none | /death |


## Intended functions, and their status as of writing this README

| Function      | Status | Notes|
| ----------- | ----------- |-----------|
| Send Messages     | 100%       | Takes about five minutes to actually deliver. Unsure if server problem or just bad implementation.|
| Set Message Recipient   | 100%        | |
| Show Friends list | 100% | |
| Add person to Friends | 100% | |
| Whois/Show Details | 0% | Technically just a placeholder function. |
| Set Status | 50% | Gives no error, but doesn't actually change status |
| Join Room | 50% | Gives no error, but doesn't actually add to room |
| Leave Room | 0% | Gives error, can't even join room |
| File Sending | 0% | Unimplemented |
| Notification sending | 0% | Unimplemented |
| Logging in | 100% | |
| Registering | 100% | |
| Logging out | 100% | |
| Deleting account | 80% | Deletes account, but hangs the program |


## Video

https://youtu.be/d0Pv0xLBtZg
