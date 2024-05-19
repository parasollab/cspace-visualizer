from robots.robot import Robot
from environment.environment import Environment

class CSpace:
    def __init__(self, robot : Robot, environment : Environment):
        self.robot = robot
        self.environment = environment

    def display(self, ax, resolution : float = 0.1):
        assert len(self.robot.dofs) <= 2, "Only 2D or 3D robots are supported"

        if len(self.robot.dofs) == 2:
            x_min, x_max = self.robot.dofs[0].range if self.robot.dofs[0].range is not None else self.environment.boundary['x']
            y_min, y_max = self.robot.dofs[1].range if self.robot.dofs[1].range is not None else self.environment.boundary['y']
            x = x_min
            while x <= x_max:
                y = y_min
                while y <= y_max:
                    valid, shape = self.robot.is_valid(self.environment, [x, y])
                    if not valid:
                        ax.plot(x, y, '.', color=shape.color)
                    y += resolution
                x += resolution
        else:
            raise NotImplementedError("3D robots are not supported yet")
        
        ax.axis([x_min, x_max, y_min, y_max])
        ax.set_aspect('equal', adjustable='box')