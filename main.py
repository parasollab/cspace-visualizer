import argparse
import matplotlib.pyplot as plt
from environment.environment import Environment
from robots import point_robot, circle_robot
from cspace.cspace import CSpace

def main():
    # Read the robot type and environment file from the command line
    parser = argparse.ArgumentParser(description='Create a configuration space for a robot')
    parser.add_argument('-r', '--robot_type', dest='robot_type', type=str, help='Type of robot (point or circle)')
    parser.add_argument('-e', '--environment_file', dest='environment_file', type=str, help='Path to the environment file')
    parser.add_argument('-d', '--resolution', dest='resolution', type=float, help='Resolution of the configuration space (default: 0.1)', default=0.1)

    args, remaining_argv = parser.parse_known_args()
    robot_type = args.robot_type
    if robot_type == 'point':
        # There are no additional configurations for the point robot
        robot = point_robot.PointRobot2D()
    elif robot_type == 'circle':
        # The circle robot requires the radius as an additional configuration
        parser.add_argument('-s', '--radius', dest='radius', type=float, help='Radius of the circle robot')
        radius = parser.parse_args().radius
        robot = circle_robot.CircleRobot2D(radius)
    else:
        raise NotImplementedError(f'Robot type {robot_type} not implemented')

    print('Loading environment...')
    environment_file = parser.parse_args().environment_file
    environment = Environment(environment_file)
    environment.load()

    # The configuration space is created using the robot and environment
    print('Creating configuration space...')
    cs = CSpace(robot, environment)

    # Display the environment and configuration space
    print('Displaying environment and computing configuration space...')
    fig, ax = plt.subplots(1, 2)
    fig.suptitle(robot.name)

    ax[0].set_title('Environment')
    environment.display(ax[0])

    ax[1].set_title('Configuration Space')
    cs.display(ax[1], resolution=args.resolution)

    plt.tight_layout()
    plt.show()
  
if __name__ == '__main__':
    main()