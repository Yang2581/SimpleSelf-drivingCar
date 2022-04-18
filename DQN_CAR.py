
from autocar import *
from DQN import Agent
import torch

if __name__ == '__main__':

    run = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
            (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]

    env = ComputerCar(1, 1, PATH)
    combined = False
    buffer_size = 50000

    # TODO: fine tune the parameters
    # -------------------------------
    # gamma: discount factor
    # epsilon: random exploration
    # batch_size:
    # n_actions: number of action space
    # input_dims: number of state space
    # lr: learning rate
    # max_mem_size: size of replay buffer

    agent = Agent(gamma=0.95, epsilon=0.10, batch_size=100, n_actions=2,
                  eps_end=0.1, input_dims=3, lr=0.001,
                  max_mem_size=buffer_size, combined=combined)

    # TODO:load the agent network weights
    #################################
    # agent.Q_eval.load_state_dict(torch.load('weight_eval.pt'))
    # agent.Q_next.load_state_dict(torch.load('weight_next.pt'))
    #################################

    scores = []
    n_games = 1000
    run = True
    for i in range(n_games):
        score = 0
        idx = 0
        done = False
        observation = env.reset()

        '''
        observation
        1. beta: sideslip angle (the angle between heading angle of the car and the center line)
        2. deviation: deviation between car and center line
        3. direction: check the car's direction from the center line(1 for left and -1 right) 
        '''

        while not done:
            clock.tick(FPS)
            draw(WIN, images, env)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if run != True:
                break        
            action = agent.choose_action(observation)
            # print('  obs: ' + str(observation))
            observation_, reward, done = env.step(action)
            score += reward
            agent.memory.store_transition(observation, action, reward,
                                          observation_, done)

            observation = observation_
            if idx % 100 == 0:
                agent.learn()
            idx += 1
            # print(observation)

        print('episodes: ' + str(i) + '------score: ' + str(score))
        if i > 100:
            pass
            # TODO: save the trained network weights
            ######################################
            # torch.save(agent.Q_eval.state_dict(), 'weight_eval.pt')
            # torch.save(agent.Q_next.state_dict(), 'weight_next.pt')
            # agent.memory.save_buffer('buffer')
            ######################################
        if run != True:
            break
        # scores.append(score)

        # avg_score = np.mean(scores[-100:])

    pygame.quit()
