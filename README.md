# Configuration Space Visualization Tool

> Last Updated May 19, 2024 by Courtney McBeth

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

The cspace visualizer can be run as shown below

```bash
python main.py <robot_type> <environment_file> <optional_robot_configs>
```

For example, to use a point robot in the `examples\example.yaml` environment

```bash
python main.py point examples\examples.yaml
```

## Adding A New Robot

All robots have their own file and class within the robots folder. All robot classes should inherit from the `Robot` base class in `robot.py`.

> TODO add example of implementation

## Adding A New Environment

Environments are specified in yaml files. Add new environments in the examples folder. Each environment file lists a boundary range for the environment and a list of shapes that make up the obstacles. See `examples\example.yaml`.

> TODO explain how to specify each shape
