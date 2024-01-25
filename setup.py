from setuptools import setup, find_packages



with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()


entry_points = {
    'console_scripts': [
        'wski=wieniawski.wieniawski:cli',
    ],
}

setup(
    name='wieniawski', 
    description='Experimental refactor of Mozart optical music recognition models.',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    author='NotJoeMartinez',
    url='https://github.com/NotJoeMartinez/wieniawski',
    packages=find_packages(),
    install_requires=dependencies,
    entry_points=entry_points,
    python_requires='>=3.8',
)