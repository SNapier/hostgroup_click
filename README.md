# hostgroup_click
Python script that gathers a list of hostgroups that a host or list of hosts belongs to.

## Configure
Put all files in same directory
If running on linux change the path for the yaml by removing double quotes.

### Edit the YAML
Change the URL and API Key for your NagiosXI Servers.

## Command
Takes a single host name or double quote encapsulated comma seperated list of hosts.
Use known hosts only.

    hostgroup_click.py -n drs -H "localhost,u2204ncpa"

## Results

    localhost: total_groups=1;  Membership for 1 group/s is assigned via hostgroup object config/s. [linux-servers]
    u2204ncpa: total_groups=3;  Membership for 2 group/s is assigned via hostgroup object config/s. [linux-columbia-mo,linux-servers] Membership for 1 group/s is assigned via host object config/s. [dev-linux-web]
