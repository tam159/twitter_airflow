import json
import requests
from datetime import date

from config import AI_AGE_GENDER_URL as url
from config import AI_AGE_GENDER_HEADERS as headers


def avatar_resolution(user):
    return {
        "profile_image_url": user.profile_image_url.replace("normal", "400x400"),
        "profile_image_url_https": user.profile_image_url_https.replace(
            "normal", "400x400"
        ),
    }


def age_gender_pridiction(user):
    age_gender_dict = {}
    payload = {
        "image_url": user.profile_image_url_https.replace("normal", "400x400"),
        "user_id": user.id,
        "screen_name": user.screen_name,
    }
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        response_code = json.loads(response.text)["code"]
        response_body = json.loads(response.text)["body"]
        response_version = json.loads(response.text)["version"]

        if all([response_code == "success", len(response_body) == 1, response_version]):
            age_gender_dict = response_body[0]
            if "age" in age_gender_dict:
                age_gender_dict["birthyear"] = (
                    date.today().year - age_gender_dict["age"]
                )
            age_gender_dict.update(ag_ai_version=response_version)
        return age_gender_dict
    except:
        return {}


# print(age_gender_pridiction('https://pbs.twimg.com/profile_banners/2935022588/1510500856'))
# print(age_gender_pridiction('http://pbs.twimg.com/profile_images/1039401580502507525/Vt-_sH5d_400x400.jpg'))

# payload = {
#     "image_url": "http://pbs.twimg.com/profile_images/1039401580502507525/Vt-_sH5d_400x400.jpg"
# }
# response = requests.post(url=url, headers=headers, data=json.dumps(payload))
# print(json.loads(response.text)["body"])
