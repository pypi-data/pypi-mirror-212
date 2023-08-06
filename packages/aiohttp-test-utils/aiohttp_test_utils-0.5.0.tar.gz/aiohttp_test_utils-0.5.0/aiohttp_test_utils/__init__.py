__version__ = '0.5.0'
import atexit
from asyncio import new_event_loop
from unittest.mock import patch

from decouple import config
from pytest import fixture


def init_tests():
    global RECORD_MODE, OFFLINE_MODE, TESTS_PATH, REMOVE_UNUSED_TESTDATA

    config.search_path = TESTS_PATH = config._caller_path()

    RECORD_MODE = config('RECORD_MODE', False, cast=bool)
    OFFLINE_MODE = config('OFFLINE_MODE', False, cast=bool) and not RECORD_MODE
    REMOVE_UNUSED_TESTDATA = config('REMOVE_UNUSED_TESTDATA', False, cast=bool) and OFFLINE_MODE


class EqualToEverything:
    def __eq__(self, other):
        return True

class FakeResponse:

    file = ''
    url = EqualToEverything()
    history = ()

    async def read(self):
        with open(self.file, 'rb') as f:
            content = f.read()
        return content


def session_fixture_factory(main_module):

    @fixture(scope='session', autouse=True)
    async def session():
        if OFFLINE_MODE:

            class FakeSession:
                @staticmethod
                async def get(*_, **__):
                    return FakeResponse()

            main_module.SESSION = FakeSession()
            yield
            return

        session = main_module.Session()

        if RECORD_MODE:
            original_get = session.get

            async def recording_get(*args, **kwargs):
                resp = await original_get(*args, **kwargs)
                content = await resp.read()
                with open(FakeResponse.file, 'wb') as f:
                    f.write(content)
                return resp

            session.get = recording_get

        yield
        await session.close()

    return session


@fixture(scope='session')
def event_loop():
    loop = new_event_loop()
    yield loop
    loop.close()


def remove_unsed_file_names():
    if REMOVE_UNUSED_TESTDATA is not True:
        return
    import os
    for filename in set(os.listdir(f'{TESTS_PATH}/testdata/')) - USED_FILENAMES:
        os.remove(f'{TESTS_PATH}/testdata/{filename}')
        print(f'removed unsed file: {filename}')


USED_FILENAMES = set()
atexit.register(remove_unsed_file_names)


def file(filename):
    if REMOVE_UNUSED_TESTDATA is True:
        USED_FILENAMES.add(filename)
    return patch.object(FakeResponse, 'file', f'{TESTS_PATH}/testdata/{filename}')
