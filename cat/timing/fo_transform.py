def error_oracle(plaintext, modification, pk, h, encrypt, decaps_timing, detect_err):
    """
    Determines whether adding some modification to the encryption of some
    message leads to a decapsulation error by analyzing the time it takes for
    the decryption to be performed

    Args:
        plaintext (int): (random) message to be encrypted for encapsulation
        modification (int): modification to add to the ciphertext
        pk (int): public key
        h ((int, int) -> (int, int)): hash function for `plaintext` and `pk`
        encrypt ((int, int, int) -> int): encryption function of `pk`, `plaintext` and
            some random bits
        decaps_timing ((int) -> int): function timing the decapsulation of a ciphertext
        detect_err ((int) -> bool): function determining if a decryption error occurred
            from a decapsulation time

    Returns:
        bool: a value indicating whether a decapsulation error occurred
    """

    r, k = h(plaintext, pk)
    ciphertext = encrypt(pk, plaintext, r)
    modified = ciphertext + modification
    time = decaps_timing(modified)
    return detect_err(time)


def recover_sk(n, message_gen, pk, h, encrypt,
               decaps_timing, detect_err, extract_sk):
    """
    Recovers a secret key by generating successive plaintext messages, then finding
    maximal ciphertext modifications such that no decapsulation error occurs, and
    using these values to recover secret information

    Args:
        n (int): number of plaintext messages to generate
        message_gen (() -> int): function generating messages
        pk (int): public key
        h ((int, int) -> (int, int)): hash function for plaintexts and `pk`
        encrypt ((int, int, int) -> int): encryption function for `pk`, a message
            and some random bits
        decaps_timing ((int) -> int): function timing the decapsulation of a ciphertext
        detect_err ((int) -> bool): function determining if a decryption error occurred
            given a decapsulation time
        extract_sk ((list[(int, int)]) -> int): function extracting a secret key given
            a list of messages and corresponding modifications as described above

    Returns:
        int: the secret key corresponding to `pk`
    """

    pairs = []
    for _ in range(n):
        m = message_gen()
        modification = 0
        while not error_oracle(m, modification + 1, pk, h,
                               encrypt, decaps_timing, detect_err):
            modification += 1

        pairs.append((m, modification))

    return extract_sk(pairs)
