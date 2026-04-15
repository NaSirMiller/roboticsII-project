from setuptools import setup
import os
from glob import glob

package_name = 'exit_detection'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'danger_exit_detection_node = exit_detection.danger_exit_detection:main',
            'safe_exit_detection_node = exit_detection.safe_exit_detection:main',
            'location_provider_node = exit_detection.location_provider:main',
        ],
    },
)