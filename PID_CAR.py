
from autocar import *

if __name__ == '__main__':

    run = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
            (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]

    env = ComputerCar(1, 1, PATH)
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

            if env.direc > 0:
                action = 1
            else:
                action = 0        

            # print('  obs: ' + str(observation))
            observation_, reward, done = env.step(action)

        if run != True:
            break

    pygame.quit()
