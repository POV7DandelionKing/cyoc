from pyramid.config import Configurator
from .models import setup_scene
from .sessions import setup_signer


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    setup_scene(settings['scenes.config'])
    setup_signer(settings['scenes.secret'])

    config = Configurator(settings=settings)

    config.add_route('reset', '/reset')

    config.add_route('join', '/join')
    config.add_route('lobby', '/lobby')

    config.add_route('respond', '/respond')
    config.add_route('responses', '/responses')
    config.add_route('question', '/question')

    config.scan()
    return config.make_wsgi_app()
