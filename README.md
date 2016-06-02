# dcos-ovh-cloud
DC/OS on OVH Cloud Installer

Hacked up script that will spin up a bunch of VMs in the OVH cloud and install DC/OS on them.

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

then run `./dcos_ovhcloud_installer.py`