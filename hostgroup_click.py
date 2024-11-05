import requests, argparse, os,json

#EXPECTED IN THE SAME DIRECTORY AS THE PLUGIN
import nagiosxi_plugin_helper as xihlpr

#DEAL WITH THE SELF SIGNED NAGIOS SSL
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#GATHER THE LIST OF NAGIOS HOSTGROUOPS THAT A HOST OBJECT BELONGS TO.
#USES SINGLE OR LIST OF CSV LIST OF HOSTS
#SNAPIER

#SCRIPT DEFINITION
cname = "hostgroup_click"
cversion = "0.0.4"
appPath = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__" :
    
    #INPUT FROM NAGIOS
    args = argparse.ArgumentParser(prog=cname+" v:"+cversion, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #ARGS
    #NSID
    args.add_argument(
        "-n","--nsid",
        required=False,
        choices=("drs","dev","prd"),
        default=None,
        help="String(nsid): The target nagiosxi environment for the plugin in the yaml file."
    ),    
    #HOSTNAME/ADDRESS
    args.add_argument(
        "-H","--host",
        required=True,
        default=None,
        help="String(hostname/hostaddress): The target host or csv list of hosts to search for in the list of nagios hostgroups."
    ),
    #MEMBERSHIP ORIGIN
    args.add_argument(
        "-o","--origin",
        required=False,
        default=None,
        action="store_true",
        help="Boolean(origin): Determine if hostgroup membership is set at the host or the group level."
    )
    #PARSE ARGS
    meta = args.parse_args()

    #INCLUDED AS A TEST FOR THE NAGIOS CREDS FILE
    #INFO IS USED WITH NAGIOSXI GENERIC API CALLS
    if meta.nsid:
        #GET CREDS FROM YAML
        try:
            crds = xihlpr.creds(meta.nsid)
        except Exception as e:
            print(e)
    
    #GET ALL HOST GROUP DATA
    hgd = xihlpr.nagiosxiGenericAPI("config","hostgroup","None","get",crds["url"],crds["apikey"])
    hgdj = hgd.json()
    
    #COUNT OF HOST MEMBER GROUPS
    gcount = 0
    glist = list()
    #WE GOT GROUPS
    if hgdj:
        
        #DEAL WITH THE SCRIPT INPUT AS A LIST
        #WE ONLY HAVE TO HIT THE API ONCE FOR THE MEMBERLIST
        hl = meta.host.split(",")
        
        for i in hl:
            #START COUNT HERE TO AVOID DUPLICATING THE TOTAL IN THE CASE OF MULTIPLE HOSTS
            tcount = 0
            gcount = 0
            glist.clear()

            #ITERATE THROUGH GROUPS
            for hg in hgdj:

                #INCREMENT TOTAL COUNT
                tcount += 1

                #IF GROUP HAS MEMBERS
                if "members" in hg.keys():
                    
                    #LOOP THROUGH MEMBERS
                    for m in hg["members"]:

                        #FIND THE NEEDLE
                        if m == i:
                            
                            #ADD GROUP TO LIST                    
                            glist.append(hg["hostgroup_name"])
                            nhost = m
                            
                            #INCREMENT COUNT
                            gcount += 1
            
            #GROUP MEMBER LIST IS NOT EMPTY
            if gcount > 0 :
                msg = "{} was found in {} of {} total hostgroups. [{}]".format(i,gcount,tcount,",".join(glist))
                #GET THE ORIGIN
                if meta.origin:
                    #API LIMITED QUERY
                    mod = "host_name={}&filter=active".format(nhost)
                    hconfig = xihlpr.nagiosxiGenericAPI("config","host",mod,"get",crds["url"],crds["apikey"])
                    
                    #THE ENDPOINT RETURNS A LIST SO WE NEED TO DEAL WITH THAT
                    hcfgj = json.dumps(hconfig.json())
                    hj = json.loads(hcfgj)
                    
                    #FIND HOSTGROUPS IS {RESEWNT}
                    for z in hj:
                        
                        if "hostgroups" in z:
                            dcount = 0
                            dhglist = list()
                            
                            #BUILD THE COUNTS AND LIST OF DIRECT GROUPS
                            for g in z["hostgroups"]:
                                dcount += 1
                                dhglist.append(g)
                            
                            #SHOW GROUPS ORIGIN    
                            msg +=" Membership for {} groups is assigned via the {} host object config. [{}]".format(dcount,nhost,",".join(dhglist))

            else:
                msg = "{} not found in {} total hostgroups.".format(i,tcount)
            print(msg)

    #THESE ARE NOT THE DROIDS YOU ARE LOOKING FOR...
    else:
        print("NO HOSTGROUPS FOUND")