# dnshole

dnshole.py is a python tool that combines public dns block lists into a single hosts file. It deduplicates entries, optionally prefixes a local hosts file, and prevents locally defined hosts from being modified.

## Usage

Copy `dnshole.py` and `sources.list` to `/opt/dnshole` and run `/opt/dnshole/dnshole.py`:

```
usage: dnshole.py [-h] [-l LOCAL] [-v] sources output

positional arguments:
  sources               sources file
  output                output file

optional arguments:
  -h, --help            show this help message and exit
  -l LOCAL, --local LOCAL
                        local hosts file
  -v, --verbose
```

#### Periodically update /etc/hosts

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