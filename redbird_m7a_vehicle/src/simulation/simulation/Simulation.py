from Sim_Timer import Sim_Timer
from Target_Robot import Target_Robot
from Obstacle_Robot import Obstacle_Robot
from time import sleep
from threading import Thread
from Ground_RobotInterface import iterations
from math import sqrt, pow, tan

class Simulation(object):
    """description of class"""

    def __init__(self):
        self._timer = Sim_Timer()

        #creating the main array of both the ground and obstacle robots with arbitrary values 
        self.Rtarget_robots = []
        self.Gtarget_robots = []
        self.Wobstacle_robots = []

        #Filling the target robot array with arbitrary values
        for robot in range(1, 5):
            self.Rtarget_robots.append(Target_Robot(0, 0))

        #Filling the obstacle robot array 
        for robot in range(11, 15):
            self.obstacle_robots.append(Obstacle_Robot(0, 0, 0, 0, robot, 0, self._timer))

    def run(self):
        #Running the timer (controls all threads) 
        self._timer.run()

        #Runs all threads in the target robot array
        for arduino in self.target_robots:
            print 'initing all of the ground robots'
            arduino.run(self.obstacle_robots)

        #Runs all threads in the obstacle robot array
        for robot in self.obstacle_robots:
            print 'initing the obstacle robots'
            robot.run()

        self.threading()

        sleep(1200)

        self._timer.quit()

    def get_Target_robots(self):
        return self.target_robots

    def get_Obstacle_Robots(self):
        return self.obstacle_robots

    def check_collision(self):
        #Only allowing for the PAUSED flag to be false
        while not self._timer._PAUSED.is_set():

            min_num = 0
            max_num = len(self.target_robots)

            while min_num < max_num :

                #looping through the array that is being input to the function
                for robot in range(1, max_num):

                    #as long as the two id are not equal
                    if not (self.target_robots[min_num]._id == self.target_robots[robot]._id):

                        #as long as the boundary flag is raised
                        if(self.target_robots[min_num]._boundary):

                            #stopping and deleting the thread
                            self.target_robots[min_num]._distanceThread._stop()

                            self.target_robots[min_num]._distanceThread._delete()

                            break
                        #testing the if the robot has exited the boundary
                        elif(self.target_robots[min_num]._x >= 10 and self.target_robots[min_num]._y >= 10):
                            self.target_robots[min_num]._boundary = True

                        else:
                            #Determining the distance from robot to robot
                            dXX =  - self.target_robots[robot]._x - self.target_robots[min_num]._x
                            dYY = self.target_robots[robot]._y - self.target_robots[min_num]._y

                            dCC = sqrt((pow(dXX, 2) + pow(dYY, 2)))

                            max_distance = sqrt(self.target_robots[min_num] + self.target_robots[robot])

                            #if the distance from center to center is less than the sum of the two radii
                            if dCC <= max_distance:

                                self.button_pushed(self.target_robots[min_num], self.target_robots[robot])

                min_num += 1

                sleep(iterations/2)

    def threading(self):
        #starting and initializing the thread

        self._collision_thread = Thread(target = self.check_collision)

        try:
            self._collision_thread.start()

            print 'Thread started'

        except:
            print 'Thread not started'

    def button_pushed(self, robot, robot1):
        #arbitrary definition of the two inputs
        robot = Target_Robot
        robot1 = Target_Robot

        #finding the distance vectors between each of the robots
        vector_i = robot._x - robot1._x
        vector_j = robot._y - robot1._y

        if (vector_i == 0):
            theta = 90
        else:
            theta = tan(vector_j / vector_i)

        #Calculating the angle of velocity vector and bounds checking
        if(robot._deltaX == 0):

            if(robot._deltaY < 0):
                v_theta = 180

            v_theta = 90

        else:
            v_theta = tan(robot._deltaY / robot._deltaX)

        #Finding the relative angle of where the button is pushed
        min_theta = robot.get_theta() - 70
        max_theta = robot.get_theta() + 70

        #Calculating the angle of velocity vector with respect to the other robot
        #this is necessary because now the Simulation is doing collision detection

        min2_theta = robot1.get_theta() - 70
        max2_theta = robot1.get_theta() + 70

        if(theta >= min_theta and theta <= max_theta):
            robot.collision = True

        if(theta >= min2_theta and theta <= max2_theta):
            robot1.collision = True