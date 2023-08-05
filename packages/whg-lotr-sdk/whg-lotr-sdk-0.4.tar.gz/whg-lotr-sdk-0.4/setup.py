from setuptools import setup


setup(
    name='whg-lotr-sdk',
    version='0.4',
    packages=['lotr_sdk', 'lotr_sdk.handlers', 'lotr_sdk.tests'],
    url='https://github.com/whgest/whg-lotr-sdk',
    install_requires=[
        'requests==2.31.0',
        'urllib3==1.26.6',
        'pytest==7.1.3'
      ],

)