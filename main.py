from stages.intro import Intro
from stages.battle import Battle
#from stages.ship_location import ShipLocation
#from stages.podium import Podium


class GameState():
    def __init__(self) -> None:
        self.client = None
        self.state = 'intro'
        self.intro_stage = None
        # self.ship_location_stage: ShipLocation = None
        # self.battle_stage: Battle = None
        # self.podium_stage: Podium = Podium()
        self.battle_stage = None
        self.window_thread = None

    def intro(self) -> None:
       
        self.intro_stage = Intro()
        self.intro_stage.show_window()


    def battle(self) -> None:
        """ Battle stage state handler. """
        if not self.battle_stage:
            self.battle_stage = Battle(self.client)

    def state_manager(self) -> None:
        """ This function keeps tracking of current game state. """

        if self.state == 'intro':
            self.intro()            
        # elif self.state == 'ship_location':
        #     self.ship_location()
        # elif self.state == 'battle':
        #     self.battle()
        # elif self.state == 'podium':
        #     self.podium()
        elif self.state == 'battle':
            self.battle()

def main():
    game_state = GameState()
    game_state.intro()
    
if __name__ == '__main__':
    main()