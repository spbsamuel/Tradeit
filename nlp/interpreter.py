import re

from common import COMMANDS,States


MSG_TO_COMMAND = {x:x for x in COMMANDS}



def interpret(message,*args,**kwargs):
    """
    return a tuple (command,command_kwargs), return None for both if message is not recognizable
    command is string, command_kwargs is a dict
    """
    user = kwargs.get("user")
    lowered_msg = ''.join(re.findall('[a-z]',message.lower()))
    return MSG_TO_COMMAND.get(lowered_msg),{}
