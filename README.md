# [DC/OS](https://dcos.io/) on [OVH Cloud](https://www.ovh.com/us/cloud/) Installer
Script that will spin up a bunch of VMs in the OVH cloud and install DC/OS on them.

## Setup
Configure your ~/.ovh.conf to contain proper credentials


```
$ cat ~/.ovh.conf
[default]
endpoint=ovh-ca

[ovh-ca]
application_key=AfgQ7aQjg1337wIl
application_secret=eEHookeEAqPTTxqPexLvKwotiTr3i2cU
consumer_key=4DxaEjBLbYm0nK3yjyFmpmscsjK4byja
```

install Python 3 and required Python modules (`pip install -r requirements.txt`) then run `./dcos_ovhcloud_installer.py --help` and set appropriate options.


##Example
```
$ ./dcos_ovhcloud_installer.py --project SomeOVHCloudProject \
                               --ssh-key "SomeOVHCloudKey" \
                               --masters 3 \
                               --agents 10 \
                               --pub-agents 2 \
                               --url https://downloads.dcos.io/dcos/stable/dcos_generate_config.sh
```

I mainly use this tool for development and quick testing where I spin up a cluster, run some tests and then tear it down. So the default behaviour is to delete the cluster when the script exits. You can override this behaviour using the `--no-cleanup` flag.

## DC/OS Quick Start
If you're interested in DC/OS independent of the OVH Cloud check [the DC/OS Quick Start](https://github.com/lloesche/dcos-ovh-cloud/blob/master/dcos-quickstart.md). The steps described in there are what this Installer runs after initializing the OVH Cloud VMs.
