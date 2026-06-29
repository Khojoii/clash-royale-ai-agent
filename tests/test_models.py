from app.models.player import Player
from app.models.cards import Card, PlayerCards
from app.models.battle import BattlePlayer, Battle
from app.models.clan import Clan


def test_player_model():
    p = Player(tag="#ABC123", name="TestPlayer", trophies=5000, expLevel=14, wins=100, losses=50)
    assert p.tag == "#ABC123"
    assert p.name == "TestPlayer"
    assert p.trophies == 5000
    assert p.expLevel == 14
    assert p.wins == 100
    assert p.losses == 50


def test_player_defaults():
    p = Player(tag="#X", name="X", trophies=0, expLevel=1, wins=0, losses=0)
    assert p.wins == 0
    assert p.losses == 0


def test_card_model():
    c = Card(id=1, name="Arrows", level=13, maxLevel=14, iconUrls={"medium": "https://example.com/icon.png"})
    assert c.id == 1
    assert c.name == "Arrows"
    assert c.level == 13
    assert c.maxLevel == 14
    assert c.iconUrls == {"medium": "https://example.com/icon.png"}


def test_card_icon_defaults_to_none():
    c = Card(id=2, name="Fireball", level=11, maxLevel=14)
    assert c.iconUrls is None


def test_player_cards():
    cards = PlayerCards(items=[
        {"id": 1, "name": "Arrows", "level": 13, "maxLevel": 14},
        {"id": 2, "name": "Fireball", "level": 11, "maxLevel": 14},
    ])
    assert len(cards.items) == 2
    assert cards.items[0].name == "Arrows"
    assert cards.items[1].name == "Fireball"


def test_battle_player_model():
    bp = BattlePlayer(tag="#XYZ", name="Opponent", crowns=2, trophies=4800)
    assert bp.tag == "#XYZ"
    assert bp.crowns == 2


def test_battle_model():
    arena = {"id": 54000015, "name": "Legendary Arena"}
    team = [{"tag": "#A", "name": "P1", "crowns": 1, "trophies": 5000}]
    opponent = [{"tag": "#B", "name": "P2", "crowns": 0, "trophies": 4900}]
    b = Battle(type="PvP", arena=arena, team=team, opponent=opponent)
    assert b.type == "PvP"
    assert b.arena["name"] == "Legendary Arena"
    assert len(b.team) == 1
    assert b.team[0].name == "P1"
    assert b.opponent[0].name == "P2"


def test_clan_model():
    c = Clan(tag="#CLAN", name="Test Clan", clanScore=50000, clanWarTrophies=2000, members=48, type="open")
    assert c.tag == "#CLAN"
    assert c.name == "Test Clan"
    assert c.clanScore == 50000
    assert c.members == 48
    assert c.type == "open"
