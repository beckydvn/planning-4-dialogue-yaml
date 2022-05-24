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
                val = [[cond_key, cond_val] for cond_key, cond_val in info[key].items()] 
            json_config["actions"][act][key] = val

print(json.dumps(json_config, indent=4))