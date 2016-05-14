
def process_for_reply(cmd,cmdargs,user,**kwargs):
    """
    :param cmd: string
    :param cmdargs: dict
    :param user: BotUser
    :return: a dict as message to be posted back, return None if nothing is to be posted back
    """
    return {'text':'hello,command is {}'.format(cmd)}