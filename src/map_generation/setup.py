from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'map_generation'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tong Wang',
    maintainer_email='wangt17@rpi.edu',
    description='Autonomous map generation using SLAM, Nav2, and nav2_wfd',
    license='MIT',
    entry_points={
        'console_scripts': [
            'map_generation_node = map_generation.map_generation_node:main',
        ],
    },
)
