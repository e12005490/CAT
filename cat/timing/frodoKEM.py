def frodoKEM_timing_attack(pk, ciphertexts, n, error_bound,
                           error_oracle, solver):
    """
    Recovers a FrodoKEM secret key by using valid ciphertexts and finding
    minimal modifications such that these ciphertexts are not correctly
    decapsulated. The recovered values can then be used to obtain linear
    equations in the secret key entries.

    Args:
        pk (int): public key.
        ciphertexts (List[List[List[int]]]): list of valid ciphertexts to use.
        n (int): number of entries to obtain for each ciphertext.
        error_bound (int): least value of an error matrix entry causing a
            decapsulation error.
        error_oracle ((int, List[List[int]]) -> bool): timing oracle returning
            whether or not the decapsulation of a ciphertext leads to an error.
        solver ((List[List[int]]) -> List[List[int]]): function recovering the
            secret key from the noise matrix values.

    Returns:
        List[List[int]]: the secret key `S`.
    """

    # noise matrix values for each ciphertext
    noise = [[] for _ in ciphertexts]

    for i, c in enumerate(ciphertexts):
        for j in range(n):
            # use binary search to find the minimal modification leading
            # to an error
            # `right` always produces an error, while `left` never does
            left, right = 0, 2 * error_bound

            while right > left + 1:
                mid = (right + left) / 2
                c[-1][j] += mid
                err = error_oracle(pk, c)
                c[-1][j] -= mid

                if err:
                    right = mid
                else:
                    left = mid

            # at this point, `right` is the minimal modification giving a
            # decapsulation error
            noise[i].append(error_bound - right)

    # recover the secret key
    return solver(noise)
