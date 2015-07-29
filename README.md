Mri-python-client
========
[![Build Status](https://travis-ci.org/Mri-monitoring/Mri-python-client.svg?branch=master)](https://travis-ci.org/Mri-monitoring/Mri-python-client)

> Neural network monitoring

The Python client for Mri offers easy monitoring of neural networking training, for example with Theano or pylearn.

## Installing

Optional: create a virtual environment to house the installation.

```
$ mkvirtualenv -p /usr/bin/python2.7 Mri
$ workon Mri
```

Install appropriate requirements to Python and install the Mri library
```
$ git clone https://github.com/Mri-monitoring/Mri-python-client.git 
$ cd Mri-python-client
$ pip install -r requirements.txt
$ python setup.py install
```

Note that not all backends require all of the requirements. For example, only the Matplotlib-dispatch backend requires Matplotlib.

## Python Library
See `examples/python_bindings` for an example of how to use the Python bindings. The bindings will require a backend to use, for example the [Mri-server](https://github.com/Mri-monitoring/Mri-server).
