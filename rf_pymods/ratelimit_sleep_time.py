# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2026 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT

import datetime
import logging
import math

import dateutil.parser
import requests


def ratelimit_sleep_time(response: requests.Response, accel: float = 10.0, leniency: float = 1.0) -> datetime.timedelta:
    """Determine sleep time from a requests response with ratelimit headers

    response: Logarithmic acceleration factor
    accel: Format string of default repr/str output
    leniency: Seconds to add if next request lands right on the reset
    """
    # SPDX-SnippetComment: Originally from https://forge.colobox.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: © 2026 Ryan Finnie <ryan@finnie.org>
    # SPDX-LicenseInfoInSnippet: MIT

    if not all([response.headers.get(x) for x in ["date", "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset"]]):
        # If no ratelimit info is present, return an empty timedelta,
        # which can still be used for time.sleep(t.total_seconds()) (zero)
        return datetime.timedelta()
    # If it's less than [leniency] seconds before reset, return [leniency] instead of the caluclated time
    leniency_td = datetime.timedelta(seconds=leniency)
    # Cutoff point to determine if a number is a millisecond Unix epoch, a second Unix epoch, or a delta
    guess_epoch_td = datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    api_current_ts = dateutil.parser.parse(response.headers.get("date"))
    api_limit = float(response.headers.get("x-ratelimit-limit"))
    api_remaining = float(response.headers.get("x-ratelimit-remaining"))
    api_reset_ts = None
    try:
        reset_float = float(response.headers.get("x-ratelimit-reset"))
    except ValueError:
        # ISO 8601 (Mastodon, Jira, etc)
        api_reset_ts = dateutil.parser.parse(response.headers.get("x-ratelimit-reset"))
    if api_reset_ts is None:
        if reset_float > (guess_epoch_td.timestamp() * 1000.0):
            # Epoch time, milliseconds
            api_reset_ts = datetime.datetime.fromtimestamp(reset_float / 1000.0, tz=datetime.timezone.utc)
        elif reset_float > guess_epoch_td.timestamp():
            # Epoch time, seconds (GitHub, etc)
            api_reset_ts = datetime.datetime.fromtimestamp(reset_float, tz=datetime.timezone.utc)
        else:
            # Delta, seconds
            api_reset_ts = api_current_ts + datetime.timedelta(seconds=reset_float)
    if api_reset_ts < api_current_ts:
        # Handle negative cases
        api_reset_ts = api_current_ts
    # Time remaining until reset
    api_reset_td = api_reset_ts - api_current_ts
    logging.debug(
        "Rate limit: {}/{} remaining until {} ({})".format(
            api_remaining,
            api_limit,
            api_reset_ts,
            api_reset_td,
        )
    )
    if api_remaining <= 0:
        # No remaining request, wait until reset
        return api_reset_td + leniency_td
    if api_reset_td < leniency_td:
        # If it's less than [leniency] seconds before reset, return [leniency] instead of the caluclated time
        return leniency_td
    if accel > 1:
        # Logarithmic weighting of faster requests at the beginning of a window
        sleep_td = api_reset_td / (api_remaining + 1) * math.log(api_limit / api_remaining, accel)
    else:
        # Even distribution of requests throughout the window
        sleep_td = api_reset_td / (api_remaining + 1)
    if sleep_td >= api_reset_td:
        # Avoid lining up a future request exactly at (or greatly after) the reset time
        sleep_td = api_reset_td + leniency_td
    return sleep_td
