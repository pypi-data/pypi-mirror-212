from setuptools import setup

from argeasy import __version__

with open('README.md', 'r') as reader:
    readme = reader.read()

setup(
    name='argeasy',
    version=__version__,
    description='ArgEasy: Create amazing CLI programs.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jaedson Silva',
    author_email='jaedson.dev@proton.me',
    packages=['argeasy'],
    url='https://github.com/jaedsonpys/argeasy',
    project_urls={
        'License': 'https://github.com/jaedsonpys/argeasy/blob/master/LICENSE'
    },
    keywords=['cli', 'command', 'argument', 'parser', 'command-line', 'interface'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
