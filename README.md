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
$ ./dcos_ovhcloud_installer.py --project SomeOVHCloudProject --ssh-key "SomeOVHCloudKey" --masters 3 --agents 10 --pub-agents 2 --url https://downloads.dcos.io/dcos/stable/dcos_generate_config.sh
```

## DC/OS Quick Start
If you're interested in DC/OS independent of the OVH cloud check out [the DC/OS Quick Start](https://github.com/lloesche/dcos-ovh-cloud/blob/master/dcos-quickstart.md).
