from setuptools import find_packages, setup

package_name = 'turtlesim_pde4430_faseeh'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='faseeh',
    maintainer_email='faseeh@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gostr = turtlesim_pde4430_faseeh.straight_line:main' ,
            'gocircle = turtlesim_pde4430_faseeh.circle:main' ,
            'go8 = turtlesim_pde4430_faseeh.eight:main' ,
            'goroomba = turtlesim_pde4430_faseeh.roomba:main' ,
            'roomba4x = turtlesim_pde4430_faseeh.roomba4x:main' ,
            'user_go = turtlesim_pde4430_faseeh.user_input_move:main' ,
            'go_goal = turtlesim_pde4430_faseeh.go_goal:main',
        ],
    },
)
