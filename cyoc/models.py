import yaml

class TextQuestion(object):
    def __init__(self, id, text, options):
        self.id = id
        self.text = text
        self.options = options


class Scene(object):

    def __init__(self, id, avatars, questions):
        self.id = id
        self.avatars = avatars
        self.questions = questions
        self.users = []
        self.responses = {q.id: [] for q in questions}
        self.current = 0

    @classmethod
    def from_config(cls, config):
        scene = config['scene']
        id = scene['id']
        avatars = scene['avatars']
        questions = [
            TextQuestion(str(i), q['question'], q['answers'])
            for i, q in enumerate(scene['questions'])
            ]
        return cls(id, avatars, questions)

    @property
    def current_question(self):
        return self.questions[self.current]


# XXX in memory persistence only right now
scenes = {}


def scene_by_id(id):
    return scenes[id]

def all_scenes():
    return scenes.values()

def setup_scene(filename):
    global session
    with open(filename) as f:
        config = yaml.load(f)
        scene = Scene.from_config(config)
        scenes[scene.id] = scene
