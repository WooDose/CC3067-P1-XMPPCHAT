import blessed

UITerminal = blessed.Terminal()
isFirst = True

options ='''
  Messaging: 
  Type without / for message.
  /set_contact <contact>: set contact for messages 
  
  Friend management: 
  /friends: Show friends roster
  /add [JID]: Add new friend
  /whois [JID]: Get friend information
  /status [status_message]: Change status
  
  Groupchat:
  /join [room]: Join Room
  /leave: Leave Room
  
  Disconnect or destroy:
  /exit: Disconnect and exit
  /death: Unregister account
  
  '''
OPTIONS_SHOWN = True

def showOptions(args=''):
  ## Show options at top of screen
  if OPTIONS_SHOWN:
    useterminal = UITerminal.location(0, int(UITerminal.height/2))
  else:
    useterminal = UITerminal.location()
  with useterminal:
    print(UITerminal.center(UITerminal.blink('Commands')))
    print(UITerminal.center(options))

def menu(functions):
  ## Start menu
  showOptions()
  OPTIONS_SHOWN = False
  while True:
    # Expect input
    message = input(UITerminal.move(UITerminal.height - 1, 0) + '>')
    # Handle commands
    if message.startswith('/'):
      command = message.strip().split()[0][1:]
      if command in functions:
        arg = message[2 + len(command):]
        print(arg)
        functions[command](arg)
      else:
        print(UITerminal.red('Unknown command.'))
    else:
      functions['send_message'](message)
