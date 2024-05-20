# Configuration Space Visualization Tool

> Last Updated May 19, 2024 by Courtney McBeth

**Read this entire README before working with the code!**

## Usage

Recommended: Create and activate a virual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

After you are finished working with the visualizer, you can deactivate the virtual environment by typing `deactivate` in the terminal.

Install dependencies

```bash
pip install -r requirements.txt
```

The cspace visualizer can be run as shown below (see `main.py` for config options).

```bash
python main.py -r <robot_type> -e <environment_file> <optional_configs>
```

For example, to use a circle robot with radius 2.0 in the `examples/example.yaml` environment

```bash
python main.py -r circle -e examples/example.yaml --radius 2 --resolution 0.1
```

## Adding a New Robot

All robots have their own file and class within the robots folder. All robot classes should inherit from the `Robot` base class in `robot.py`. See `circle_robot.py` for an example.

Any additional information needed to define the robot geometry can be read from the command line arguments using argparse (see `main.py`). For example, for the circle robot, the radius is read from the command line arguments (`--radius x`) or defaults to 1 if none is provided.

When initializing the robot object, a list of degrees of freedom (dofs) should be provided to the superclass. For a mobile robot, these will have the type `DOFType.POSITION` and `DOFType.ORIENTATION` if body rotation in the environment matters. For fixed base, manipulators, these will have type `DOFType.ROTATION`. In the circle robot example, orientation is omitted since the rotation of the circle about its center does not change the cspace. For positional degrees of freedom, the range can be omitted and will be gotten from the environment bounds. For orientation and positional degrees of freedom a range should be specified in radians (e.g. [-pi, pi]).

When implementing a new robot class, the bulk of the work will be implementing the `is_valid` function. This takes in an `Environment` object and a configuration, `q`, which is a list of degree of freedom values. Iterate through all shapes in the environment and for each circle and rectangle determine whether your robot's geometry is in collision with the obstacle. Note that for more complex robot geometries, this may be slow, that is expected.

## Adding a New Environment

Environments are specified in yaml files. Add new environments in the examples folder. Each environment file lists a boundary range for the environment and a list of shapes that make up the obstacles. All environments are two dimensional. See `examples/example.yaml`.

The supported shapes are circles and rectangles. Files follow the format shown in the example below. All named matplotlib colors are supported.

```yaml
boundary:
  x: [-10, 10] # [min, max]
  y: [-10, 10] # [min, max]
obstacles:
  - shape: circle
    location: [0, 0] # center
    radius: 1
    color: lightseagreen
  - shape: circle
    location: [2, 0]
    radius: 2
    color: coral
  - shape: rectangle
    location: [-3, 5] # center
    width: 2
    height: 1
    theta: 45 # degrees, rotated about center
    color: blueviolet
```

## How to Merge Code

**IMPORTANT:** Make your changes on a new branch (not main).

When you're ready, make a pull request to merge your branch into main. This will request a code review from a code owner. They may request changes or merge the code.

## Remaining Robots

- Rectangle with parameterizable length and width
- Equilateral triangle with parameterizable side length
- 2 link manipulator
- 3 link manipulator
- mobile 1 link manipulator
- Elliptical robot with parameterizable radii
