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
        self.users = set()
        self.reset()

    def reset(self):
        self.responses = {q.id: {} for q in self.questions}
        self.users = set()

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
        # for now we go on after a single response, rather than
        # waiting for all of them
        for question in self.questions:
            if not self.responses[question.id].keys():
                return question
        return None

        # for question in self.questions:
        #     # if there aren't answers from all registered users, then
        #     # the question is still current
        #     if set(self.responses[question.id].keys()) != self.users:
        #         return question
        # return None

    def respond(self, question_id, response_id, user_id):
        self.responses[question_id][user_id] = response_id


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
