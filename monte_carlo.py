from game import Game
import numpy as np

value_map = {0:0, 2:1, 4:2, 8:3, 16:4, 32:5, 64: 6}
size = 3
moves = ['a','s','d','w']
epsilon = 0.5
end_number = 32

def generate_episode(Q, show = False):
    game = Game(end_number=end_number, size = size)
    states_visited = []
    actions_taken = []
    while not game.is_over():
        if show:
            game.print_board()
        state = map_board_to_int(game.get_board())
        if np.random.random() < epsilon:
            move = np.random.randint(0, len(moves))
        else:
            move  = np.argmax(Q[state])
        if show:
            print(moves[move])
        game.play(moves[move])
        #only count if the state was actually changed
        next_state = map_board_to_int(game.get_board())
        if next_state != state:
            states_visited.append(state)
            actions_taken.append(move)
    if show:
        game.print_board()
    if game.is_won():
        G = 1
    else:
        G = 0
    
    return (states_visited, actions_taken, G)

def play_optimally(Q, iters = 10, show = False):
    wins = 0
    loses = 0
    timeouts = 0
    steps = 0
    for i in range(iters):
        game = Game(end_number=end_number, size=size)
        move_num = 0
        while not game.is_over():
            if move_num > 1000:
                timeouts += 1
                break
            if show:
                game.print_board()
            move_num += 1
            state = map_board_to_int(game.get_board())
            move = np.argmax(Q[state])
            if show:
                print(moves[move])
            game.play(moves[move])
        if game.is_won():
            wins += 1
        if game.is_lost():
            loses += 1
        steps += move_num
    return (wins, loses, timeouts, float(steps)/iters)

def map_board_to_int(state):
    res = 0
    for i in range(len(state)):
        for j in range(len(state)):
            res += value_map[state[i,j]] * len(value_map)  ** ( (i*len(state) + j))
    return res

if __name__ == "__main__":

    #initialise tables
    state_space_size = len(value_map) ** (size * size)
    print("State space size: {}".format(state_space_size))
    Q = np.array([[0.0 for j in range(4)] for i in range(state_space_size)])
    visits = np.array([0 for j in range(state_space_size)])

    iters = 0
    last_episodes = []
    average_wins = 0
    show = False
    while True:
        iters += 1
        #play for an entire episode
        (states, actions, G) = generate_episode(Q, show = show)

        #remember last 1000  results to compute average
        last_episodes.insert(0,G)
        if len(last_episodes) > 1000:
            last_episodes.pop()
        
        #update expected values using monte-carlo, etimating the true mean
        for state, action in zip(states, actions):
            visits[state] += 1
            Q[state, action]  +=  ((G - Q[state, action]) / visits[state])

        #Compute and display metrics
        average_wins += (float(G) - average_wins)/float(iters)
        if iters % 1000 == 0:
            print(iters)
            print("Average wins/last 1000 episodes: {:.2f}/{}".format( average_wins, sum(last_episodes)/len(last_episodes)))
            print("Visits max/min/avg: {}/{}/{}".format(np.max(visits), np.min(visits), np.average(visits)))
            print("Play optimally (wins, loses, timeouts, steps/game): {}".format(play_optimally(Q)))
