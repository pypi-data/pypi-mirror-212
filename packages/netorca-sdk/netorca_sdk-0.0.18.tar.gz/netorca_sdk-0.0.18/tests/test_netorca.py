from unittest.mock import MagicMock, create_autospec

import pytest

from netorca_sdk.auth import AbstractNetorcaAuth
from netorca_sdk.netorca import Netorca
from netorca_sdk.validations import ContextIn, InvalidContextError


@pytest.fixture
def auth_mock():
    """
    Fixture to create a MagicMock of the AbstractNetorcaAuth class.
    """
    auth = MagicMock(spec=AbstractNetorcaAuth)
    auth.fqdn = "https://api.example.com"
    return auth


@pytest.fixture
def endpoint_caller(auth_mock):
    """
    Fixture to create an instance of Netorca with a MagicMock of the AbstractNetorcaAuth class.
    """
    return Netorca(auth_mock)


@pytest.mark.parametrize(
    "status_code, result, error_message", [(200, {"result": "success"}, None), (404, None, "Could not fetch data")]
)
def test_get(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'get' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result if result else {"error": "not found"}

    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "get", id=1)
    else:
        res = endpoint_caller.caller("deployed_items", "get", id=1)
        auth_mock.get.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(201, {"result": "created"}, None), (400, None, "Could not create data")]
)
def test_create(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'post' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.post.return_value.status_code = status_code
    auth_mock.post.return_value.json.return_value = result if result else {"error": "bad request"}

    data = {"field": "value"}
    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "create", data=data)
    else:
        res = endpoint_caller.caller("deployed_items", "create", data=data)
        auth_mock.post.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(200, {"result": "updated"}, None), (400, None, "Could not update data")]
)
def test_update(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'update' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = result if result else {"error": "bad request"}

    data = {"field": "new_value"}
    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "update", id=1, data=data)
    else:
        res = endpoint_caller.caller("deployed_items", "update", id=1, data=data)
        auth_mock.patch.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(204, {"status": "deleted"}, None), (404, None, "Could not delete data")]
)
def test_delete(status_code, result, error_message, auth_mock, endpoint_caller):
    """
    Test the 'delete' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.delete.return_value.status_code = status_code
    auth_mock.delete.return_value.json.return_value = {"error": "not found"} if status_code == 404 else None

    if error_message:
        with pytest.raises(Exception, match=error_message):
            endpoint_caller.caller("deployed_items", "delete", id=1)
    else:
        res = endpoint_caller.caller("deployed_items", "delete", id=1)
        assert res == result


def test_invalid_endpoint_or_operation(auth_mock, endpoint_caller):
    """
    Test function to ensure that an appropriate ValueError is raised when an invalid
    endpoint or operation is specified when calling the 'caller' method of the 'Netorca'
    class instance.
    """
    with pytest.raises(ValueError, match="Invalid endpoint"):
        endpoint_caller.caller("nonexistent_endpoint", "delete", id=1)

    with pytest.raises(ValueError, match="Invalid operation"):
        endpoint_caller.caller("deployed_items", "nonexistent_operation", id=1)


def test_create_url_context_handling(auth_mock, endpoint_caller):
    """
    Test function to ensure that the 'create_url' method of the 'Netorca' class returns the
    correct URL string for various context and ID values.
    """
    endpoint = "deployed_items"
    url_serviceowner = "https://api.example.com/v1/orcabase/serviceowner/deployed_items/"
    url_consumer = "https://api.example.com/v1/orcabase/consumer/deployed_items/"

    assert endpoint_caller.create_url(endpoint, context=ContextIn.SERVICEOWNER.value) == url_serviceowner
    assert endpoint_caller.create_url(endpoint, context=ContextIn.CONSUMER.value) == url_consumer

    # Test with default context value (assuming ContextIn.SERVICEOWNER is the default)
    assert endpoint_caller.create_url(endpoint) == url_serviceowner

    # Test with an invalid context value
    with pytest.raises(InvalidContextError):
        endpoint_caller.create_url(endpoint, context="wrong_context")

    # Test with a wrong context type (e.g., a string instead of a ContextIn)
    with pytest.raises(InvalidContextError):
        endpoint_caller.create_url(endpoint, context="service_owner")
