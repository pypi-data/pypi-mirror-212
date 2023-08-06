from pathlib import Path

import pytest

from pwproxy.run import Run

pytest_plugins = "pytester"


def test_run(pytester: pytest.Pytester, tmp_path: Path):
    path = pytester.makepyfile("""
from playwright.sync_api import Route

def replace_resp(route: Route):
    if "http://example.com/" in route.request.url:
        response = route.fetch()
        body = response.text()
        body = body.replace("Example Domain", "Goodo")
        route.fulfill(
            body=body
        )

addons = [
    replace_resp
] 
    """)

    page = Run.run(path, url="http://example.com/", headless=True)
    assert "Goodo" == page.inner_text("h1")


@pytest.mark.skip
def test_cli(pytester: pytest.Pytester, tmp_path: Path):
    path = pytester.makepyfile("""
from playwright.sync_api import Route

def replace_resp(route: Route):
    if "http://example.com/" in route.request.url:
        response = route.fetch()
        body = response.text()
        body = body.replace("Example Domain", "Goodo")
        route.fulfill(
            body=body
        )

addons = [
    replace_resp
]
    """)
    # subprocess.run([
    #     "pwp", "-s", path,
    #     "--url", "http://example.com/",
    #     "--headless"
    # ])
    # assert "Goodo" == page.inner_text("h1")
    import os
    os.system(f"pwp -s {path} --url http://example.com/ --headless")
