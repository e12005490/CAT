from .prng_stoker import PRNGStoker

"""
Parameters for glibc's rand_r or when invoking initstate with an 8 byte state.
"""
glibc_lcg_params = {"m": 2 ** 32, "a": 1103515245, "b": 12345, "shift": 0}
java_lcg_params = {"m": 2 ** 48, "a": 0x5DEECE66D, "b": 0xB, "shift": 48 - 16}
