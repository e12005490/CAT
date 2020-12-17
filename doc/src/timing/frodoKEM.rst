FrodoKEM
========

`FrodoKEM <https://frodokem.org/>`_ is a key encapsulation mechanism (KEM) based on an :math:`\mathsf{IND}`-:math:`\mathsf{CPA}` public-key encryption scheme transformed into an :math:`\mathsf{IND}`-:math:`\mathsf{CCA}` KEM using a variation of the Fujisaki-Okamoto transform described in [hofheinz-et-al]_.

As with timing attacks against scheme based on some general variation of the :doc:`fo_transform`, FrodoKEM is vulnerable if the comparison used in the decapsulation algorithm to detect a decryption error is not made in constant time. The attack is detailed in [guo-et-al]_. The particular variation used is given below and found in the FrodoKEM specifications [alkim-et-al]_:

.. image:: ../figures/frodokem_fo.*

The underlying public-key scheme is based on the Learning With Errors problem, where keys are related by something similar to

.. math::
   \mathbf{B} = \mathbf{AS} + \mathbf{E}

with :math:`\mathbf{A, B}` publicly known matrices, :math:`\mathbf{S}` a secret matrix and :math:`\mathbf{E}` an error matrix with small entries.

The scheme also uses pseudorandom error matrices during encapsulation and decapsulation, which gives it the property that a sufficient modification to the ciphertext results in a decryption error, which can be detected if the check above is not done in constant time.

In particular, it is possible to find the entries in an error matrix which is a linear function of the secret matrix :math:`\mathbf{S}` by finding the minimal modifications to some valid ciphertexts (which can be easily generated) that induce a decryption error. :math:`\mathbf{S}` can then be recovered by solving the obtained linear equations (handling possible errors while obtaining the system coefficients).

.. [alkim-et-al] FrodoKEM Learning With Errors Key Encapsulation Algorithm Specifications And Supporting Documentation

   https://frodokem.org/files/FrodoKEM-specification-20200930.pdf
