from setuptools import setup, find_packages


VERSION = '0.0.6'
DESCRIPTION = 'This project is a Python script that utilizes built-in trace tools like tracert for Windows and traceroute for Linux to perform a traceroute to a given hostname or IP address. It traces the path that packets take from your device to the destination host, providing ip addresses'
LONG_DESCRIPTION = '''
pyhop is a Python package that simplifies the process of performing traceroutes by utilizing the built-in trace tools, tracert for Windows and traceroute for Linux. This package provides a consistent interface and reliable results across different platforms, allowing network administrators, developers, and users to diagnose network issues and optimize performance with ease. 

With pyhop, you can effortlessly trace the path of packets from your device to a destination host, gaining valuable insights into network connectivity.

Usage Example:

from pyhop import traceroute

print(traceroute('google.com'))

'''

# Setting up
setup(
    name="pyhop",
    version=VERSION,
    author="Sarthak",
    author_email="<waliasarthak@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'traceroute', 'tracert',
              'hops', 'ip address', 'server hops'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
