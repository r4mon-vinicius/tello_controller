from setuptools import find_packages, setup

package_name = 'tello_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'opencv-python'],
    zip_safe=True,
    maintainer='ramon',
    maintainer_email='ramon.vinicius.eng@gmail.com',
    description='A simple ROS2 package for controller DJI Tello',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tello_cam = tello_controller.tello_cam:main',
            'webcam_node = tello_controller.webcam_node:main'
        ],
    },
)
