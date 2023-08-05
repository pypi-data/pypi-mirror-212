from setuptools import setup

setup(
name='automate_pyspark_project_setup',
    version='1.0.0',
    description='Program to automate folder creation',
    author='Sagar Lakshmipathy',
    author_email='18vidhyasagar@email.com',
    py_modules=['pyspark_project_setup'],
    install_requires=[
        'requests',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'pyspark_project_setup=pyspark_project_setup:init',
        ],
    },
)
