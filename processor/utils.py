DEFAULT_IMG_URL = "https://pbs.twimg.com/profile_images/608080301932175360/OEeZ2ydH.jpg"

def get_url(cmd_args,use_default=True):
    try:
        return cmd_args['img_url'][0]['payload']['url']
    except:
        return DEFAULT_IMG_URL if use_default else None