from unittest.mock import patch

import pytest

from app.models.player import Player
from app.models.cards import PlayerCards
from app.models.battle import Battle


PLAYER_RESPONSE = {
    "tag": "#C2C0L2QLR",
    "name": "khojoii",
    "trophies": 12332,
    "expLevel": 58,
    "wins": 2727,
    "losses": 2987,
}

CARDS_RESPONSE = {
    "cards": [
        {"id": 1, "name": "Flying Machine", "level": 10, "maxLevel": 14, "iconUrls": {"medium": "https://example.com/flying_machine.png"}},
        {"id": 2, "name": "Goblin Giant", "level": 7, "maxLevel": 11},
    ]
}

BATTLES_RESPONSE = [
    {
        "type": "PvP",
        "arena": {"id": 54000015, "name": "Legendary Arena"},
        "team": [{"tag": "#A", "name": "P1", "crowns": 1, "startingTrophies": 5000}],
        "opponent": [{"tag": "#B", "name": "P2", "crowns": 0, "startingTrophies": 4900}],
    }
]

ERROR_RESPONSE = {"reason": "notFound"}


@patch("app.tools.player.api")
def test_get_player_info(mock_api):
    mock_api.get_player.return_value = PLAYER_RESPONSE
    from app.tools.player import get_player_info

    result = get_player_info("#C2C0L2QLR")
    assert isinstance(result, Player)
    assert result.tag == "#C2C0L2QLR"
    assert result.name == "khojoii"
    assert result.trophies == 12332
    assert result.expLevel == 58
    assert result.wins == 2727
    assert result.losses == 2987
    mock_api.get_player.assert_called_once_with("#C2C0L2QLR")


@patch("app.tools.player.api")
def test_get_player_info_api_error(mock_api):
    mock_api.get_player.side_effect = Exception("API error 404: notFound")
    from app.tools.player import get_player_info

    with pytest.raises(Exception, match="API error 404"):
        get_player_info("#INVALID")


@patch("app.tools.cards.api")
def test_get_player_cards(mock_api):
    mock_api.get_player_cards.return_value = CARDS_RESPONSE
    from app.tools.cards import get_player_cards

    result = get_player_cards("#C2C0L2QLR")
    assert isinstance(result, PlayerCards)
    assert len(result.items) == 2
    assert result.items[0].name == "Flying Machine"
    assert result.items[0].level == 10
    assert result.items[1].name == "Goblin Giant"
    assert result.items[1].maxLevel == 11
    mock_api.get_player_cards.assert_called_once_with("#C2C0L2QLR")


@patch("app.tools.cards.api")
def test_get_player_cards_empty(mock_api):
    mock_api.get_player_cards.return_value = {}
    from app.tools.cards import get_player_cards

    result = get_player_cards("#EMPTY")
    assert len(result.items) == 0


@patch("app.tools.battles.api")
def test_get_recent_battles(mock_api):
    mock_api.get_recent_battles.return_value = BATTLES_RESPONSE
    from app.tools.battles import get_recent_battles

    result = get_recent_battles("#C2C0L2QLR")
    assert len(result) == 1
    assert isinstance(result[0], Battle)
    assert result[0].type == "PvP"
    assert result[0].arena["name"] == "Legendary Arena"
    assert result[0].team[0].name == "P1"
    assert result[0].opponent[0].name == "P2"
    mock_api.get_recent_battles.assert_called_once_with("#C2C0L2QLR")


@patch("app.tools.battles.api")
def test_get_recent_battles_empty(mock_api):
    mock_api.get_recent_battles.return_value = []
    from app.tools.battles import get_recent_battles

    result = get_recent_battles("#NOBATTLES")
    assert len(result) == 0
