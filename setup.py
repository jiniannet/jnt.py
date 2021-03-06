from setuptools import setup, find_packages
import io

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='jnt.py',
    version='0.1 Beta',
    description='Open source templating engine for python.',
    long_description=readme,
    author='jiniannet',
    author_email='hnvvv@163.com',
    maintainer='jiniannet',
    maintainer_email='hnvvv@163.com',
    license='MIT License',
    packages=['jntemplate'],
    platforms=["all"],
    url='http://www.jiniannet.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)