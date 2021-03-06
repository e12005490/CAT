from cat.prng.lcg import (
    construct_lattice,
    reconstruct_lcg_state,
    reconstruct_lehmer_lower,
)
from cat.utils import descriptors
from cat.utils.descriptors import Adversary


class PRNGStoker(Adversary):
    # TODO: we need to set `shift`, but `shift` is documented nowhere!
    #   - same goes for `modulus`
    #   - we might want to use mpz instead of int
    """
    A convenience class for performing attacks on PRNGs that checks the correctness of input values.
    """

    increment = descriptors.Number(int, forbidden_values=[0])
    """ The increment for (Lehmer style) LCG prediction. """
    modulus = descriptors.Number(int, forbidden_values=[0])
    """ The modulus for (Lehmer style) LCG prediction. """
    multiplier = descriptors.Number(int, forbidden_values=[0])
    """ The multiplier for (Lehmer style) LCG prediction. """
    samples = descriptors.TypedList(min_length=3, element_type=int)
    """ Consecutive sample outputs of a truncated (Lehmer style) LCG. """
    shift = descriptors.Number(int)
    """ The shift applied during (Lehmer style) LCG prediction. """
    __states = descriptors.List(min_length=1)

    def reconstruct_lehmer_state(self):
        # type: (PRNGStoker) -> int
        r"""
        Uses the :attr:`samples` of the stoker as states of a Lehmer style LCG and
        reconstructs the first state.

        An Lehmer style LCG uses an initial state :math:`s_0` (often called seed),
        a multiplier parameter :math:`a` and a modulus :math:`m`.
        The states of a Lehmer style LCG are computed by the recurrence relation
        :math:`s_{i+1} = a \cdot s_0` \mod m.

        :returns: The first state of the recurrence relation :math:`s_1`
        """
        L = construct_lattice(self.modulus, self.multiplier, len(self.samples))

        lower_bits = reconstruct_lehmer_lower(L, self.modulus, self.samples)

        self.__states = [
            (x + y) % self.modulus for (x, y) in zip(lower_bits, self.samples)
        ]

        return self.__states[0]

    def reconstruct_lcg_state(self):
        # type: (PRNGStoker) -> int
        r"""
        Uses the :attr:`samples` of the stoker as states of an LCG and
        reconstructs the first state.

        An LCG uses an initial state :math:`s_0` (often called seed),
        a multiplier parameter :math:`a`, an increment :math:`b`
        and a modulus :math:`m`.
        The states of an LCG are computed by the recurrence relation
        :math:`s_{i+1} = a \cdot s_0 + b` \mod m.

        :returns: The first state of the recurrence relation :math:`s_1`
        """
        lower_bits = reconstruct_lcg_state(
            self.modulus, self.multiplier, self.increment, self.samples, self.shift
        )

        self.__states = [
            (x + y) % self.modulus for (x, y) in zip(lower_bits, self.samples)
        ]

        return self.__states[0]
