from robots.robot import Robot, DOF, DOFType
from environment.environment import Environment, Shape
import math

class PointRobot2D(Robot):
    def __init__(self):
        dofs = [DOF('x', DOFType.POSITION), DOF('y', DOFType.POSITION)]
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
            elif shape.shape == 'rectangle':
                if is_point_in_rotated_rect((x, y), shape.location, shape.width, shape.height, shape.theta):
                    return False, shape
            else:
                raise NotImplementedError('Shape not implemented')
            
        return True, None
    
def is_point_in_rotated_rect(point, rect_center, rect_width, rect_height, rect_angle):
    def rotate_point(px, py, cx, cy, angle):
        # Translate point to origin
        temp_x = px - cx
        temp_y = py - cy

        # Rotate point
        rotated_x = temp_x * math.cos(angle) - temp_y * math.sin(angle)
        rotated_y = temp_x * math.sin(angle) + temp_y * math.cos(angle)

        # Translate point back
        px = rotated_x + cx
        py = rotated_y + cy
        return px, py

    def point_in_rotated_rect(px, py, cx, cy, width, height, angle):
        angle_rad = math.radians(-angle)
        translated_x, translated_y = rotate_point(px, py, cx, cy, angle_rad)
        half_width = width / 2
        half_height = height / 2
        return (cx - half_width <= translated_x <= cx + half_width and
                cy - half_height <= translated_y <= cy + half_height)

    return point_in_rotated_rect(point[0], point[1], rect_center[0], rect_center[1], rect_width, rect_height, rect_angle)
