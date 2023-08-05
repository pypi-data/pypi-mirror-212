from unittest.mock import patch
from caqui import synchronous
from tests import fake_responses


@patch("requests.request", return_value=fake_responses.GET_URL)
def test_get_url(*args):
    expected = "playground.html"

    assert expected in synchronous.get_url("", "")


@patch("requests.request", return_value=fake_responses.GET_TIMEOUTS)
def test_get_timeouts(*args):
    expected = "implicit"

    assert expected in synchronous.get_timeouts("", "")


@patch("requests.request", return_value=fake_responses.GET_STATUS)
def test_get_status(*args):
    assert synchronous.get_status("").get("value").get("ready") is True


@patch("requests.request", return_value=fake_responses.GET_TITLE)
def test_get_title(*args):
    expected = "Sample page"

    assert synchronous.get_title("", "") == expected

@patch("requests.request", return_value=fake_responses.GET_COOKIES)
def test_get_cookies(*args):
    expected = []

    assert synchronous.get_cookies("", "") == expected

@patch("requests.request", return_value=fake_responses.FIND_ELEMENTS)
def test_find_elements(*args):
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements = synchronous.find_elements("", "", "", "")

    assert element in elements
    assert len(elements) == 3


@patch("requests.request", return_value=fake_responses.GET_PROPERTY_VALUE)
def test_get_property(*args):
    expected = "any_value"

    assert synchronous.get_property("", "", "", "") == expected

@patch("requests.request", return_value=fake_responses.GET_ATTRIBUTE_VALUE)
def test_get_attribute(*args):
    expected = "any_value"

    assert synchronous.get_attribute("", "", "", "") == expected

@patch("requests.request", return_value=fake_responses.GO_TO_PAGE)
def test_go_to_page(*args):
    assert synchronous.go_to_page("", "", "") is True


@patch("requests.request", return_value=fake_responses.CLOSE_SESSION)
def test_close_session(*args):
    assert synchronous.close_session("", "") is True


@patch("requests.request", return_value=fake_responses.GET_TEXT)
def test_get_text(*args):
    expected = "any"

    assert synchronous.get_text("", "", "") == expected


@patch("requests.request", return_value=fake_responses.SEND_KEYS)
def test_send_keys(*args):
    assert synchronous.send_keys("", "", "", "") is True


@patch("requests.request", return_value=fake_responses.CLICK)
def test_click(*args):
    assert synchronous.click("", "", "") is True


@patch("requests.request", return_value=fake_responses.GET_SESSION)
def test_get_session(*args):
    expected = "4358a5b53794586af59678fc1653dc40"

    assert synchronous.get_session("", "") == expected


@patch("requests.request", return_value=fake_responses.FIND_ELEMENT)
def test_find_element(*args):
    expected = "0.8851292311864847-1"

    assert synchronous.find_element("", "", "", "") == expected
