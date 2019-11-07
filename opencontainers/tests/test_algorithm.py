#!/usr/bin/python

# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from opencontainers.digest import Digest
from opencontainers.digest.algorithm import (
    Algorithm,
    algorithms,
)

from opencontainers.digest.exceptions import (
    ErrDigestInvalidLength,
    ErrDigestInvalidFormat,
    ErrDigestUnsupported
)
import os
import io
import pytest



def test_digests(tmp_path):
    '''test creation of an opencontainers Digest
    '''
    # Generate random bytes
    p = b"\x00"+os.urandom(18)+b"\x00"

    for name, alg in algorithms.items():
        h = alg.hash()
        h.update(p) 
        expected = Digest("%s:%s" %(alg, h.hexdigest()))

        # Calculate from reader (not necessary for Python, but mirroring golang)
        newReader = io.BytesIO(p)
        readerDgst = alg.fromReader(newReader)

        assert alg.fromBytes(p) == readerDgst 
        #alg.fromString(string(p)) # need to figure out what this is for
