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

The decapsulation starts with a call to the decryption routine, which computes the matrix :math:`\mathbf{M}` as

.. math::
   \mathbf{M} = \mathbf{C} - \mathbf{B'S} = \mu + \mathbf{S'E} - \mathbf{E'S} + \mathbf{E''}.

We can then define the combined noise matrix as

.. math::
   \mathbf{E'''} = \mathbf{S'E} - \mathbf{E'S} + \mathbf{E''},

which is a linear function of the secret key. Now, since a modification to the ciphertext is essentially equivalent to a modification to the noise matrix, a decryption error indicates that the modified entry in the noise matrix is at least as big as some specific threshold whose value is known. Finding the minimal modification leading to an error then determines the entry's original value. Repeating this enough times, one gets linear equations in the values of :math:`\mathbf{S}`, which can easily be solved (handling possible errors while obtaining the system coefficients).

.. [alkim-et-al] FrodoKEM Learning With Errors Key Encapsulation Algorithm Specifications And Supporting Documentation

   https://frodokem.org/files/FrodoKEM-specification-20200930.pdf
