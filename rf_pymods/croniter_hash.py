# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import binascii
import random
import re

import croniter


class croniter_hash(croniter.croniter):
    """Extend croniter with hash/random support

    All croniter.croniter functionality is supported; in addition,
    Jenkins-style "H" hashing is supported, or "R" for random.  Keyword
    argument "hash_id" (a croniter_hash-specific addition) is required
    for "H" definitions.

    Note that hash functionality has been upstreamed as of croniter
    1.0.12, but this extension is backwards compatible with older and
    newer croniter.
    """

    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    hash_expression_re = re.compile(
        r"^(?P<hash_type>h|r)(\((?P<range_begin>\d+)-(?P<range_end>\d+)\))?(\/(?P<divisor>\d+))?$"
    )

    def __init__(self, expr_format, *args, **kwargs):
        hash_id = None
        if "hash_id" in kwargs:
            hash_id = kwargs["hash_id"]
            del kwargs["hash_id"]
        if hash_id is None or isinstance(hash_id, bytes):
            pass
        elif isinstance(hash_id, str):
            hash_id = hash_id.encode("UTF-8")
        else:
            raise TypeError("hash_id must be bytes or UTF-8 string")
        expr_format = self._ch_hash_replace(expr_format, hash_id=hash_id)
        return super(croniter_hash, self).__init__(expr_format, *args, **kwargs)

    def _ch_hash_do(
        self, idx, hash_type="h", hash_id=None, range_end=None, range_begin=None
    ):
        """Return a hashed/random integer given range/hash information"""
        if not range_end:
            range_end = self.RANGES[idx][1]
        if not range_begin:
            range_begin = self.RANGES[idx][0]
        if hash_type == "r":
            crc = random.randint(0, 0xFFFFFFFF)
        else:
            crc = binascii.crc32(hash_id) & 0xFFFFFFFF
        return ((crc >> idx) % (range_end - range_begin + 1)) + range_begin

    def _ch_hash_replace(self, expr_format, hash_id=None):
        """Replace a hashed/random expression with its normal representation"""
        expr_aliases = {
            "@midnight": ("0 0 * * *", "h h(0-2) * * * h"),
            "@hourly": ("0 * * * *", "h * * * * h"),
            "@daily": ("0 0 * * *", "h h * * * h"),
            "@weekly": ("0 0 * * 0", "h h * * h h"),
            "@monthly": ("0 0 1 * *", "h h h * * h"),
            "@yearly": ("0 0 1 1 *", "h h h h * h"),
            "@annually": ("0 0 1 1 *", "h h h h * h"),
        }
        expr_format = expr_format.lower()
        if expr_format in expr_aliases:
            if hash_id is None:
                expr_format = expr_aliases[expr_format][0]
            else:
                expr_format = expr_aliases[expr_format][1]

        return " ".join(
            [
                self._ch_hash_expand_expr(expr, idx, hash_id=hash_id)
                for idx, expr in enumerate(expr_format.split())
            ]
        )

    def _ch_hash_expand_expr(self, expr, idx, hash_id=None):
        """Expand a hashed/random expression to its normal representation"""
        hash_expression_re_match = re.match(self.hash_expression_re, expr)
        if not hash_expression_re_match:
            return expr
        m = hash_expression_re_match.groupdict()

        if m["hash_type"] == "h" and hash_id is None:
            raise croniter.CroniterBadCronError(
                "Hashed definitions must include hash_id"
            )

        if m["range_begin"] and m["range_end"] and m["divisor"]:
            # Example: H(30-59)/10 -> 34-59/10 (i.e. 34,44,54)
            return "{}-{}/{}".format(
                self._ch_hash_do(
                    idx,
                    hash_type=m["hash_type"],
                    hash_id=hash_id,
                    range_end=int(m["divisor"]),
                )
                + int(m["range_begin"]),
                int(m["range_end"]),
                int(m["divisor"]),
            )
        elif m["range_begin"] and m["range_end"]:
            # Example: H(0-29) -> 12
            return str(
                self._ch_hash_do(
                    idx,
                    hash_type=m["hash_type"],
                    hash_id=hash_id,
                    range_end=int(m["range_end"]),
                    range_begin=int(m["range_begin"]),
                )
            )
        elif m["divisor"]:
            # Example: H/15 -> 7-59/15 (i.e. 7,22,37,52)
            return "{}-{}/{}".format(
                self._ch_hash_do(
                    idx,
                    hash_type=m["hash_type"],
                    hash_id=hash_id,
                    range_end=int(m["divisor"]),
                ),
                self.RANGES[idx][1],
                int(m["divisor"]),
            )
        else:
            # Example: H -> 32
            return str(self._ch_hash_do(idx, hash_type=m["hash_type"], hash_id=hash_id))
