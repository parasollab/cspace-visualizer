from robots.robot import Robot, DOF, DOFType
from environment.environment import Environment, Shape

class PointRobot2D(Robot):
    def __init__(self):
        dofs = [DOF('x', DOFType.POSITION, None), DOF('y', DOFType.POSITION, None)]
        super().__init__('Point Robot', dofs)
    
    def is_valid(self, env, q) -> tuple[bool, Shape]:
        # Check if the point robot is inside the environment
        x, y = q
        if x < env.boundary['x'][0] or x > env.boundary['x'][1]:
            return False, None
        if y < env.boundary['y'][0] or y > env.boundary['y'][1]:
            return False, None

        # Check if the point robot is colliding with any obstacle
        for shape in env.shapes:
            if shape.shape == 'circle':
                dx = x - shape.location[0]
                dy = y - shape.location[1]
                if dx**2 + dy**2 <= shape.radius**2:
                    return False, shape
            else:
                raise NotImplementedError
            
        return True, None