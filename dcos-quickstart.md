#[Mesosphere DC/OS](https://dcos.io) Quickstart

If you're super eager to get started [jump to TL;DR](#tldr) below!

## Intro
This document assumes you roughly know what DC/OS is and why you want it. If not check out [the Overview on dcos.io](https://dcos.io/docs/1.8/overview/what-is-dcos/)

It documents how to use the DC/OS CLI Installer to perform the installation. This is the easiest way of installing a DC/OS cluster without a GUI. For large installations there's [the Advanced DC/OS Installation Guide](https://dcos.io/docs/1.8/administration/installing/custom/advanced/). 

From a systems perspective you require at least 2 nodes. A master and an agent. The master will schedule the workloads the agent will run it. For a HA setup you require at least 3 master nodes, 5 is better.
DC/OS uses Zookeeper which requires a simple majority to vote a quorum. So in a 3 master cluster 1 node can fail and in a 5 node cluster 2 nodes can fail for the cluster to still be operational.

You can also add public agents which have a special role in DC/OS. They are meant to be exposed to the Internet except for their tcp ports 22 (ssh) and 5051 (mesos-agent).
The idea is that your masters and (private) agents run inside an internal firewalled network. And the public agents while having access to the master IPs are located in a public network.
It is however up to the user to get this network security into place. Either by creating local iptables on all nodes or putting firewalls in front of the nodes. DC/OS itself is currently not firewalling anything though there are plans to do so in the future.  
## Requirements
Things you need:
* A local Linux system with Docker running on it where we download the DC/OS Installer to
* Two or more Linux server where DC/OS is to be installed
* [The DC/OS Installer](https://downloads.dcos.io/dcos/EarlyAccess/dcos_generate_config.sh) in your current directory e.g. `./dcos_generate_config.sh`
* An ip-detect script saved at `./genconf/ip-detect`
* The ssh key to access your nodes saved at `./genconf/ssh_key` (mode 0600)
* The DC/OS Installer config saved at `./genconf/config.yaml`
Note regarding ip-detect script: This is just a script or program various parts of DC/OS will execute on startup. They expect it to print the IP address on stdout DC/OS is supposed bind to. This is mainly used for machines with multiple network interfaces.

I'm usually using the following script which prints the IP of the interface that is connected to the default gateway:
```
#!/usr/bin/env bash
set -o nounset -o errexit -o pipefail
export PATH=/sbin:/usr/sbin:/bin:/usr/bin:$PATH
MASTER_IP=${MASTER_IP:-8.8.8.8}
INTERFACE_IP=$(ip r g ${MASTER_IP} | \
awk -v master_ip=${MASTER_IP} '
BEGIN { ec = 1 }
{
  if($1 == master_ip) {
    print $7
    ec = 0
  } else if($1 == "local") {
    print $6
    ec = 0
  }
  if (ec == 0) exit;
}
END { exit ec }
')
echo $INTERFACE_IP
```
## Setup
1) Download the DC/OS Installer to `./dcos_generate_config.sh`
  * Latest stable (GA) release: `https://downloads.dcos.io/dcos/stable/dcos_generate_config.sh`
  * Latest early access (EA) release `https://downloads.dcos.io/dcos/EarlyAccess/dcos_generate_config.sh`
2) Save the ip-detect script to `./genconf/ip-detect`
3) Save the SSH private key that has access to your nodes to `./genconf/ssh_key` and `chmod 0600 ./genconf/ip-detect`
4) Save the DC/OS Installer config.yaml to `./genconf/config.yaml`

When those four files are in place  you should have a structure like this:
```
./dcos_generate_config.sh
./genconf/ip-detect
./genconf/ssh_key
./genconf/config.yaml
```
## genconf/config.yaml:
####Example
```
master_list:
- 10.0.0.11
- 10.0.0.12
- 10.0.0.13
agent_list:
- 10.0.0.21
- 10.0.0.22
- 10.0.0.23
- 10.0.0.24
- 10.0.0.25
public_agent_list: []
ssh_user: admin
cluster_name: DCOS Test
bootstrap_url: file:///opt/dcos_install_tmp
exhibitor_storage_backend: static
master_discovery: static
process_timeout: 10000
resolvers: [8.8.8.8, 8.8.4.4]
ssh_port: 22
telemetry_enabled: 'false'
```

For a complete list of configuration options see the [Install Configuration Parameters section](https://dcos.io/docs/1.8/administration/installing/custom/configuration-parameters/) of the DC/OS documentation.

The interesting ones for this Quickstart are:
* `master_list`: List of Master IPs
* `agent_list`: List of Agent IPs (optionally `public_agent_list` is the list of Public Agents)
* `ssh_user`: Admin user that can ssh into the nodes using the key in `genconf/ssh_key` and run sudo'ed commands.

## Installation
```
$ ./dcos_generate_config.sh --genconf         && \
  ./dcos_generate_config.sh --install-prereqs && \
  ./dcos_generate_config.sh --preflight       && \
  ./dcos_generate_config.sh --deploy          && \
  ./dcos_generate_config.sh --postflight
```

Quick explanation of the steps:
* `--genconf` Extracts the Docker install container and validates the configuration you previously created
* `--install-prereqs` SSH'es into the nodes and installs some prerequisits like Docker
* `--preflight` Checks your nodes are ready for installation
* `--deploy` Actually installs DC/OS
* `--postflight` Makes sure DC/OS was installed successfully

That's it. If everything went well you'll be able to log into DC/OS using http on any of the master IPs.

## TL;DR
At the very least replace `master_list`, `agent_list` and `ssh_user`.
```
mkdir genconf
cp ~/.ssh/id_rsa genconf/ssh_key && \
chmod 600 genconf/ssh_key

cat << EOF > genconf/ip-detect
#!/usr/bin/env bash
set -o nounset -o errexit -o pipefail
export PATH=/sbin:/usr/sbin:/bin:/usr/bin:\$PATH
MASTER_IP=\${MASTER_IP:-8.8.8.8}
INTERFACE_IP=\$(ip r g \${MASTER_IP} | \
awk -v master_ip=\${MASTER_IP} '
BEGIN { ec = 1 }
{
  if(\$1 == master_ip) {
    print \$7
    ec = 0
  } else if(\$1 == "local") {
    print \$6
    ec = 0
  }
  if (ec == 0) exit;
}
END { exit ec }
')
echo \$INTERFACE_IP
EOF

cat << EOF > genconf/config.yaml
master_list:
- 10.0.0.11
agent_list:
- 10.0.0.21
- 10.0.0.22
public_agent_list: []
ssh_user: admin
cluster_name: DCOS Test
bootstrap_url: file:///opt/dcos_install_tmp
exhibitor_storage_backend: static
master_discovery: static
process_timeout: 10000
resolvers: [8.8.8.8, 8.8.4.4]
ssh_port: 22
telemetry_enabled: 'false'
EOF

curl -o dcos_generate_config.sh https://downloads.dcos.io/dcos/EarlyAccess/dcos_generate_config.sh
chmod +x dcos_generate_config.sh

./dcos_generate_config.sh --genconf         && \
./dcos_generate_config.sh --install-prereqs && \
./dcos_generate_config.sh --preflight       && \
./dcos_generate_config.sh --deploy          && \
./dcos_generate_config.sh --postflight
```
