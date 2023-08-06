from setuptools import setup, find_packages

setup(
    name='deepchecks-installer',
    version='0.3',
    packages=find_packages(),
    package_data={'deepchecks_installer': ['deepchecks_installer/*.sh']},
    install_requires=[
        'argparse',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'deepchecks-installer=deepchecks_installer.cli:main',
        ],
    },
)
