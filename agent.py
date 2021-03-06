from gameobjects import GameObject
from move import Move, Direction


class Agent:

    board_height = 5
    direction = None
    utilities = []
    updatedutilities = []

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        global counter
        counter = 0
        for i in range(0,25):
            Agent.utilities.append(0)
        for i in range(0,25):
            Agent.updatedutilities.append(0)

    def getFood(board):
        global food
        for x in range(0,5):
            for y in range(0,5):
                if (board[x][y] == GameObject.FOOD):
                    food = (x,y)

    def validMove(x,y):
        return(x>=0 and x<Agent.board_height and y>=0 and y<Agent.board_height)

    def determineMove(direction, moveToMake, position):
        global move
        xy_man = (moveToMake[0] - position[0], moveToMake[1] - position[1])
        if (direction.get_new_direction(Move.RIGHT).get_xy_manipulation() == xy_man):
            move = Move.RIGHT
        elif (direction.get_new_direction(Move.LEFT).get_xy_manipulation() == xy_man):
            move = Move.LEFT
        elif (direction.get_new_direction(Move.STRAIGHT).get_xy_manipulation() == xy_man):
            move = Move.STRAIGHT

    def setNewDirection():
        Agent.direction = Agent.direction.get_new_direction(move)

    def bestMove(x,y,board):
        global best
        util = -100
        best = (0,0)
        for i in range(0, len(list_man)):
            new_x = x+list_man[i][0]
            new_y = y+list_man[i][1]
            if(Agent.validMove(new_x, new_y)):
                if not(board[x][y] == GameObject.WALL):
                    if(Agent.updatedutilities[Agent.board_height * new_x + new_y] > util):
                        best = (new_x, new_y)
                        util = Agent.updatedutilities[Agent.board_height * new_x + new_y]
    def updateBoard(board):
        gamma = 0.8
        reward = -0.04
        for x in range (0,5):
            for y in range (0,5):
                i = Agent.board_height * x + y
                #up (0,+1)
                if(Agent.validMove(x,y+1) == False):
                    up = Agent.utilities[i]
                    print("up not valid", up)
                elif(board[x][y+1] == GameObject.WALL):
                    up = -100
                    print(up)
                else:
                    up = Agent.utilities[Agent.board_height * x + y+1]
                    print("up valid", up)
                #down (0,-1)
                if(Agent.validMove(x,y-1) == False):
                    down = Agent.utilities[i]
                    print("down not valid", down)
                elif(board[x][y-1] == GameObject.WALL):
                    down = -100
                    print(down)
                else:
                    down = Agent.utilities[Agent.board_height * x + y-1]
                    print("down valid", down)
                #right(1,0)
                if(Agent.validMove(x+1,y) == False):
                    right = Agent.utilities[i]
                    print("right not valid", right)
                elif(board[x+1][y] == GameObject.WALL):
                    right = -100
                    print(right)
                else:
                    right = Agent.utilities[Agent.board_height * (x+1) + y]
                    print("right valid", right)
                #left(-1,0)
                if(Agent.validMove(x-1,y) == False):
                    left = Agent.utilities[i]
                    print("left not valid", left)
                elif(board[x-1][y] == GameObject.WALL):
                        up = -100
                else:
                    left = Agent.utilities[Agent.board_height * (x-1) + y]
                    print(" left valid", left)
                if(up >= down and up >= right and up >= left):
                    Agent.updatedutilities[i] = Agent.utilities[i] + reward + gamma * (0.8 * up + 0.1 * right + 0.1 * left)
                    print("up")
                elif(down >= up and down >= right and down >= left):
                    Agent.updatedutilities[i] = Agent.utilities[i] + reward + gamma * (0.8 * down + 0.1 * right + 0.1 * left)
                    print("down")
                elif(right >= up and right >= down and right >= left):
                    Agent.updatedutilities[i] = Agent.utilities[i] + reward + gamma * (0.8 * right + 0.1 * down + 0.1 * up)
                    print("right")
                else:
                    Agent.updatedutilities[i] = Agent.utilities[i] + reward + gamma * (0.8 * left + 0.1 * down + 0.1 * up)
                    print("left")
                print(i, "utility", Agent.updatedutilities[i])


    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        global reward, list_man, initial
        print(len(Agent.utilities))
        Agent.direction = direction
        initial = head_position
        Agent.getFood(board)
        Agent.updateBoard(board)
        Agent.utilities[Agent.board_height * food[0]+ food[1]] = 1
        Agent.updatedutilities[Agent.board_height * food[0]+ food[1]] = 1
        print("board", Agent.updatedutilities)
        list_man = Agent.direction.get_xy_moves()
        Agent.bestMove(initial[0],initial[1],board)
        Agent.determineMove(direction, best, initial)
        Agent.setNewDirection()
        for i in range (0,25):
            Agent.utilities[i] = Agent.updatedutilities[i]
        if(best == food):
            utilities = []
            updatedutilities = []
            for i in range(0,25):
                Agent.utilities.append(0)
            for i in range(0,25):
                Agent.updatedutilities.append(0)

        return move

        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)
        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return False

    def on_die(self, head_position, board, score, body_parts):



        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """
