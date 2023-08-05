
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="json-to-github-actions",
    version="1.1.0",
    packages=find_packages(),
    py_modules=['json_to_github_actions'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'json_to_github_actions = json_to_github_actions:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
