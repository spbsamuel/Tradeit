# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone

from nlp import interpret
from processor import process_for_reply
from matcher import find_match
from fbmbot.models import BotUser
from fbmbot.utils import create_user,post_facebook_text,post_facebook


#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAAB0FiCOfH8BAML86kAIzSC6OwyyohpEjZAAfer9uZA3BZCpcCEJkVz2VkDahsnMP2uOZCOAgHk7xICSNKVjKifgEHW9dhg4cZCQlVvK4oXsaf2hP3PnWYtwUby1ZAy0DY7InWtCJVfPqLqqeJPjIvmDVtssx99G2SAZArFGfedtwZDZD"
VERIFY_TOKEN = "2318934571"
ASK_FOR_CLARIFICATION = "Sorry, I dun understand your message"

def landing_page(request):
    return render(request,"landing.html")

def is_btn_postback(msg_obj):
    return "postback" in msg_obj.keys() and "message" not in msg_obj.keys()


# Create your views here.
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # get and save user profile if this is the first time
                user = self.get_and_save_profile(message['sender']['id'])
                # Print the message to the terminal
                pprint("message received: {}".format(message))
                if ("message" in message.keys()):
                    msg_text=message['message'].get("text","")
                    msg_obj = message['message']
                elif("postback" in message.keys()):
                    msg_text = message['postback']['payload']
                    msg_obj = message['postback']
                else:
                    return HttpResponse()
                cmd,cmd_args = interpret(msg_text,user=user,msg_obj=msg_obj)
                if (cmd==None):
                    # tell the user we dun understand
                    post_facebook_text(message['sender']['id'],ASK_FOR_CLARIFICATION)
                    return HttpResponse()
                else:
                    reply = process_for_reply(cmd,cmd_args,user)
                    if (reply):
                        post_facebook(fbid=user.fb_user_id,msg_dict=reply)

        return HttpResponse()

    def get_and_save_profile(self,sender_id):
        # return BotUser, and create it
        # check whether the id is there
        user = BotUser.objects.filter(fb_user_id=sender_id)
        if (user):
            return user[0]
        # if not, ask for the profile
        user_details_url = "https://graph.facebook.com/v2.6/%s"%sender_id
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
        user_details = requests.get(user_details_url, user_details_params).json()
        user = create_user(fb_id=sender_id,user_details=user_details)
        return user

