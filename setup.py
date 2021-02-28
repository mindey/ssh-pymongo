from setuptools import find_packages, setup

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ssh-pymongo',
    version='1.0.4',
    description='Simple shortcut for PyMongo over ssh.',
    long_description=long_description,
    long_description_content_type='text/rst',
    url='https://github.com/mindey/ssh-pymongo',
    author='Mindey',
    author_email='~@mindey.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'pymongo',
        'sshtunnel',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
)
