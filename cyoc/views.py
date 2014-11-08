from pyramid.httpexceptions import HTTPError
from pyramid.view import view_config
from .models import (
    scene_by_id,
    scenes,
    )
from .errors import (
    JSONError,
    JSONUnauthorized,
    )
from .sessions import signer


@view_config(route_name='join', renderer='json')
def join(request):
    """
    Takes a avatar id, scene id

    Returns a token
    """
    json = request.json_body
    scene = scene_by_id(json['scene'])
    avatar = request.json_body['avatar']
    if avatar in scene.users:
        raise JSONError(errors={'avatar': 'in use'})
    if avatar not in scene.avatars:
        raise JSONError(errors={'avatar': 'invalid'})
    scene.users.append(avatar)
    return {'token': signer.sign('{}.{}'.format(
        scene.id, avatar
        ))}


@view_config(route_name='lobby', renderer='json')
def avatars(request):
    """
    Returns the currently available avatars in scenes
    """
    scene = scenes[0] # XXX we have only one session right now
    return {'sessions': [{
        'id': scene.id,
        'avatars': [
            a for a in session.avatars if a not in session.users
            ]}]
            }


class SessionView(object):
    """
    Add views require a token
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.json = request.json_body
        token = signer.unsign(self.json['session'])
        scene_id, user_id = token.split('.')
        self.scene = scene_by_id(scene_id)
        self.user = user_id

    @view_config(route_name='respond', renderer='json')
    def respond(self):
        """
        Takes question id and response id
        """
        question_id = self.json['question']
        response_id = self.json['response']
        self.scene.questions[question_id].responses[self.user] = response_id
        return {'ok': True}

    @view_config(route_name='responses', renderer='json')
    def responses(self):
        """
        Takes a question id

        Responses {user id -> response id}
        """
        question_id = self.json['question']
        return {'responses': self.scene.responses[question_id]}

    @view_config(route_name='question', renderer='json')
    def question(self):
        """
        current question: {id, prompt, options[{id, label, type}]}
        """
        question = self.scene.current_question
        return {
            'question': {
                'id': question.id,
                'prompt': question.text,
                'responses': [
                    {'id': str(i), 'text': o}
                    for i, o in enumerate(question.options)
                    ]
                }
            }
