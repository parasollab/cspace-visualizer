import sys
import matplotlib.pyplot as plt
from environment.environment import Environment
from robots import point_robot
from cspace.cspace import CSpace

def main():
    # Read the robot type and environment file from the command line
    if len(sys.argv) < 3:
        print('Usage: python main.py <robot_type> <environment_file> <optional_robot_configs>')
        sys.exit(1)

    robot_type = sys.argv[1]
    if robot_type == 'point':
        robot = point_robot.PointRobot2D()
    else:
        raise NotImplementedError('Robot type not implemented')

    environment_file = sys.argv[2]

    environment = Environment(environment_file)
    environment.load()

    cs = CSpace(robot, environment)

    fig, ax = plt.subplots(1, 2)
    fig.suptitle(robot.name)
    ax[0].set_title('Environment')
    environment.display(ax[0])
    ax[1].set_title('Configuration Space')
    cs.display(ax[1])
    plt.show()
  
if __name__ == '__main__':
    main()