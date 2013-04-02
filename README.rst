==========================
Rogers Email Notifications
==========================

Scrapers for sending auto-updates of information from your My Rogers account.
The main motivation for this is daily updates of bandwidth usage, but maybe
I'll make some scrapers to pull other info.

Example
-------

::

    >> from rogers_usage.session import RogersSession
    >> from rogers_usage.usage   import current_usage_info
    >> session = RogersSession('user@example.com', 'password123')
    >> info = current_usage_info(session)
    >> info
    {
        'allowance'     : 120.0,
        'billing_period': 'March 08, 2013 - April 07, 2013',
        'download_usage': 95.46,
        'left'          : 17.48,
        'total_usage'   : 102.52,
        'upload_usage'  : 7.06,
    }

Credits
-------

Copyright 2013 Brandon Sandrowicz <brandon@sandrowicz.org>

License
-------

MIT License. See LICENSE for text.
