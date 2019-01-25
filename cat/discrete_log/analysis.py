"""
Tools for analyzing systems based on discrete logarithm hardness.
"""

from enum import Enum

from gmpy2 import is_prime, mpq, mpz


class Result(Enum):
    """Represents the result of an analysis."""

    SAFE_PRIME = 0
    """
    Indicates that all checks passed and that the modulus is a safe prime. A safe prime is of the form
    :code:`2q + 1` where :code:`q` is also prime.
    """
    NON_PRIME_MODULUS = 1
    """
    Indicates that the given modulus is not a prime number. A non-prime modulus :code:`p` can be factored
    into prime factors :code:`q_i`, which allows you to solve the discrete logarithm problem
    in :math:`O(\\sum_i e_i \\sqrt(q_i))` using `Pohlig-Hellman decomposition`_.

    .. _`Pohlig-Hellman decomposition`: https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm
    """
    SMALL_MODULUS = 2
    """
    Indicates that the given prime modulus is too small. "Smallness" is defined via a bound that is passed to
    the function returning this value and for the prime modulus to be "large enough" it has to be at least
    double the bit length of the given bound. This is due to the `Phollard Rho`_ algorithm and Shanks'
    `baby step-giant step`_ algorithm both being able to solve the discrete logarithm problem in
    :math:`O(\\sqrt(q))`, where :math:`q` is the order of the group (and since the modulus :code:`p` is prime,
    the order of the group :math:`q=p-1`).

    .. _`Phollard Rho`: https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm
    .. _`baby step-giant step`: https://en.wikipedia.org/wiki/Baby-step_giant-step
    """
    SMALL_SUBGROUP = 3
    """
    Indicates that the size of the generated subgroup is 1-2. This happens when :math:`g` is the identity
    (:math:`1`) or :math:`p-1`.
    """
    UNKNOWN = 4
    """
    Indicates that none of the above results hold. It is possible that :math:`p` has small prime factors,
    which would allow for a (partial) key recovery attack using `Pohlig-Hellman decomposition`_.
    """


def check_components(g, p, B=512):
    # type: (int, int, int) -> Result
    """
    Takes a modulus :attr:`p` and a generator :attr:`g` together with an optional bound :attr:`B` and
    checks various conditions that must hold for e.g. Diffie-Hellman Key Exchange. If one of these
    conditions is violated, the failing condition is returned as defined in :class:`Result`.

    The conditions that are verified are:
    * Is :attr:`p` a prime number?
    * Is the bit size of :attr:`p` greater than :code:`2*B`?
    * Is the biggest prime factor of :attr:`p` greater than :code:`B`?
    * Is :attr:`p` a safe prime?

    .. warning::
        It is not feasible to check the actual subgroup order generated by :code:`g` (if :code:`p`
        is a non-safe prime). It is therefore possible that a :class:`Result` of :class:`Result.UNKOWN`
        is insecure if :code:`p` does not have large prime factors.

    For further information on these conditions, you can refer to:
    * "On Diffie-Hellman Key Agreement with Short Exponents" by van Oorschot and Wiener
    * "Minding your p's and q's" by Anderson and Vaudenay
    * "Measuring small subgroup attacks against Diffie-Hellman" by Valenta, et.al.

    >>> result = check_components(1, 4)
    >>> result == Result.SMALL_SUBGROUP
    True
    >>> result = check_components(3, 4)
    >>> result == Result.SMALL_SUBGROUP
    True
    >>> result = check_components(2, 4)
    >>> result == Result.NON_PRIME_MODULUS
    True
    >>> result = check_components(2, 7)
    >>> result == Result.SMALL_MODULUS
    True
    >>> from cat.utils.ntheory import gen_safe_prime
    >>> safe_prime = gen_safe_prime(512)
    >>> result = check_components(3, safe_prime, B=256)
    >>> result == Result.SAFE_PRIME
    True
    >>> import gmpy2
    >>> big_prime = gmpy2.next_prime(2**(2*512))
    >>> result = check_components(3, big_prime)
    >>> result == Result.UNKNOWN
    True

    :param g: A generator for the group mod :attr:`p`.
    :param p: A prime number used as a modulus of the group.
    :param B: A bound that defines "largeness" or "smallness". I.e. :attr:`p` is said to be a "large" prime
              if it satisfies :code:`p > 2*B`. Defaults to :code:`512`.
    :returns: A :class:`Result`.
    """
    # g == 1 or g == p-1 generates a subgroup of order 1-2
    if g == 1 or g == (p - 1):
        return Result.SMALL_SUBGROUP
    # Check if p is prime
    if not is_prime(mpz(p)):
        return Result.NON_PRIME_MODULUS
    # Check size of p
    if p.bit_length() < 2 * B:
        return Result.SMALL_MODULUS
    # Check whether we have a safe prime
    p_ = mpz(mpq(p - 1) / 2)
    if is_prime(mpz(p_)):
        # The only possible subgroup orders are: 1, 2, q, 2q.
        # Any generator 1 < g < p-1 generates a subgroup of order q or 2q.
        if 1 < g < p - 1:
            return Result.SAFE_PRIME
    return Result.UNKNOWN


def check_private_exponent(a, B=512):
    """
    Checks the bit length of the given private exponent.

    If you've asked for a random number of bit length at least :param:`B`, but are retrieving
    numbers that are smaller than said size, you might want to check your RNG.

    >>> B = 8
    >>> a = 0b11111111
    >>> check_private_exponent(a, B)
    (8, 1)
    >>> a = 0b1111111
    >>> check_private_exponent(a, B)
    (7, 0.5)
    >>> a = 0b111111
    >>> check_private_exponent(a, B)
    (6, 0.25)
    >>> a = 0b11111
    >>> check_private_exponent(a, B)
    (5, 0.125)
    >>> a = 0b1111
    >>> check_private_exponent(a, B)
    (4, 0.0625)

    :param a: The private exponent.
    :param B: The boundary (i.e. bit length) to check for, defaults to :code:`512` bits.
    :returns: A tuple containing :param:`a`'s actual bit length and the probability of receiving
              a number of that bit length from an RNG if you've asked for a number of bit length
              at least :param:`B`. If :param:`a`'s bit length is greater than :param:`B`, the
              probability is set to :code:`1`.
    """
    bit_len = a.bit_length()

    if bit_len < B:
        zero_bits = B - bit_len
        probability = float(1) / 2 ** zero_bits

        return (bit_len, probability)
    return (bit_len, 1)
