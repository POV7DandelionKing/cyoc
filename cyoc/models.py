import random
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
        _answers[self.id] = {}
        for question in self.questions:
            _answers[self.id][question.id] = {}

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

    def respond(self, question_id, response_id, user_id):
        _answers[self.id][question_id][user_id] = response_id

    def responses(self, question_id):
        answers = dict(_answers[self.id][question_id])

        # XXX for now we fill in fake responses for users if there
        # aren't any in the db
        for avatar in self.avatars:
            if avatar not in answers:
                q = self.questions[int(question_id)]
                user_options = q.options[avatar]
                option_ids = [str(i) for i in range(len(user_options))]
                answers[avatar] = random.choice(option_ids)
        return answers


# XXX in memory persistence only right now
_scenes = {}
_answers = {}

def scene_by_id(id):
    return _scenes[id]

def all_scenes():
    return _scenes.values()

def setup_scene(filename):
    with open(filename) as f:
        config = yaml.load(f)
        scene = Scene.from_config(config)
        _scenes[scene.id] = scene
