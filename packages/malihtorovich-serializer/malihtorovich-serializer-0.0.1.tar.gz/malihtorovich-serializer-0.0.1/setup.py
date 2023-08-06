from setuptools import setup

setup(
    name='malihtorovich-serializer',
    version='0.0.1',
    packages=['serializer',
              'serializer.encoder',
              'serializer.serializers'],
    entry_points={
        "console_scripts": [
            "custom-serialize = serializer.custom_serializer:main"
        ]
    },
    url='',
    license='',
    author='vpg1',
    author_email='',
    description=''
)