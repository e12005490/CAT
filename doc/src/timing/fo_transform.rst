Fujisaki-Okamoto Transform
==========================

The Fujisaki-Okamoto transform (FOT) is a way to convert weak asymmetric and symmetric encryption schemes into a stronger (IND-CCA-secure) asymmetric scheme.

Variations of this transformation can be used to create IND-CCA-secure key encapsulation mechanisms (KEM), which are used to ensure secure sharing of symmetric keys using asymmetric schemes. Such a variation is given in [hofheinz-et-al]_:

.. image:: ../figures/fo_kem.*
	:width: 100 %

where :math:`\mathsf{PKE}_1 = (\mathsf{Gen}_1, \mathsf{Enc}_1, \mathsf{Dec}_1)` is the underlying asymmetric scheme, :math:`\mathcal{M}` its message space, and :math:`\mathsf{H}` a hash function.

This module implements a general timing attack on KEMs based on the FOT assuming a slightly different implementation, both explained in [guo-et-al]_.

The attack is based on the fact that, in this implementation, the decryption routine in the decapsulation algorithm does not return :math:`\perp` on a decryption error, but rather a wrong plaintext, this failure being detected by comparing the encryption of this plaintext and the given ciphertext parameter.

The key observation is that this comparison is in principle not executed in constant time; in particular, the comparison time is shorter if the operands differ in their first bytes and longer if the operands are equal up to their last bytes.

From this, we can observe that if it is possible to slightly alter a ciphertext without changing the plaintext decrypted by :math:`\mathsf{Dec}_1` (which is the case e.g. in code-based schemes), then it is possible to find a maximal modification that does not result in a failed decryption using timing analysis of the decapsulation function. These specific values can then be used to recover secret information.

More information about the FOT can be found in [fujisaki-okamoto]_.

.. [fujisaki-okamoto] Secure Integration of Asymmetric and Symmetric Encryption Schemes

   https://link.springer.com/article/10.1007/s00145-011-9114-1

.. [guo-et-al] A key-recovery timing attack on post-quantum primitives using the Fujisaki-Okamoto transformation and its application on FrodoKEM

   https://eprint.iacr.org/2020/743

.. [hofheinz-et-al] A Modular Analysis of the Fujisaki-Okamoto Transformation

	https://eprint.iacr.org/2017/604.pdf
