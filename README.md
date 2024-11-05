# hostgroup_click
Python script that gathers a list of hostgroups that a host or list of hosts belongs to.

## Configure
Put all files in same directory
If running on linux change the path for the yaml by removing double quotes.

### Edit the YAML
Change the URL and API Key for your NagiosXI Servers.

## Command
Takes a single host name or double quote encapsulated comma seperated list of hosts.

    hostgroup_click.py -n drs -H "localhost,u2204ncpa"

## Results

    localhost was found in 1 of 6 toal hostgroups. [linux-servers]
    u2204ncpa was found in 2 of 6 toal hostgroups. [linux-servers,linux-columbia-mo]

## -o/--origin
    localhost was found in 1 of 6 total hostgroups. [linux-servers]
    u2204ncpa was found in 2 of 6 total hostgroups. [linux-columbia-mo,linux-servers] Membership for 1 groups is assigned via the u2204ncpa host object config. [dev-linux-web]
