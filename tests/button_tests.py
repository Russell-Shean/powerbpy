'''AI generated tests for the _Button class
'''

# pylint: disable=import-error

import os
import builtins
import pytest
from unittest.mock import MagicMock, mock_open

from powerbpy.button import _Button


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def mock_visual_base(monkeypatch, tmp_path):
    """
    Mock _Visual.__init__ so _Button can be tested in isolation.
    """

    def fake_visual_init(
        self,
        *,
        page,
        visual_id,
        height,
        width,
        x_position,
        y_position,
        z_position,
        tab_order,
        parent_group_id,
        alt_text,
        background_color,
        background_color_alpha,
    ):
        self.page = page
        self.dashboard = MagicMock()
        self.dashboard.pages_folder = tmp_path

        self.visual_json_path = tmp_path / f"{visual_id}.json"

        # minimal viable visual_json structure
        self.visual_json = {
            "visual": {
                "visualType": None,
                "objects": {},
                "visualContainerObjects": {},
            }
        }

    monkeypatch.setattr(
        "powerbpy.visual.button._Visual.__init__",
        fake_visual_init,
    )


@pytest.fixture
def base_args():
    return dict(
        page="page1",
        label="My Button",
        visual_id="btn1",
        height=100,
        width=200,
        x_position=10,
        y_position=20,
    )


# ---------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------

@pytest.mark.parametrize("alpha", [-1, 101, 1.5, "10"])
def test_alpha_validation_raises(base_args, mock_visual_base, alpha):
    with pytest.raises(ValueError, match="alpha must be an integer"):
        _Button(**base_args, alpha=alpha)


def test_url_and_page_navigation_mutually_exclusive(base_args, mock_visual_base):
    with pytest.raises(ValueError, match="only supply a url_link OR"):
        _Button(
            **base_args,
            url_link="https://example.com",
            page_navigation_link="page2",
        )


def test_invalid_page_navigation_link_raises(
    base_args, mock_visual_base, monkeypatch
):
    monkeypatch.setattr(os.path, "isdir", lambda _: False)

    with pytest.raises(ValueError, match="page you are trying to link"):
        _Button(
            **base_args,
            page_navigation_link="missing_page",
        )


# ---------------------------------------------------------------------
# Visual JSON structure tests
# ---------------------------------------------------------------------

def test_basic_visual_type_and_metadata(
    base_args, mock_visual_base, monkeypatch
):
    monkeypatch.setattr(builtins, "open", mock_open())

    btn = _Button(**base_args)

    assert btn.visual_json["visual"]["visualType"] == "actionButton"
    assert btn.visual_json["howCreated"] == "InsertVisualButton"


def test_label_is_written_correctly(
    base_args, mock_visual_base, monkeypatch
):
    monkeypatch.setattr(builtins, "open", mock_open())

    btn = _Button(**base_args, label="Download Data")

    text_objects = btn.visual_json["visual"]["objects"]["text"]
    label_expr = text_objects[1]["properties"]["text"]["expr"]["Literal"]["Value"]

    assert label_expr == "'Download Data'"


def test_fill_color_and_alpha_written(
    base_args, mock_visual_base, monkeypatch
):
    monkeypatch.setattr(builtins, "open", mock_open())

    btn = _Button(**base_args, fill_color="#FF0000", alpha=25)

    fill_objects = btn.visual_json["visual"]["objects"]["fill"]
    color_value = (
        fill_objects[1]["properties"]["fillColor"]
        ["solid"]["color"]["expr"]["Literal"]["Value"]
    )
    alpha_value = (
        fill_objects[1]["properties"]["transparency"]
        ["expr"]["Literal"]["Value"]
    )

    assert color_value == "'#FF0000'"
    assert alpha_value == "25D"


# ---------------------------------------------------------------------
# Link behavior tests
# ---------------------------------------------------------------------

def test_url_link_creates_visual_link(
    base_args, mock_visual_base, monkeypatch
):
    monkeypatch.setattr(builtins, "open", mock_open())

    btn = _Button(**base_args, url_link="https://example.com")

    link = btn.visual_json["visual"]["visualContainerObjects"]["visualLink"][0]
    assert link["properties"]["type"]["expr"]["Literal"]["Value"] == "'WebUrl'"
    assert (
        link["properties"]["webUrl"]["expr"]["Literal"]["Value"]
        == "'https://example.com'"
    )


def test_page_navigation_link_creates_visual_link(
    base_args, mock_visual_base, monkeypatch, tmp_path
):
    monkeypatch.setattr(builtins, "open", mock_open())
    monkeypatch.setattr(os.path, "isdir", lambda p: True)

    btn = _Button(**base_args, page_navigation_link="page2")

    link = btn.visual_json["visual"]["visualContainerObjects"]["visualLink"][0]
    assert (
        link["properties"]["type"]["expr"]["Literal"]["Value"]
        == "'PageNavigation'"
    )
    assert (
        link["properties"]["navigationSection"]["expr"]["Literal"]["Value"]
        == "'page2'"
    )


# ---------------------------------------------------------------------
# File write behavior
# ---------------------------------------------------------------------

def test_visual_json_is_written_to_disk(
    base_args, mock_visual_base, monkeypatch
):
    m = mock_open()
    monkeypatch.setattr(builtins, "open", m)

    _Button(**base_args)

    m.assert_called_once()
