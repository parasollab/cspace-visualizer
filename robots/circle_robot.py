from robots.robot import Robot, DOF, DOFType
from environment.environment import Environment, Shape
import math

class CircleRobot2D(Robot):
    def __init__(self, radius):
        self.radius = radius
        dofs = [DOF('x', DOFType.POSITION), DOF('y', DOFType.POSITION)]
        super().__init__(f'Circle Robot with Radius {radius}', dofs)
    
    def is_valid(self, env, q) -> tuple[bool, Shape]:
        # Check if the circle robot is inside the environment
        x, y = q
        if x < env.boundary['x'][0] or x > env.boundary['x'][1]:
            return False, None
        if y < env.boundary['y'][0] or y > env.boundary['y'][1]:
            return False, None

        # Check if the circle robot is colliding with any obstacle
        for shape in env.shapes:
            if shape.shape == 'circle':
                dx = x - shape.location[0]
                dy = y - shape.location[1]
                if dx**2 + dy**2 <= (self.radius + shape.radius)**2:
                    return False, shape
            elif shape.shape == 'rectangle':
                if is_collision((x, y), self.radius, shape.location, shape.width, shape.height, shape.theta):
                    return False, shape
            else:
                raise NotImplementedError('Shape not implemented')
            
        return True, None

def is_collision(circle_center, circle_radius, rect_center, rect_width, rect_height, rect_angle):
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

    def point_in_circle(px, py, cx, cy, radius):
        return (px - cx) ** 2 + (py - cy) ** 2 <= radius ** 2

    def rect_corners(cx, cy, width, height, angle):
        angle_rad = math.radians(angle)
        half_width = width / 2
        half_height = height / 2

        corners = [
            (cx - half_width, cy - half_height),
            (cx + half_width, cy - half_height),
            (cx + half_width, cy + half_height),
            (cx - half_width, cy + half_height)
        ]

        rotated_corners = [rotate_point(x, y, cx, cy, angle_rad) for x, y in corners]
        return rotated_corners

    rect_corners = rect_corners(rect_center[0], rect_center[1], rect_width, rect_height, rect_angle)

    # Check if any of the rectangle's corners are inside the circle
    for corner in rect_corners:
        if point_in_circle(corner[0], corner[1], circle_center[0], circle_center[1], circle_radius):
            return True

    # Check if the circle's center is inside the rectangle
    def point_in_rotated_rect(px, py, cx, cy, width, height, angle):
        angle_rad = math.radians(-angle)
        translated_x, translated_y = rotate_point(px, py, cx, cy, angle_rad)
        half_width = width / 2
        half_height = height / 2
        return (cx - half_width <= translated_x <= cx + half_width and
                cy - half_height <= translated_y <= cy + half_height)

    if point_in_rotated_rect(circle_center[0], circle_center[1], rect_center[0], rect_center[1], rect_width, rect_height, rect_angle):
        return True

    # Check if any of the rectangle's edges intersect the circle
    def line_circle_intersection(x1, y1, x2, y2, cx, cy, radius):
        # Vector AB
        ABx = x2 - x1
        ABy = y2 - y1
        # Vector AC
        ACx = cx - x1
        ACy = cy - y1
        # Project vector AC onto AB, computing the projection scalar
        proj_scalar = (ACx * ABx + ACy * ABy) / (ABx ** 2 + ABy ** 2)
        # Find the closest point D on the line segment to the circle center
        closest_x = x1 + proj_scalar * ABx
        closest_y = y1 + proj_scalar * ABy
        if proj_scalar < 0:
            closest_x, closest_y = x1, y1
        elif proj_scalar > 1:
            closest_x, closest_y = x2, y2

        # Check if this closest point is within the circle's radius
        return point_in_circle(closest_x, closest_y, cx, cy, radius)

    for i in range(len(rect_corners)):
        x1, y1 = rect_corners[i]
        x2, y2 = rect_corners[(i + 1) % len(rect_corners)]
        if line_circle_intersection(x1, y1, x2, y2, circle_center[0], circle_center[1], circle_radius):
            return True

    return False
