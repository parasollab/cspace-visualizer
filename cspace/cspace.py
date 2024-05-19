from robots.robot import Robot
from environment.environment import Environment
import numpy as np
from tqdm import tqdm

class CSpace:
    def __init__(self, robot : Robot, environment : Environment):
        self.robot = robot
        self.environment = environment

    def display(self, ax, resolution : float = 0.1):
        assert len(self.robot.dofs) <= 3, "Only 2D or 3D cspaces are supported"

        if len(self.robot.dofs) == 2:
            x_min, x_max = self.robot.dofs[0].range if self.robot.dofs[0].range is not None else self.environment.boundary['x']
            y_min, y_max = self.robot.dofs[1].range if self.robot.dofs[1].range is not None else self.environment.boundary['y']

            for x in tqdm(np.arange(x_min, x_max, resolution)):
                for y in np.arange(y_min, y_max, resolution):
                    valid, shape = self.robot.is_valid(self.environment, [x, y])
                    if not valid:
                        ax.plot(x, y, '.', color=shape.color)

            ax.set_xlabel(self.robot.dofs[0].name)
            ax.set_ylabel(self.robot.dofs[1].name)

            ax.axis([x_min, x_max, y_min, y_max])
            ax.set_aspect('equal', adjustable='box')
        else:
            x_min, x_max = self.robot.dofs[0].range if self.robot.dofs[0].range is not None else self.environment.boundary['x']
            y_min, y_max = self.robot.dofs[1].range if self.robot.dofs[1].range is not None else self.environment.boundary['y']
            z_min, z_max = self.robot.dofs[2].range

            for x in tqdm(np.arange(x_min, x_max, resolution)):
                for y in np.arange(y_min, y_max, resolution):
                    for z in np.arange(z_min, z_max, resolution):
                        valid, shape = self.robot.is_valid(self.environment, [x, y, z])
                        if not valid:
                            ax.plot(x, y, z, '.', color=shape.color)
            
            ax.set_xlabel(self.robot.dofs[0].name)
            ax.set_ylabel(self.robot.dofs[1].name)
            ax.set_zlabel(self.robot.dofs[2].name)
        