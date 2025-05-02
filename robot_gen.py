from robot import *
import random
import math

nb_robots = 0
debug = False  # debug çıktısını görmek istersen True yap

class Robot_player(Robot):
    team_name = "Gen"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

        # Genetik algoritma parametreleri
        self.param = [random.uniform(-2, 2) for _ in range(8)]  # 8 ağırlık
        self.it_per_evaluation = 400  # her 400 adımda yeni parametre
        self.iteration = 0
        self.trial = 0

        self.x_0 = x_0
        self.y_0 = y_0
        self.log_sum_of_translation = 0.0
        self.log_sum_of_rotation = 0.0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        self.iteration += 1

        # Her it_per_evaluation adımda bir yeni strateji dener
        if self.iteration % self.it_per_evaluation == 0:
            if self.iteration > 0:
                print("Trial", self.trial, "→", self.param)
                print("→ Movement Score =", self.log_sum_of_translation)
                print("→ Distance from origin =", math.sqrt((self.x - self.x_0)**2 + (self.y - self.y_0)**2))
            
            # Yeni rastgele parametre seti oluştur
            self.param = [random.uniform(-2, 2) for _ in range(8)]
            self.trial += 1
            self.log_sum_of_translation = 0.0
            self.log_sum_of_rotation = 0.0
            return 0, 0, True  # reset sinyali

        # Braitenberg tipi ağırlıklı kontrol (tanh ile yumuşatılmış)
        s1 = sensors[sensor_front_left]
        s2 = sensors[sensor_front]
        s3 = sensors[sensor_front_right]

        translation = math.tanh(self.param[0] + self.param[1]*s1 + self.param[2]*s2 + self.param[3]*s3)
        rotation = math.tanh(self.param[4] + self.param[5]*s1 + self.param[6]*s2 + self.param[7]*s3)

        # Hareket kaydı (performans ölçümü için)
        self.log_sum_of_translation += abs(translation)
        self.log_sum_of_rotation += abs(rotation)

        return translation, rotation, False
