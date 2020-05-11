#!/usr/bin/env python3

import argparse
import re
import requests


LOCAL_ADDR = "127.0.0.1"
LOCAL_RE = r"^[0-9a-fA-F:\.]+[\s]+([0-9a-zA-Z_\-\.]+)$"


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("sources", type=str, help="sources file")
    argparser.add_argument("output", type=str, help="output file")
    argparser.add_argument("-a", "--addr", type=str, default=LOCAL_ADDR, help="destination address")
    argparser.add_argument("-l", "--local", type=str, help="local hosts file")
    argparser.add_argument("-v", "--verbose", action="store_true", default=False)
    args = argparser.parse_args()

    local_data = ""
    results = set()
    excluded = set([
        "local",
        "localhost",
        "localhost.localdomain",
        "broadcasthost",
        "ip6-localhost",
        "ip6-loopback",
        "ip6-localnet",
        "ip6-mcastprefix",
        "ip6-allnodes",
        "ip6-allrouters",
        "ip6-allhosts"
    ])

    if args.local:
        with open(args.local, "r") as local_file:
            local_data = local_file.read()

            if args.verbose:
                print(f"Read local file {args.local}")

            for local_result in re.findall(LOCAL_RE, local_data, re.MULTILINE):
                excluded.add(local_result)

    with open(args.sources, "r") as sources_file:
        sources = eval(sources_file.read())

        if args.verbose:
            print(f"Read sources file {args.sources}")
            print(f"{len(sources)} sources found")

    for source in sources:
        if not source['enabled']:
            print(f"Source {source['name']} is disabled, skipping")
            continue

        add_count = 0
        raw_count = 0

        if args.verbose:
            print(f"Requesting {source['name']}")

        try:
            source_request = requests.get(source["url"])

            if source_request.status_code != 200:
                raise Exception(f"Unable to load {source['url']}")

            source_data = source_request.content.decode("utf-8")

            for source_result in re.findall(source["pattern"], source_data, re.MULTILINE):
                raw_count += 1

                if (source_result not in excluded
                    and source_result not in results):
                    results.add(source_result)
                    add_count += 1
        except Exception as e:
            print(f"Error: {e}")

        if args.verbose:
            print(f"Added {add_count}/{raw_count} hosts")

    with open(args.output, "w") as out_file:
        if local_data:
            out_file.write(local_data)
            out_file.write("\n")

        for r in results:
            out_file.write(f"{args.addr} {r}\n")

        if args.verbose:
            print(f"Wrote {len(results)} hosts to {args.output}")
