__author__ = 'Administrator'

# list of valid commands
COMMANDS = ['welcome',
            'instructions',
            'help',
            'inventory',
            'createitem',
            'edititem',
            'locationsaved',
            'changelocation',
            'starttrading',
            'waiting',
            'rejected',
            'success',
            'chats']

class States(object):
    STATIC = 0
    ADD_NEW,EDIT,START_TRADING = 6,7,8