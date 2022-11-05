import requests

import vars as v

def install():
    pass

def check():
    api_response = requests.get(
        "https://api.github.com/repos/not-nef/onyx/releases"
    )

    try:
        latest_tag = next(iter(api_response.json()))["tag_name"]

        if float(str(latest_tag).removeprefix("v")) > float(v.ver.split(" ")[0]):
            return True
        else:
            return False
    except:
        return "rate limit"