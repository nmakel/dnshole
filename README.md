# dnshole

dnshole.py is a python tool that combines public DNS block lists into a single hosts file. It deduplicates entries, optionally prefixes a local hosts file, and prevents locally defined hosts from being modified.


## Usage

Copy `dnshole.py` and `sources.list` to `/opt/dnshole` and run `/opt/dnshole/dnshole.py`:

```
usage: dnshole.py [-h] [-a ADDR] [-l LOCAL] [-v] sources output

positional arguments:
  sources               sources file
  output                output file

optional arguments:
  -h, --help            show this help message and exit
  -a ADDR, --addr ADDR  destination address
  -l LOCAL, --local LOCAL
                        local hosts file
  -v, --verbose
```


### Add or remove source lists

Entries in `sources.list` are python `dict` items in a `list`. Their properties are:

```
    {
        "enabled": True,
        "name": "Sample List",
        "url": "https://example.org/list",
        "pattern": r"^127\.0\.0\.1[\s]+([0-9a-zA-Z_\-\.]+)"
    }
```

Public or private lists of advertising or otherwise undesirable domains can be included by adding an entry such as the one above. The `pattern` property is a regular expression that results in only a single fully qualified domain name per line. Modify this regular expression to suit the source material. Set `enabled` to `False` to disable an entry.


### 127.0.0.1 or 0.0.0.0

The destination address of all hosts in the output hosts list is `127.0.0.1` by default, but can be modified by passing the `-a` or `--addr` parameter, followed by the destination IP address. This may be useful if `0.0.0.0` results in faster loading times in your particular situation, or if you need to redirect requests to another system.


### Periodically update /etc/hosts

**Before you begin:** you should copy `/etc/hosts` to `/etc/hosts.local`. Provide this file using the `--local` parameter to have its contents placed at the start of the output hosts file.

To run dnshole periodically, create the following shell script at `/usr/local/bin/update_dnshole.sh`, not forgetting to `chmod +x` the file:

```
#!/usr/bin/env sh

/opt/dnshole/dnshole.py -l /etc/hosts.local /opt/dnshole/sources.list /etc/hosts

# uncomment the following line to have dnsmasq reload its hosts files
#systemctl reload dnsmasq
```

Next, add the following entry to `/etc/crontabs` to have `/usr/local/bin/update_dnshole.sh` executed every day at midnight:

```
0 0 * * * root /usr/local/bin/update_dnshole.sh
```

Run `systemctl restart cron` to have cron re-read the crontab file.