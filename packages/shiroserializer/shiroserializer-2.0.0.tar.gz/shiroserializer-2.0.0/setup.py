from setuptools import setup

setup(
    name='shiroserializer',
    version="2.0.0",
    description="serializer of XML and JSON",
    author="NLShiro",
    author_email='artem.rogachev@tut.by',
    url='https://github.com/NLShiro/pyserializer',
    install_requires=["pytomlpp", 'pyyaml'],
    packages=['lab3'],
    test_suite='tests/',
)
