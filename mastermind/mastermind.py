from game import Game, Player
from cpu import DonaldKnuth

def human_vs_human():
    Game(codemaker=Player("Player One"), codebreaker=Player("Player Two")).run()
    
def human_vs_cpu():
    human = Player("Human")
    cpu = DonaldKnuth()
    Game(codemaker=human, codebreaker=cpu).run()

if __name__ == "__main__":
    # TODO signal handling.
    # todo human vs human // human vs cpu selection
    #human_vs_human
    human_vs_cpu()
