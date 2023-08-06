from setuptools import setup

setup(
    name='barney_log',
    version='0.1',
    description='A logging library for Python',
    author='Barney Liu',
    author_email='bernayliu708@gmail.com',
    packages=['barney_log'],
    install_requires=[
        'datetime',
        'logging',
        'os',
        'sys'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)