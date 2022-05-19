import yaml
import json

def parse_outcome(outcome):
    if isinstance(outcome, dict):
        for key, val in outcome.items():
            if key == "have":
                return f"(have_{val})"
            elif key == "maybe_have":
                return f"(maybe_have_{val})"
            elif key == "one-of":
                return "\n(one-of(\n\t{0}\n)".format('\n\t'.join([parse_outcome(outcome) for outcome in val]))
            elif key == "forced-follow-up":
                return '\n\t'.join([f"not(can-do_({act}))" for act in action_set - {val}])
            else:
                return f"\n(and({parse_outcome(val)})"
    else:
        return f"\nand({outcome})"


yaml = yaml.load(open("rasa_gist.yaml", "r"), Loader=yaml.FullLoader)
to_json = json.dumps(yaml, indent=4)
print(to_json)

# action_set = {a["name"] for act_type in action_yaml for a in action_yaml[act_type]}
# pddl = ""
# for act_type in action_yaml:
#     for action in action_yaml[act_type]:
#         pddl += "(:action {0}\n\t:effect ".format(action["name"])
#         if "need" in action.keys():
#             for outcome in action["need"]:
#                 pddl += parse_outcome(outcome)
#         if "effects" in action.keys():
#             for outcome in action["effects"]:
#                 pddl += parse_outcome(outcome)
#         pddl += "\n)"
# print(pddl)
