from django.utils import timezone

from fbmbot.models import Item
from fbmbot.utils import post_facebook
from common import States,Commands
from matcher import find_match
from processor.utils import get_url,DEFAULT_IMG_URL

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
    if buttons and len(buttons) > 0:
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
    if (item_ls):
        return fb_msg(
            "template",
            fb_helper_playload_generic(
                item_ls
            )
        )
    else:
        return fb_msg(
            "text",
            "No items so far"
        )


def create_item(user,cmd_args):
    """
    cmd_args: url
    """

    item = Item.objects.create(
        owner = user,
        image_url =cmd_args['img_url'][0]['payload']['url'],
        description = cmd_args.get("description",DEFAULT_DESCRIPTION),
        date_created = timezone.now(),
        last_active = timezone.now(),
    )
    user.last_state = States.ADD_NEW
    user.save()
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
                    "btn_cancel",
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
    :param cmd_args: url,description
    :return:
    """
    item = user.item_set.filter(is_editing=True)[0]
    new_url = get_url(cmd_args,use_default=False)
    item.image_url = new_url if new_url else item.image_url
    item.description = cmd_args.get("text",item.description)
    button_ls = [
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
    if (item.image_url!=DEFAULT_IMG_URL and item.description!=DEFAULT_DESCRIPTION):
        for i in user.item_set.all():
            i.active = False
            i.save()
        item.active = True
        item.save()
        button_ls.append(fb_helper_btn(
            "Trade This",
            "",
            "btn_trade_active",
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

# helper function
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


def start_trading(user):
    active_item = user.item_set.filter(active=True)[0]
    active_item.is_editing = False
    active_item.save()
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
                              fb_helper_btn("Cancel","","btn_cancel_trade",False)
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

def cancel_trading(user):
    items = user.item_set.filter(active=True,deleted=False)
    for item in items:
        item.active = False
        item.save()
    user.last_state = States.STATIC
    user.save()
    return fb_msg(
        "text",
        "Trading Cancelled..."
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
        return instructions()

    elif command == "help":
        return help()

    elif command == "inventory":
        return inventory(user)

    elif command == "createitem":
        return create_item(user,command_args)

    elif command == "edititem":
        return edit_item(user,cmd_args=command_args)

    elif command == "locationsaved":
        return location_saved()

    elif command == "changelocation":
        return change_location()

    elif command == "starttrading":
        return start_trading(user)

    elif command == "rejected":
        return rejected()

    elif command == "waiting":
        return waiting()

    elif command == Commands.CANCEL_TRADING:
        return cancel_trading(user)

    elif command == "success":
        return success()
    else:
        return default()
