# Hill Climbing Algorithm
This repository contains a Python implementation of the Hill Climbing Algorithm for optimizing the placement of hospitals 
in a given space to minimize the distance from houses to the nearest hospital.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Dependencies](#dependencies)
- [Author](#author)
- [License](#license)
- [Sources](#sources)


## Overview
The Hill Climbing Algorithm is a heuristic search algorithm used for mathematical optimization problems. 
It starts with an arbitrary solution to a problem and iteratively makes small changes to the solution, each time selecting the best neighboring solution. 
The process continues until no better neighboring solution can be found, indicating that a local optimum has been reached.

## Features
- **Space Initialization:** Initialize a space with a specified height, width, and number of hospitals.
- **House and Hospital Placement:** Add houses and randomly place hospitals in the space.
- **Cost Calculation:** Calculate the total cost based on the distance of each house from the nearest hospital.
- **Hill Climbing Optimization:** Optimize the placement of hospitals using the Hill Climbing Algorithm.
- **Image Output:** Generate images representing the space and the optimization progress.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/TanerYSLY/Hill_Climbing_Algorithm.git
    cd Hill_Climbing_Algorithm
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install pillow
    ```
    
## Usage

1. Create a space with the desired dimensions and number of hospitals:
    ```python
    from hill_climbing import Space
    s = Space(height=6, width=12, num_hospitals=2)
    ```

2. Add houses to the space:
   
    ```python
    import random

    for i in range(5):  # Adding 5 houses
        s.add_house(random.randrange(s.height), random.randrange(s.width))
    ```

3. Perform the hill climbing optimization and generate images:
    ```python
    hospitals = s.hill_climb(image_prefix="hospitals", log=True)
    ```

4.The images representing the optimization process will be saved with the specified prefix (hospitals in this case).

## Example
Here's an example of how to use the provided code:

```python
from hill_climbing import Space
import random

# Initialize the space
s = Space(height=6, width=12, num_hospitals=2)

# Add houses to the space
for i in range(5):
    s.add_house(random.randrange(s.height), random.randrange(s.width))

# Perform hill climbing optimization
hospitals = s.hill_climb(image_prefix="hospitals", log=True)
```

## Dependencies
- Python 3.x
- Pillow (Python Imaging Library)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Sources 
- https://www.youtube.com/watch?v=sBzpqLuSDyY

## Author
TanerYSLY

