.. testsetup:: *
   from cat import *

:mod:`cat.timing` --- Timing Attacks
====================================

.. epigraph::

   [A] timing attack is a side-channel attack in which the attacker attempts to compromise a cryptosystem by analyzing the time taken to execute cryptographic algorithms.

   -- `Wikipedia`_.

.. _Wikipedia: https://en.wikipedia.org/wiki/Timing_attack


Cryptographic algorithms often run in non-constant time because of variable cache accesses, conditional branches or optimization of some operations (among which comparisons, multiplications or exponentiations) which are all determined by inputs. This means that analyzing the runtime of insecure algorithms can yield information about secret parameters, and compromise the security of the system.

:mod:`cat.timing` provides different attacks based on timing analysis.


Attacks
-------
.. toctree::
   :glob:

   timing/*
