from setuptools import setup, find_packages


setup(
    name='nbgrader-server',
    version='0.1',
    description='API server for nbgrader',
    author='Dmitry Gerasimenko',
    author_email='kiddima@gmail.com',
    url='https://github.com/kidig/nbgrader-server',
    license='BSD',
    keywords=['jupyter-notebook', 'nbgrader', 'tornado'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=[
        'tornado>=5.1',
        'nbgrader>=0.5',
    ],
    packages=find_packages(),
    scripts=['server.py'],
)