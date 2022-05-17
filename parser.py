from enum import Enum, auto
from opcode import HAVE_ARGUMENT
import yaml

class PDDLKeys(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    ONEOF = auto()
    LABELED_ONEOF = auto()

# have a function that creates PDDL representation within each class

def have(entity):
    return 

def maybe_have(entity):
    return f"(maybe_have_{entity.lower()} )"

def not_key(entity):
    return f"(not({entity.lower()} ))"

# class Have:
#     def __init__(self, entity) -> None:
#         self.entity = entity.lower()
#     def __repr__(self) -> str:
#         return f"(have_{self.entity} )"

# class MaybeHave():
#     def __init__(self, entity) -> None:
#         self.entity = entity.lower()
#     def __repr__(self) -> str:
#         return f"(maybe_have_{self.entity} )"

def create_tree(nesting):
    for key in nesting:
        if key == "havev ":
            pass

class And:
    def __init__(self, out) -> None:
        self.out = []
        for o in out:
            # convert to nests of have, not, maybe objects
            self.out.append(link(o)(out[o]))

class OneOf:
    def __init__(self, out) -> None:
        self.out = []
        for o in out:
            # convert to nests of have, not, maybe objects
            self.out.append(link(o)(out[o]))

# class Outcome:
#     def __init__(self, name, node_type, out) -> None:
#         self.name = out["name"]
#         self.node_type = 
#         self.out = []
#         del out["name"]
#         for o in out:
#             # convert to nests of have, not, maybe objects
#             self.out.append(link(o)(out[o]))

class Action:
    def __init__(self, name, category, entities=None, dialogue=None, precond=None, effects=None) -> None:
        self.name = name
        self.category = category
        self.entities = entities
        self.dialogue = dialogue
        self.precond = precond
        self.effects = []
        for e in effects:
            for key, val in e.items():
                self.effects.append(link(key)(val))
        # self.effects = [OneOf(e) for e in effects]

    @classmethod
    def deserialize(cls, data):
        return cls(**data)

class AskAction(Action):
    def __init__(self, name, category, entities=None, dialogue=None, precond=None, effects=None) -> None:
        super().__init__(name, category, entities=entities, dialogue=dialogue, precond=precond, effects=effects)
        # self.precond = {'not': ''}

def link(key: str):
    return {
        "ask-for": AskAction,
        "one-of": OneOf,
        "and": And
    }[key]

def grab_yaml_actions():
    return yaml.load(open("rasa_gist.yaml", "r"), Loader=yaml.FullLoader).get("actions")

def create_actions():
    actions = grab_yaml_actions()
    ls = []
    for act_type in actions:
        for action in actions[act_type]:
            ls.append(link(act_type).deserialize(action))
    return ls

if __name__ == "__main__":
    for act in create_actions():
        print(act.__dict__)
