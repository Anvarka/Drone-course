from gym_duckietown.tasks.task_solution import TaskSolution
import numpy as np
import cv2


class DontCrushDuckieTaskSolution(TaskSolution):
    def __init__(self, generated_task):
        super().__init__(generated_task)
        self.env = self.generated_task['env']
        self.lower_yellow = np.array([20,  100, 100])
        self.upper_yellow = np.array([30, 255, 255])

    def solve(self):
        # getting the initial picture
        img, _, _, _ = self.env.step([0, 0])

        condition = True
        while condition:
            img, reward, done, info = self.env.step([1, 0])
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

            condition = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow).sum() < 3e6
            self.env.render()
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        # поворачиваем
        count = self.turn(1, hsv)
        # перестраиваемся
        self.move(7)
        # выпрямляемся на встречке
        self.turn_only(count + 1, -1)
        # едем по встречке
        self.move(7)
        # возвращаемся
        self.turn_only(count + 1, -1)
        self.move(7)
        # едем по своей полосе
        self.turn_only(count + 1, 1)
        self.move(10)

    def move(self, _steps):
        for _ in range(_steps):
            self.env.step([0.5, 0])
            self.env.render()

    # def move_with_check_yellow_right(self, hsv):
    #     self.move(5)
    #     while cv2.inRange(hsv, self.lower_yellow, self.upper_yellow).sum() >= 2e6:
    #         self.move(5)

    def turn(self, angle, hsv):
        count = 0
        while cv2.inRange(hsv, self.lower_yellow, self.upper_yellow).sum() >= 2e6:
            img, _, _, _ = self.env.step([0.2, angle])
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            self.env.render()
            count += 1
        self.env.step([0.2, angle])
        self.env.render()
        return count

    def turn_only(self, steps, angle):
        for _ in range(steps):
            img, _, _, _ = self.env.step([0.2, angle])
            self.env.render()

