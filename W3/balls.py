__author__ = 'ciacicode'
import random
import pdb


class Ball(object):
    """
        ball object
    """
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color + " ball"

class Bucket(object):
    """
    bucket needed for ball drawing simulation
    """
    def __init__(self, num_balls, *args):
        """

        :param num_balls: integer representing the number of balls
        :param args: colors of the balls
        :return: initialises the bucket
        """

        if num_balls <= 0:
            raise ValueError("Total number of balls must be >0")
        else:
            self.num_balls = num_balls
            self.bucket = list()
            self.colors = args
            self.balls_per_color = num_balls/len(self.colors)

        for color in self.colors:
            for b in range(self.balls_per_color):
                ball = Ball(color)
                self.bucket.append(ball)


    def getTotalBalls(self):
        return self.num_balls


    def getBallsOfColor(self, color):
        ball_color_count = 0
        if color in self.colors:
            for item in self.bucket:
                if item.color == color:
                    ball_color_count +=1
            return ball_color_count
        else:
            raise ValueError("No " + str(color) + " balls in bucket")



    def drawBall(self):
        if len(self.bucket)<=0:
            #the bucket is empty, nothing to draw:
            return "Bucket is empty, nothing to draw"
        else:
            drawn_ball = random.choice(self.bucket)
            self.bucket.remove(drawn_ball)
            self.num_balls -=1
            return drawn_ball.color


    def __repr__(self):
        return str(self.bucket)



def drawing_without_replacement_sim(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns a float - the fraction of times 3
    balls of the same color were drawn in the first 3 draws.
    '''
    # Your code here
    successful_trial_results = 0.0
    for trial in range(numTrials):
        # Create Bucket object as specified
        b = Bucket(8, "red", "green")
        #create list to track colors
        colors_drawn = list()
        for draw in range(3):
            drawn_color = b.drawBall()
            colors_drawn.append(drawn_color)
        if len(set(colors_drawn))==1:
            #there is only one type of color
            successful_trial_results+=1.0

    return float(successful_trial_results)/float(numTrials)






