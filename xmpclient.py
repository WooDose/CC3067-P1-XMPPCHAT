from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.asyncio import asyncio
from threading import Thread
from blessedmenu import menu
import logging
import os
import blessed

#Blessed!
UITerminal = blessed.Terminal()

class xmpclient(ClientXMPP):

  def __init__(self, jid, password, nick):
    ClientXMPP.__init__(self, jid, password)
    self.add_event_handler("session_start", self.session_start)
    self.add_event_handler("message", self.message)
    self.add_event_handler("register", self.register)

    ## Chat parameters
    self.params = {'room':'helloworld',
    'nick':nick,
    'recipient':('helloworld', 'group'),
    }

    self.auto_subscribe = True

    # Menu functions
    functions = {
      ## Message functions
      'send_message': self.send_msg,
      'set_contact': self.set_contact,

      ## Friend functions
      'friends': self.get_friends,
      'add': self.add_contact,
      'whois': self.whois,
      'status': self.set_status,

      ## Groupchat
      'join': self.join_room,
      'leave': self.leave_room,

      ## Misc
      #'file': self.send_file, ## Not yet implemented
      
      ## Disconnect or Destroy account
      'exit': self.terminate, 
      'death': self.destroy_acct
    }

    ## Instantiate blessed menu in backgounrd
    self.menuInstance = Thread(target = menu, args = (functions,))

 

  def session_start(self, event):
    '''
    Session start - Starts session and menu instance
    event: dummy variable
    Status: Working
    '''
    self.send_presence()
    self.get_roster()
    self.menuInstance.start()

  async def register(self, iq):
    '''Self Register - Registers user if does not exist
    iq: stanza with register information, ends up being dummy due to stanza generated within function
    Status: Working
    '''
    resp = self.Iq()
    resp['type'] = 'set'
    resp['register']['username'] = self.boundjid.user
    resp['register']['password'] = self.password
    try:
      await resp.send()
      logging.info("Account created for %s!" % self.boundjid)
    except IqError as e:
      logging.error("Account already exists.")
    except IqTimeout:
      logging.error("No response from server.")
      self.disconnect()
    
  def message(self, msg):
    '''
    Message - Read messages
    msg: message that has been received
    BUG: Kind of works, sometimes takes up to five minutes to receive messages, sometimes crashes.
    '''
    if msg['type'] in ('chat', 'normal'):
      print(UITerminal.yellow(str(msg['from'])+ ' > ') + UITerminal.white(msg['body']))

  def send_msg(self, msg):
      '''
      Send message - Send message
      msg: message to be sent (recipient is determined from set contact)
      BUG: Again, sometimes takes up to five minutes, sometimes crashes.
      '''
      self.send_message(mto=self.params['recipient'][0], mbody=msg, msubject='normal message', mfrom=self.boundjid)

  
  def set_contact(self, recipient):
    '''
    Set contact - Sets recipient for future messages
    recipient: recipient
    Status: Working
    '''
    if recipient in self.roster[self.jid]:
      self.params['recipient'] = (recipient, 'person')
    else:
      print(UITerminal.red('User '+ recipient + ' does not exist.'))

  
  def get_friends(self,session):
    '''
    Get Friends - Gets friends list and prints, assuming you have any.
    session - dummy variable
    Status: Working
    '''
    # self.get_roster()
    print(UITerminal.palegreen ('Friends: '))
    for jid in self.roster[self.jid]:
      if jid != self.jid:
        print(UITerminal.white(jid))
  
  
  def add_contact(self, contact):
    '''
    Add contact - Add new contact to roster, prints new list.
    contact: User to be added to roster
    Status: Working
    '''
    self.send_presence_subscription(pto=contact)
    ## Stupid try/except loop because for some reason, update_roster works properly and adds the user, but decides to kill itself. This seemingly useless try/except fixes it, because the roster is updated, but the error is handled and keeps going as normal.
    try:
      self.update_roster(contact)
    except:
      pass
    print(UITerminal.green(contact + ' has been added to friends roster.'))
    print(UITerminal.green('Roster list is now:'))
    self.get_friends('1')

 
  def whois(self,contact):
    '''
    Whois - Prints contact information
    contact: Contact to be queried
    Status: Pretty much a placeholder, but gets the job done.
    '''
    print(UITerminal.red(contact + ' is ' +contact))

  
  def set_status(self, status):
    '''
    Set status - Changes presence status
    status: status to be set
    Status: Works, but doesn't reflect anywhere else.
    '''
    self.make_presence(pshow=status)
    print(UITerminal.cyan('Status is now: '+status))

  def muc_online(self, presence):
    if presence['muc']['nick'] != self.nick:
      print(UITerminal.bold("Joined Room"))

  def join_room(self, room):
    '''
    Join Room - Joins MUC room, and sets as the current recipient.
    room: Room to be joined
    BUG: Receives OK signal, but doesn't actually add to room.
    '''
    self.add_event_handler("muc::%s::got_online" % room, self.muc_online)
    self.plugin['xep_0045'].join_muc(room, self.params['nick'])
    self.params['room'] = room

    print(UITerminal.forestgreen('You are now talking in: '+ room+', or at least, I hope so.'))
    self.params['recipient'] = (room,'group')

  def leave_room(self, msg = ''):
    '''
    Leave Room - Leaves MUC room, and sets recipient to self.
    msg: dummy variable to fill IQ
    BUG: Crashes, most likely because joining rooms is broken.
    '''
    self.plugin['xep_0045'].leave_muc(self.jid, self.params['nick'], msg)
    print(UITerminal.bold_red('Leaving room: ' + self.params['room'] +', assuming you really were there.'))
    self.params['room'] = ''
    self.params['recipient'] = (self.jid,'person')

  
  def terminate(self, session):
    '''
    Terminate - Ends session and disconnects
    session: dummy variable
    BUG: Disconnects, but leaves menu thread running, so doesn't close entirely
    '''
    self.disconnect(wait=1.0)
    os._exit(1)
    
  def destroy_acct(self, args):
    '''Async function to destroy account in background'''
    asyncio.run(self.destroy_acct_activator())

  async def destroy_acct_activator(self):
    '''
    Destroy account - deletes account
    Variables: n/a
    BUG: Does not work. Just stays in an infinite loop.'''
    resp = self.Iq()
    resp['type'] = 'set'
    resp['from'] = self.boundjid.jid
    resp['register'] = ' '
    resp['register']['remove'] = ' '
    try:
      await resp.send(timeout=1)
      self.terminate()
    except IqError:
      print(UITerminal.bold_red('Unable to delete account'))
    except IqTimeout:
      print(UITerminal.bold_red('Timeout when deleting account'))
      self.disconnect()


