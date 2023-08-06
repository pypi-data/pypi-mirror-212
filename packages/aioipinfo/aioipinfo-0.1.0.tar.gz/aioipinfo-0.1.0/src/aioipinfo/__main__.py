"""CLI for aioipinfo."""

import argparse
import asyncio
import logging
import os
import sys

from . import IPAddress, IPInfoClient, IPInfoError


PARSER = argparse.ArgumentParser(
    description="Return the free ipinfo.io information on the given IP Address."
)
PARSER.add_argument(
    "addresses", help="The IP address(es) to lookup.", nargs="+", metavar="IP"
)
PARSER.add_argument(
    "--debug", help="Print exceptions when there is an error.", action="store_true"
)
PARSER.add_argument(
    "--token", help="Use this API token instead of reading $IPINFO_TOKEN."
)


async def query_ip(client: IPInfoClient, address: IPAddress) -> None:
    """Query for a single IP and print the result.

    Calls `pprint` on the `IPInfoResponse`. Errors are logged.

    Parameters
    ----------
    client : IPInfoClient
        The client to query with.
    address : IPAddress
        The IP to query.
    """

    try:
        info = await client.ipinfo(address)
    except IPInfoError as err:
        exc_info = (
            sys.exc_info() if logging.getLogger().level == logging.DEBUG else None
        )
        logging.critical(f"Error querying ipinfo.io: {err}", exc_info=exc_info)
    else:
        info.pprint()


async def main():
    """Entry point."""

    args = PARSER.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    if args.token:
        token = args.token
    else:
        try:
            token = os.environ["IPINFO_TOKEN"]
        except KeyError:
            logging.critical("Unable to find ipinfo.io API token.")
            sys.exit(1)

    client = IPInfoClient(token)

    await asyncio.gather(*[query_ip(client, address) for address in args.addresses])

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
