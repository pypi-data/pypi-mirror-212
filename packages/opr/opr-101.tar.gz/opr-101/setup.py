# This file is placed in the Public Domain.
# pylint: disable=E231


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name='opr',
    version='101',
    url='https://github.com/bthate/opr',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="object programming runtime",
    long_description=read(),
    long_description_content_type='text/x-rst',
    license='Public Domain',
    packages=[
              "opr",
              "opr.modules"
             ],
    zip_safe=True,
    scripts=[
             "bin/opr",
            ],
    classifiers=[
                 'Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
