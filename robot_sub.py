from robot import *
import random

nb_robots = 0

class Robot_player(Robot):
    team_name = "Challenger"
    robot_id = -1
    memory = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        self.memory += 1

        front = sensors[sensor_front]
        threshold = 0.25  # ön engel algılama mesafesi

        # Ön kapalıysa → tam dönüş yap
        if front < threshold:
            translation = 0.1  # çarpmamak için yavaş
            rotation = 1.0     # maksimum dönüş → 180 derece
            return translation, rotation, False

        # Ön açık → düz ve hızlı ilerle
        translation = 1.0
        rotation = 0.0
        return translation, rotation, False
