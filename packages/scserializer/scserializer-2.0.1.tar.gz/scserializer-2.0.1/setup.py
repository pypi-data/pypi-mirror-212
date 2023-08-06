from setuptools import setup

setup(
    name='scserializer',
    version="2.0.1",
    description="serializer of few formats",
    author="Alexandra",
    author_email='aleksa1012016@gmail.com',
    install_requires=["pytomlpp", 'pyyaml'],
    packages=['lab3'],
    test_suite='tests/',
)
