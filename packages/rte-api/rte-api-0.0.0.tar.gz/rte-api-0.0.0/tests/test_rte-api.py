'''Testing rte-api__init__()'''

from pathlib import Path
from beetools.beearchiver import Archiver
import api


_PROJ_DESC = __doc__.split('\n')[0]
_PROJ_PATH = Path(__file__)


def project_desc():
    return _PROJ_DESC


b_tls = Archiver(_PROJ_DESC, _PROJ_PATH)


class TestApi:
    def test__init__(self, env_setup_self_destruct):
        """Assert class __init__"""
        env_setup = env_setup_self_destruct
        t_api = api.rte - api("api", env_setup.dir)

        assert t_api.success
        pass

    def test_method_1(self, env_setup_self_destruct):
        """Assert class __init__"""
        env_setup = env_setup_self_destruct
        t_api = api.rte - api("api", env_setup.dir)

        assert t_api.method_1("THis is a test message for Method_1")
        pass

    def test_do_examples(self):
        api.do_examples()


del b_tls
