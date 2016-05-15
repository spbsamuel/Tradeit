DEFAULT_IMG_URL = "https://scontent-sin1-1.xx.fbcdn.net/v/t34.0-12/13233383_120300000003937368_1961529093_n.png?oh=985336d530a9117a3484fa4a88bcc966&oe=573A019C"

def get_url(cmd_args,use_default=True):
    try:
        return cmd_args['img_url'][0]['payload']['url']
    except:
        return DEFAULT_IMG_URL if use_default else None