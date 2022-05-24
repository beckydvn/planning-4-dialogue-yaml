import yaml
import json

yaml = yaml.load(open("rasa_gist.yaml", "r"), Loader=yaml.FullLoader)
# print(json.dumps(yaml, indent=4))

json_config = {}
json_config["name"] = yaml["name"]
json_config["intents"] = {intent["intent"] : intent["examples"] for intent in yaml["nlu"]}
json_config["context-variables"] = {}
for var, info in yaml["context-variables"].items():
    json_config["context-variables"][var] = {}
    for key, val in info.items():
        if key == "known":
            key = "certainty"
            if val == "true":
                val = "Known"
            elif val == "false":
                val = "Unknown"
            else:
                val = "Uncertain"
        json_config["context-variables"][var][key] = val
# still have to: fix conditions, fix $$ syntax, create clarify effects, update effect syntax etc.
json_config["actions"] = {}
for act_type in yaml["actions"]:
    for act, info in yaml["actions"][act_type].items():
        json_config["actions"][act] = {}
        json_config["actions"][act]["name"] = act
        json_config["actions"][act]["type"] = act_type
        for key, val in info.items():
            if key == "condition":
                conditions = []
                for cond_key, cond_config in info[key].items():
                    for cond_config_key, cond_val in cond_config.items():
                        if cond_config_key in ["known", "config"]:
                            conditions.append([cond_key, cond_val])
                        elif cond_config_key == "or":
                            pass
                val = conditions
            json_config["actions"][act][key] = val

print(json.dumps(json_config, indent=4))