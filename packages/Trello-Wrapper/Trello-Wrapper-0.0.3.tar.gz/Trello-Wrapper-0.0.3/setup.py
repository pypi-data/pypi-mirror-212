from setuptools import setup, find_packages
with open("README2.md", "r") as f:
    long_description = f.read()

setup(
    name='Trello-Wrapper',
    version='0.0.3',
    author='Rtsil',
    author_email='rtsilavotahina@gmail.com',
    description='A Python Wrapper around the Trello API',
    long_description=long_description,
    url='https://github.com/Rtsil/Trello-Wrapper',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords=['trello', 'wrapper', 'api'],
    install_requires=[
        "requests"
    ]

)

