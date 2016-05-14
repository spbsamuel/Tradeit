def fb_helper_btn(title,url,payload,web_url=True):
    if web_url:
        return {"type": "web_url", "title":title,"url":url}
    if not web_url:
        return {"type": "postback", "title":title,"payload":payload}


def fb_helper_element(title,item_url="",image_url="",subtitle="",buttons=None):
    temp = {"title":title}
    if len(image_url) > 0:
        temp["image_url"] = image_url
    if len(subtitle) > 0:
        temp["subtitle"] = subtitle
    if len(item_url) > 0:
        temp["item_url"] = item_url
    if len(buttons) > 0:
        temp["buttons"] = buttons
    return temp


def fb_helper_playload_btn(text,buttons=None):
    return {"template_type":"button","text":text,"buttons":buttons}


def fb_helper_playload_generic(elements=None):
    return {"template_type":"generic","elements":elements}


def fb_msg(type,payload,notification="REGULAR"):
    if type == "text":
        return {"text":payload}
    if type == "image":
        return {"attachment":{"type":"image","payload":{"url":payload}}}
    if type == "template":
        return {"attachment":{"type":"template","payload":payload}}


def welcome_msg():
    return fb_msg(
        "template",
        fb_helper_playload_btn(
            "Welcome",
            [fb_helper_btn("Start Trading","","btn_start_trade",False),
            fb_helper_btn("How it works","","btn_instructions",False)]
            )
        )


def update_user():
    return 0


def instructions():
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                "Instruction Page 1",
                "",
                "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg"
                ),
            fb_helper_element(
                "Instruction Page 2",
                "",
                "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg"),
            fb_helper_element(
                "You can use these links",
                "",
                "",
                "",
                [
                fb_helper_btn(
                    "Start Trading",
                    "",
                    "btn_start_trade",
                    False
                    ),
                fb_helper_btn(
                    "See Inventory",
                "",
                "btn_inventory",
                False
                )
                ]
                )
            ]
            )
        )


def help():
    return fb_msg(
        "text",
        "Hey there don't worry you can use these cmds:\ntrade: 'trade now'\nsee all: 'my items'"
        )


def inventory(user):
    """
    Return list of elements

    use this function

    fb_helper_element(
            "Item desc",
            "",
            "Item Picture",
            "",
            [
            fb_helper_btn(
                "Trade This",
                "",
                "btn_start_trade",
                False
                ),
            fb_helper_btn(
                "Edit This",
                "",
                "btn_inventory",
                False
                )
            ]
            )
    """
    user.item_set.all()
    element_list = [];
    #for item in item_set push element into element_list

    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                "Item 1 Desc",
            "",
            "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
            "",
            [
            fb_helper_btn(
                "Trade This",
                "",
                "btn_start_trade",
                False
                ),
            fb_helper_btn(
                "Edit This",
                "",
                "btn_inventory",
                False
                )
            ]
            ),
            fb_helper_element(
                "Item 2 Desc",
            "",
            "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
            "",
            [
            fb_helper_btn(
                "Trade This",
                "",
                "btn_start_trade",
                False
                ),
            fb_helper_btn(
                    "See Inventory",
                "",
                "btn_inventory",
                False
                )
            ]
            ),
            fb_helper_element(
                "Item 1 Desc",
            "",
            "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
            "",
            [
            fb_helper_btn(
                "Start Trading",
                "",
                "btn_start_trade",
                False
                ),
            fb_helper_btn(
                    "See Inventory",
                "",
                "btn_inventory",
                False
                )
            ]
            )
            ]
        )
    )


def create_item():
    """

    """
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                "Your Item Name",
                "",
                "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
                "Add Item description by replying",
                [
                fb_helper_btn(
                    "Cancel",
                    "",
                    "btn_cancel",
                    False
                    )
                ]
                )
            ]
            )
        )


def edit_item():
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                "Item description",
                "",
                "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
                "Change infomation by replying with text or image",
                [
                fb_helper_btn(
                    "Delete",
                    "",
                    "btn_delete",
                    False
                    ),
                fb_helper_btn(
                    "Cancel",
                    "",
                    "btn_cancel",
                    False
                    )
                ]
                )
            ]
            )
        )


def location_saved():
    return fb_msg(
        "text",
        "Your Location is saved as _____"
        )


def change_location():
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                "Your Location is _____",
                "",
                "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
                "Tell us your new location or send it to us to change it",
                [
                fb_helper_btn(
                    "Cancel",
                    "",
                    "btn_cancel",
                    False
                    )
                ]
                )
            ]
            )
        )


def start_trading():
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                "My favorite poster of Emma Watson",
                "",
                "http://static.independent.co.uk/s3fs-public/thumbnails/image/2015/03/08/09/emmawatson.jpg",
                "Queesway street",
                [
                fb_helper_btn(
                    "Accept",
                    "",
                    "btn_cancel",
                    False
                    ),
                fb_helper_btn(
                    "Reject",
                    "",
                    "btn_cancel",
                    False
                    )
                ]
                )
            ]
            )
        )


def waiting():
    return fb_msg(
        "template",
        fb_helper_playload_btn(
            "Waiting for the other user to response",
            [
            fb_helper_btn(
                    "Cancel & Reject",
                    "",
                    "btn_cancel",
                    False
                    )
            ]
            )
        )


def rejected():
    return fb_msg(
        "template",
        fb_helper_playload_btn(
            "The other user rejected :(",
            [
            fb_helper_btn(
                    "Find Another",
                    "",
                    "btn_cancel",
                    False
                    )
            ]
            )
        )


def success():
    return fb_msg(
        "template",
        fb_helper_playload_btn(
            "Congratulations! You can chat with the user with the link",
            [
            fb_helper_btn(
                    "Start Chat",
                    "https://www.facebook.com/messages/",
                    "btn_cancel",
                    True
                    )
            ]
            )
        )


def default():
    return fb_msg(
        "text",
        "Wa Ham Zi Tou Ahhhhhh"
        )


def process_for_reply(command,command_args,user,**kwargs):
    
    """
    :param cmd: string
    :param cmdargs: dict
    :param user: BotUser
    :return: a dict as message to be posted back, return None if nothing is to be posted back
    """
    if command == "welcome":
        return welcome_msg()

    elif command == "instructions":
        return instructions(user)

    elif command == "help":
        return help()

    elif command == "inventory":
        return inventory()

    elif command == "create_item":
        return create_item()

    elif command == "edit_item":
        return edit_item()

    elif command == "location_saved":
        return location_saved()

    elif command == "change_location":
        return change_location()

    elif command == "start_trading":
        return start_trading()

    elif command == "rejected":
        return rejected()

    elif command == "waiting":
        return waiting()

    elif command == "success":
        return success()
    else:
        return default()




