htm.advanced
==============

This package contains a port to Python3 and htm.core of the location framework code from the [htmresearch repository](https://github.com/numenta/htmresearch) of Numenta. 
htmresearch contains experimental algorithm work done internally at Numenta.

The htmresearch code was written in Python2 which is reaching end of life at the end of 2019. Numenta has stated that it has no plans to port htmresearch to Python3 and is no longer going continue development in the htmresearch repository.

Since Numenta is no longer developing in htmresearch, the API in htm advanced can be considered stable. The only caveat is that the modules directly use the htm Connections class so any changes to its API may effect htm advanced.

Location Framework
==============
The location framework is the code that underlies Jeff Hawkins [Thousand Brains model of the Neocortex](https://numenta.com/neuroscience-research/research-publications/papers/a-framework-for-intelligence-and-cortical-function-based-on-grid-cells-in-the-neocortex/) and hence is probably the most important framework in htmresearch.  
There are some example applications showing how to use the location framework.

Additional goodies are the RawSensor and RawValues regions, the GridCellLocationRegion and the ColumnPoolerRegion.

Future Additions
================
Other frameworks from htmresearch may be added in the future.

Namespace
=========
The location framework is located in the htm.advanced namespace. In the future it may be promoted to the htm namespace.

Connections
===========
A subclass of the htm.core Connections class can be found in htm.advanced.algorithms.connections.py. This subclass supplies APIs that were provided in nupic.core and were not yet implemented in htm.core as well as some additional convenience methods.
Hopefully, for performance and completeness, these will be added to the htm.core cpp implementation.

Install python dependencies
===========
In order to run this python code, one must install extras requirements by running
```
pip install htm.core[examples]
```
or if building from source run in root of repository
```
pip install -e .[examples]
```
