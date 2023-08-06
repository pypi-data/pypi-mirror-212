# This file is part of pyRDDLGym.

# pyRDDLGym is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published by
# the Free Software Foundation.

# pyRDDLGym is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with pyRDDLGym. If not, see <https://opensource.org/licenses/MIT>.

from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
      name='pyRDDLGym',
      version='1.0.56',
      author="Ayal Taitler, Michael Gimelfarb, Scott Sanner, Jihwan Jeong, Sriram Gopalakrishnan, Martin Mladenov, jack liu",
      author_email="ataitler@gmail.com, mike.gimelfarb@mail.utoronto.ca, ssanner@mie.utoronto.ca, jhjeong@mie.utoronto.ca, sriram.gopalakrishnan@jpmchase.com, mmladenov@google.com, xiaotian.liu@mail.utoronto.ca",
      description="pyRDDLGym: RDDL automatic generation tool for OpenAI Gym",
      # long_description=long_description,
      license="MIT License",
      url="https://github.com/ataitler/pyRDDLGym",
      packages=find_packages(),
      install_requires=['ply', 'pillow>=9.2.0', 'matplotlib>=3.5.0', 'numpy>=1.22', 'gym>=0.24.0', 'pygame'],
      python_requires=">=3.8",
      include_package_data=True,
      # package_data={'': ['Examples/CartPole/Continuous/*.rddl',
      #                    'Examples/CartPole/Discrete/*.rddl',
      #                    'Examples/Elevator/*.rddl',
      #                    'Examples/Mars_rover/*.rddl',
      #                    'Examples/MountainCar/*.rddl',
      #                    'Examples/Power_gen/*.rddl',
      #                    'Examples/Racecar/*.rddl',
      #                    'Examples/Recsim/*.rddl',
      #                    'Examples/UAV/Continuous/*.rddl',
      #                    'Examples/UAV/Discrete/*.rddl',
      #                    'Examples/UAV/Mixed/*.rddl',
      #                    'Examples/Wildfire/*.rddl',
      #                    'Examples/Supply_Chain/*.rddl',
      #                    'Examples/Traffic/*.rddl',
      #                    'Examples/PropDBN/*.rddl',
      #                    'Examples/WildlifePreserve/*.rddl',
      #                    ]},
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
