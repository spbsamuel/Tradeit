__author__ = 'Administrator'

# list of valid commands
class Commands(object):
    WELCOME = "welcome"
    INSTRUCTIONS = "instructions"
    HELP = "help"
    INVENTORY = "inventory"
    CREATE_ITEM = "createitem"
    EDIT_ITEM = "edititem"
    LOCATION_SAVED = "locationsaved"
    CHANGE_LOCATION = "changelocation"
    START_TRADING = "starttrading"
    CANCEL_TRADING = "btncanceltrade"
    # WAITING = 'waiting'
    REJECTED = 'rejected'
    # SUCCESS = 'success'
    CHATS = 'chats'

class States(object):
    STATIC = 0
    CHANGE_LOCATION = 5
    ADD_NEW,EDIT,START_TRADING = 6,7,8