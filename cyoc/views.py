from pyramid.httpexceptions import HTTPError
from pyramid.view import view_config
from .models import (
    scene_by_id,
    all_scenes,
    )
from .errors import (
    JSONError,
    JSONUnauthorized,
    )
from .sessions import get_signer


@view_config(route_name='join', request_method='POST', renderer='json')
def join(request):
    """
    Takes {"avatar": id, "scene":id}

    Returns a token
    """
    json = request.json_body
    scene = scene_by_id(json['scene'])
    avatar = request.json_body['avatar']

    # XXX disable this for now, it makes testing harder
    #
    # if avatar in scene.users:
    #     raise JSONError(errors={'avatar': 'in use'})

    if avatar not in scene.avatars:
        raise JSONError(errors={'avatar': 'invalid'})
    scene.users.add(avatar)
    return {'token': get_signer().sign('{}.{}'.format(
        scene.id, avatar
        ))}


@view_config(route_name='lobby', renderer='json')
def avatars(request):
    """
    Returns the currently available avatars in scenes
    """
    return {'sessions': [
        {'id': scene.id,
         'avatars': [
            a for a in scene.avatars if a not in scene.users
            ]} for scene in all_scenes()]
            }


class SessionView(object):
    """
    Add views require a token
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        scheme, token = request.authorization
        creds = get_signer().unsign(token)
        scene_id, user_id = creds.split('.')
        self.scene = scene_by_id(scene_id)
        self.user = user_id

    @view_config(route_name='respond', request_method='POST', renderer='json')
    def respond(self):
        """
        Takes question id and response id
        """
        json = self.request.json_body
        question_id = json['question']
        response_id = json['response']
        self.scene.respond(question_id, response_id, self.user)
        return self._responses(question_id)

    @view_config(route_name='responses', request_method='POST', renderer='json')
    def responses(self):
        """
        Takes a question id

        Responses {user id -> response id}
        """
        json = self.request.json_body
        question_id = json['question']
        return self._responses(question_id)

    def _responses(self, question_id):
        r = []
        for user_id, response_id in self.scene.responses[question_id].items():
            options = self.scene.questions[int(question_id)].options[user_id]
            r = {'user': user_id, 'response':options[int(response_id)]}
        return {'responses': r}

    @view_config(route_name='question', renderer='json')
    def question(self):
        """
        current question: {id, prompt, options[{id, label, type}]}
        """
        question = self.scene.current_question
        if question is None:
            return {'question': None}
        return {
            'question': {
                'id': question.id,
                'prompt': question.text,
                'responses': [
                    {'id': str(i), 'text': o}
                    for i, o in enumerate(question.options[self.user])
                    ]
                }
            }
