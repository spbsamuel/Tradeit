import re

from common import Commands,States

def is_create_item(user,msg_obj):
    if (user.last_state == States.STATIC):
        try:
            return 'attachments' in msg_obj.keys()
        except:
            return False
    return False

def is_edit_desc(user,msg_obj):

    if (user.last_state == States.EDIT or user.last_state == States.ADD_NEW):
        try:
            msg_text = ''.join(re.findall('[a-z]',msg_obj["text"].lower()))
            return len(msg_obj["text"])>0 and msg_text != Commands.START_TRADING
        except:
            return False
    return False

def is_edit_pic(user,msg_obj):
    if (user.last_state == States.EDIT or user.last_state == States.ADD_NEW):
        try:
            return msg_obj['attachments']['type']=='image'
        except:
            return False
    return False

def interpret(message,*args,**kwargs):
    """
    return a tuple (command,command_kwargs), return None for both if message is not recognizable
    command is string, command_kwargs is a dict
    """
    user = kwargs.get("user")
    msg_obj = kwargs.get("msg_obj")
    lowered_msg = ''.join(re.findall('[a-z0-9]',message.lower()))
    if (is_create_item(user,msg_obj)):
        return Commands.CREATE_ITEM,{'img_url':msg_obj['attachments']}
    elif(is_edit_desc(user,msg_obj)):
        return Commands.EDIT_ITEM,{'text':msg_obj['text']}
    elif(is_edit_pic(user,msg_obj)):
        return Commands.EDIT_ITEM,{'img_url':msg_obj['attachments']}
    elif(user.last_state == States.CHANGE_LOCATION):
        return Commands.LOCATION_SAVED,{'text':msg_obj['text']}
    if (lowered_msg.find("btn")!=-1):
        id = int(re.findall('[0-9]+',lowered_msg)[0])
        return lowered_msg,{'msg_obj':msg_obj,'id':id}
    else:
        return lowered_msg,{'msg_obj':msg_obj}
