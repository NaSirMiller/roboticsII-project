from setuptools import setup
import os
from glob import glob

package_name = 'yahboomcar_nav'

setup(
    name=package_name,
    version='0.1.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tong Wang',
    maintainer_email='wangt17@rpi.edu',
    description='Yahboom ROSMASTER X3 bringup and LiDAR launch files',
    license='MIT',
    entry_points={
        'console_scripts': [],
    },
)
