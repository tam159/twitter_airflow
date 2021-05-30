def entities_url(user):
    entities_url_dict = {
        "entities_display_url": None,
        "entities_expanded_url": None,
        "entities_url": None,
    }
    if "url" in user.entities:
        if "urls" in user.entities["url"]:
            if len(user.entities["url"]["urls"]) == 1:
                if "display_url" in user.entities["url"]["urls"][0]:
                    entities_url_dict["entities_display_url"] = user.entities["url"][
                        "urls"
                    ][0]["display_url"]
                if "expanded_url" in user.entities["url"]["urls"][0]:
                    entities_url_dict["entities_expanded_url"] = user.entities["url"][
                        "urls"
                    ][0]["expanded_url"]
                if "url" in user.entities["url"]["urls"][0]:
                    entities_url_dict["entities_url"] = user.entities["url"]["urls"][0][
                        "url"
                    ]
    return entities_url_dict
