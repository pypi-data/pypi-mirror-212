from pytest import fixture, mark
from caqui import asynchronous, synchronous
from tests.constants import PAGE_URL


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
        }
    }
    session = synchronous.get_session(driver_url, capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    synchronous.close_session(driver_url, session)


@mark.asyncio
async def test_go_back(__setup):
    driver_url, session = __setup

    assert synchronous.go_back(driver_url, session) is True
    assert await asynchronous.go_back(driver_url, session) is True


@mark.asyncio
async def test_get_url(__setup):
    driver_url, session = __setup
    expected = "playground.html"

    assert expected in synchronous.get_url(driver_url, session)
    assert expected in await asynchronous.get_url(driver_url, session)


@mark.asyncio
async def test_get_timeouts(__setup):
    driver_url, session = __setup
    expected = "implicit"

    assert expected in synchronous.get_timeouts(driver_url, session)
    assert expected in await asynchronous.get_timeouts(driver_url, session)


@mark.asyncio
async def test_get_status(__setup):
    driver_url, _ = __setup
    expected = "ready"
    assert expected in synchronous.get_status(driver_url).get("value")
    response = await asynchronous.get_status(driver_url)
    assert expected in response.get("value")


@mark.asyncio
async def test_get_title(__setup):
    driver_url, session = __setup
    expected = "Sample page"

    assert synchronous.get_title(driver_url, session) == expected
    assert await asynchronous.get_title(driver_url, session) == expected


@mark.asyncio
async def test_find_elements(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    elements = synchronous.find_elements(
        driver_url, session, locator_type, locator_value
    )
    async_elements = await asynchronous.find_elements(
        driver_url, session, locator_type, locator_value
    )

    assert len(elements) > 0
    assert len(async_elements) > 0


@mark.asyncio
async def test_find_element(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    assert (
        synchronous.find_element(driver_url, session, locator_type, locator_value)
        is not None
    )
    assert (
        await asynchronous.find_element(
            driver_url, session, locator_type, locator_value
        )
        is not None
    )


@mark.asyncio
async def test_get_property(__setup):
    driver_url, session = __setup
    text = "any_value"
    locator_type = "xpath"
    locator_value = "//input"
    property = "value"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.send_keys(driver_url, session, element, text)

    assert synchronous.get_property(driver_url, session, element, property) == text
    assert (
        await asynchronous.get_property(driver_url, session, element, property) == text
    )


@mark.asyncio
async def test_get_text(__setup):
    driver_url, session = __setup
    expected = "end"
    locator_type = "xpath"
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.get_text(driver_url, session, element) == expected
    assert synchronous.get_text(driver_url, session, element) == expected


@mark.asyncio
async def test_send_keys(__setup):
    driver_url, session = __setup
    text_async = "any_async"
    text_sync = "any_sync"
    locator_type = "xpath"
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert (
        await asynchronous.send_keys(driver_url, session, element, text_async) is True
    )
    assert synchronous.send_keys(driver_url, session, element, text_sync) is True


@mark.asyncio
async def test_click(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.click(driver_url, session, element) is True
    assert synchronous.click(driver_url, session, element) is True
