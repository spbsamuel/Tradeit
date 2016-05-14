from django.utils import timezone

from fbmbot.models import Item
from fbmbot.utils import post_facebook
from common import States
from matcher import find_match

DEFAULT_IMG_URL = "https://pbs.twimg.com/profile_images/608080301932175360/OEeZ2ydH.jpg"
DEFAULT_DESCRIPTION = "Your Item Description"

def fb_helper_btn(title,url,payload,web_url=True):
    type = "web_url" if web_url else "postback"
    return {"type": type, "title":title,"payload":payload}

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
                    "View Inventory",
                "",
                "btn_inventory",
                False
                ),
                    fb_helper_btn(
                        "Set Location",
                        "",
                        "btn_set_location",
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
        "Hey there! Don't worry you can use these cmds:\nTrade: 'start trading'\nView inventory: 'inventory'"
        )


def inventory(user):
    items = user.item_set.all()
    #for item in item_set push element into element_list
    item_ls = []
    for item in items:
        item_ls.append(
            fb_helper_element(
                item.description,
            "",
            item.image_url,
            "",
            [
            fb_helper_btn(
                "Trade This",
                "",
                "btn_start_trade_{}".format(item.id),
                False
                ),
            fb_helper_btn(
                "Edit This",
                "",
                "btn_edit_{}".format(item.id),
                False
                )
            ]
            )
        )
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            item_ls
        )
    )


def create_item(user,cmd_args):
    """
    cmd_args: url
    """

    item = Item.objects.create(
        owner = user,
        image_url =cmd_args.get("url",DEFAULT_IMG_URL),
        description = cmd_args.get("description",DEFAULT_DESCRIPTION),
        date_created = timezone.now()
    )

    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                item.description,
                "",
                item.image_url,
                "Add Item description by replying",
                [
                fb_helper_btn(
                    "Cancel",
                    "",
                    "btn_delete_{}",format(item.id),
                    False
                    )
                ]
                )
            ]
            )
        )


def edit_item(user,cmd_args):
    """
    :param user:
    :param cmd_args: url,description,id
    :return:
    """
    #if id is set use item(id)
    #set all else to false
    item = user.item_set.filter(is_editing=True)
    item.image_url = cmd_args.get("url",item.image_url)
    item.description = cmd_args.get("url",item.description)
    button_ls = [
                fb_helper_btn(
                    "Delete",
                    "",
                    "btn_delete_{}".format(item.id),
                    False
                    ),
                fb_helper_btn(
                    "Save",
                    "",
                    "btn_cancel".format(item.id),
                    False
                    )
                ]
    if (item.image_url!=DEFAULT_IMG_URL and item.description!=DEFAULT_DESCRIPTION):
        button_ls.append(fb_helper_btn(
            "Trade This",
            "",
            "btn_start_trade_{}".format(item.id),
            False
        ))
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                item.description,
                "",
                item.image_url,
                "Change information by replying with text or image",
                button_ls
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
                "Send us your location to change it"
                )
            ]
            )
        )

def get_match_msg(user,item):
    return fb_msg(
        "template",
        fb_helper_playload_generic(
            [
            fb_helper_element(
                item.description,
                "",
                item.image_url,
                user.location,
                [
                fb_helper_btn(
                    "Accept",
                    "",
                    "btn_accept",
                    False
                    ),
                fb_helper_btn(
                    "Reject",
                    "",
                    "btn_reject",
                    False
                    )
                ]
                )
            ]
            )
        )


def start_trading(user):
    #if no item create new
    #if id is set use item(id)
    active_item = user.item_set.filter(active=True)[0]
    matched_items = find_match(active_item)
    user.last_state = States.START_TRADING
    user.save()
    if (matched_items):
        matched_item = matched_items[0]
        other_user = matched_item.owner
        msg = get_match_msg(user=other_user,item=matched_item)
        post_facebook(fbid=user.fb_user_id,msg_dict=msg)
        msg = get_match_msg(user=user,item=active_item)
        post_facebook(fbid=other_user.fb_user_id,msg_dict=msg)
    else:
        return fb_msg(type="template",
                      payload=fb_helper_playload_btn(
                          "searching for match...",
                          [
                              fb_helper_btn("Cancel","","btn_cancel",False)
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
                    "btn_reject",
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
                    "btn_start_trade",
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
                    "",
                    True
                    )
            ]
            )
        )

def delete():
    return fb_msg(
        "text",
        "Item Deleted"
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

    elif command == "createitem":
        return create_item(user,command_args)

    elif command == "edititem":
        return edit_item()

    elif command == "locationsaved":
        return location_saved()

    elif command == "changelocation":
        return change_location()

    elif command == "starttrading":
        return start_trading()

    elif command == "rejected":
        return rejected()

    elif command == "waiting":
        return waiting()

    elif command == "success":
        return success()
    else:
        return default()
