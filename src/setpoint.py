#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:

    def __init__(self):
        #create a node, give it a name and anonymous = True ensures that your 
        #node has a unique name by adding random numbers to the end of NAME
        rospy.init_node('tortuguita', anonymous=True)
        #create a publisher to give informations of velocity on the topic cmd_vel
        #and a subscriber to update the pose when the topic messages it.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        self.pose = Pose()

        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        #The euclidean distance is the lenght of a straigh line segment that 
        # connects two points. The value is given by the equation:
        # squareroot((q1-p1)^2+(q2-p2)^2+(q3-p3)^2+...+(qn-pn)^2)
        # with the two points 'p' and 'q' are defined for:
        # p = (p1,p2,p3,...,pn) and q = (q1,q2,q3,...,qn)
        # for the turtle example, we will consider that we only have two 
        # coordenates for each point.
        eucl=sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
        return eucl

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        while(True):
            #Moves to the goal by importing from the turtlesim package
            goal_pose = Pose()
        

            # Get the input from the user.
            goal_pose.x = input("X goal: ")
            goal_pose.y = input("Y goal: ")

            #For the challenge, the tolerance is always 0.1.
            distance_tolerance=0.1

            #importing Twist package
            vel_msg = Twist()

            while self.euclidean_distance(goal_pose) >= distance_tolerance:
             # geometry_msgs/Twist has two vectors of three floating point elements
             # each: Linear and angular. For this example, it can be moved foward 
             # using the x-linear value and the rotational maneuvers using the 
             # z-angular.
             # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()

            # Stopping our robot after the movement is over.
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()
        


if __name__ == '__main__':
        x = TurtleBot()
        x.move2goal()