from setuptools import find_packages, setup

package_name = 'python_pack'

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
    maintainer='moaz',
    maintainer_email='moazforfire@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "node1 = python_pack.node1:main",
            "go_to_goal_node = python_pack.GoToGoalNode:main",
        ],
    },
)
