import pytest
from tools.sessions import SoapSession


@pytest.fixture(scope='module')
def soap_session(envs):
    """Взаимодействие с SOAP session"""
    session = SoapSession(base_url=envs.soap_address)
    return session
