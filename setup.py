from setuptools import setup, find_packages

setup(
    name='jntemplate',
    version=0.1,
    description=(
        '<项目的简单描述>'
    ),
    long_description=open('README.rst').read(),
    author='jiniannet',
    author_email='hnvvv@163.com',
    maintainer='jiniannet',
    maintainer_email='hnvvv@163.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='http://www.jiniannet.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
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