from robot import *
import random

nb_robots = 0

class Robot_player(Robot):
    team_name = "Challenger"
    robot_id = -1
    memory = 0  # sadece sayaç

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        self.memory += 1

        wall_left = 1.0 - sensors[sensor_front_left]
        wall_right = 1.0 - sensors[sensor_front_right]
        wall_front = 1.0 - sensors[sensor_front]

        is_friend = [1.0 * (sensor_view[i] == 2 and sensor_team[i] == self.team_name) for i in range(8)]

        # Translation: öndeki engelden dolayı hafif yavaşla ama durma
        translation = 0.9 - 0.5 * wall_front
        translation = max(0.3, translation)

        # Rotation: daha agresif tepkiyle dön
        rotation = 0.0

        # Duvar etkisi (erken kaçış, ama artık çarpan büyük)
        rotation += (wall_right - wall_left) * (1.5 + 1.5 * wall_front)

        # Takım arkadaşı etkisi
        rotation += is_friend[sensor_right] * 1.2
        rotation += is_friend[sensor_front_right] * 0.8
        rotation -= is_friend[sensor_left] * 1.2
        rotation -= is_friend[sensor_front_left] * 0.8

        # Rastgelelik — ön sinyal yüksekse (duvara çok yakınsa), daha fazla sapma ekle
        noise_amplitude = 0.1 + 0.5 * wall_front  # duvara ne kadar yakınsa, o kadar yüksek
        rotation += (random.random() - 0.5) * noise_amplitude

        translation = max(min(translation, 1.0), -1.0)
        rotation = max(min(rotation, 1.0), -1.0)

        return translation, rotation, False
