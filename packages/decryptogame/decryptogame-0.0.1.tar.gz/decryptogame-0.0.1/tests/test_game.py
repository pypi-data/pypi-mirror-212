import pytest
from decryptogame.game import Game

class TestGame:
    def test_default(self):
        words = (
            ("black", "dragonfly", "cocktail", "sombrero"),
            ("antiquity", "bone", "morning", "nightmare")
        )
        game = Game(words=words)

        assert game.words == words

        assert game.miscommunications[0] == 0
        assert game.miscommunications[1] == 0

        assert game.interceptions[0] == 0
        assert game.interceptions[1] == 0

        assert game.winner is None
        assert game.rounds_played == 0        


    def test_kw_only(self):
        with pytest.raises(TypeError):
            game = Game(0)
    
    def test_configurable(self):
        words = [
            ("black", "dragonfly", "cocktail", "sombrero"),
            ("antiquity", "bone", "morning", "nightmare")
        ]
        game = Game(words=words, miscommunications=[1,2], interceptions=[3,4])
        assert game.miscommunications[0] == 1
        assert game.miscommunications[1] == 2
        assert game.interceptions[0] == 3
        assert game.interceptions[1] == 4