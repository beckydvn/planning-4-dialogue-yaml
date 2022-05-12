from enum import Enum, auto
import yaml

class Nest(Enum):
    AND = auto()
    OR = auto()

# class Outcome:
#     def __init__(self, nest: Nest) -> None:
#         self.name = name
#         self.category = category

class Action:
    def __init__(self, name, category, entities=None, dialogue=None, precond=None, effects=None) -> None:
        self.name = name
        self.category = category
        self.entities = entities
        self.dialogue = dialogue
        self.precond = precond
        self.effects = effects

    @classmethod
    def deserialize(cls, data):
        """Converts a json object to an Action."""
        return cls(**data)

class AskAction(Action):
    def __init__(self, name, category, entities=None, dialogue=None, precond=None, effects=None) -> None:
        super().__init__(name, category, entities=entities, dialogue=dialogue, precond=precond, effects=effects)
        # self.precond = {'not': ''}

def link_constructor(key: str):
    return {
        "ask-for": AskAction
    }[key]

def grab_yaml_actions():
   return yaml.load(open("rasa_gist.yaml", "r"), Loader=yaml.FullLoader).get("actions")

def create_actions():
    actions = grab_yaml_actions()
    ls = []
    for act_type in actions:
        for action in actions[act_type]:
            ls.append(link_constructor(act_type).deserialize(action))
    return ls

if __name__ == "__main__":
    for act in create_actions():
        print(act.__dict__)