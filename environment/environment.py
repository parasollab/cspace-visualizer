import matplotlib.pyplot as plt
import yaml

"""
An environment is a boundary and a collection of obstacles within the boundary.
An obstacle is given by a shape and a location.
TODO the only shapes supported now are circles, add more shapes.
"""
class Shape:
    def __init__(self, shape : str, location : tuple, color : str = 'r'):
        self.shape = shape
        self.location = location
        self.color = color

    def display(self):
        raise NotImplementedError
    
class Circle(Shape):
    def __init__(self, location : tuple, color : str, radius : float):
        super().__init__('circle', location, color)
        self.radius = radius

    def display(self, ax):
        circle = plt.Circle(self.location, self.radius, color=self.color, fill=True)
        ax.add_artist(circle)

class Environment:
    def __init__(self, filename):
        self.filename = filename
        self.shapes = []
        self.boundary = None

    def load(self):
        with open(self.filename, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            self.boundary = data['boundary']
            for shape in data['obstacles']:
                if shape['shape'] == 'circle':
                    self.shapes.append(Circle(shape['location'], shape['color'], shape['radius']))
                else:
                    raise NotImplementedError
    
    def display(self, ax):
        # TODO add support for 3D environments
        ax.axis([self.boundary['x'][0], self.boundary['x'][1], self.boundary['y'][0], self.boundary['y'][1]])
        ax.set_aspect('equal', adjustable='box')
        for shape in self.shapes:
            shape.display(ax)
