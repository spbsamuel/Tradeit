import re
import json
import requests

from pprint import pprint
from django.utils import timezone

from models import BotUser,Item

PAGE_ACCESS_TOKEN = ""

def create_user(fb_id,user_details):
    return BotUser.objects.create(
            joined = timezone.now(),
            last_activity = timezone.now(),
            fb_user_id = fb_id,
            location = user_details.get("location","Singapore"), #TODO: check this
            lat = user_details.get("lat",1.0),
            lon = user_details.get("long",131),
            profile_pic = user_details.get("profile_pic","#"), #TODO: check
            first_name = user_details.get("first_name"),
            last_name = user_details.get("last_name"),
            gender = user_details.get("gender")
        )

def post_facebook_text(fbid, msg):
    # post a text message to fb
    return post_facebook(fbid,{"text":msg})

def post_facebook(fbid,msg_dict):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":msg_dict})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint("Message posted: {}".format(status.json()))
