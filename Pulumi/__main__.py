import pulumi
from pulumi_gcp import compute

project = pulumi.Config('gcp').require('project')
region = 'us-central1'
zone = f'{region}-a'


with open('id_rsa.pub') as f:
    ssh_public_key = f.read().strip()


network = compute.Network("custom-network", auto_create_subnetworks=False)
subnetwork = compute.Subnetwork("custom-subnetwork", 
                                network=network.id, 
                                ip_cidr_range="10.0.0.0/24", 
                                region=region)

firewall_ssh = compute.Firewall("allow-ssh", 
                                network=network.id, 
                                allows=[{"protocol": "tcp", "ports": ["22"]}], 
                                source_ranges=["0.0.0.0/0"])

firewall_flask = compute.Firewall("allow-flask", 
                                  network=network.id, 
                                  allows=[{"protocol": "tcp", "ports": ["5000"]}], 
                                  source_ranges=["0.0.0.0/0"])

firewall_mysql = compute.Firewall("allow-mysql", 
                                  network=network.id, 
                                  allows=[{"protocol": "tcp", "ports": ["3306"]}], 
                                  source_ranges=["0.0.0.0/0"])

firewall_jenkins = compute.Firewall("allow-jenkins", 
                                    network=network.id, 
                                    allows=[{"protocol": "tcp", "ports": ["8080", "80"]}], 
                                    source_ranges=["0.0.0.0/0"])

webapp_instance = compute.Instance('webappberk',
                                   machine_type='e2-medium',
                                   zone=zone,
                                   boot_disk={
                                       'initializeParams': {
                                           'image': 'debian-cloud/debian-11'
                                       }
                                   },
                                   metadata={
                                       "ssh-keys": f"root:{ssh_public_key}\nberkekimgcp:{ssh_public_key}"
                                   },
                                   network_interfaces=[{
                                       'network': network.id,
                                       'subnetwork': subnetwork.id,
                                       'accessConfigs': [{}]
                                   }],
                                   allow_stopping_for_update=True,
                                   metadata_startup_script=f"""
                                   #!/bin/bash
                                   useradd -m -s /bin/bash berkekimgcp
                                   mkdir -p /home/berkekimgcp/.ssh
                                   echo '{ssh_public_key}' > /home/berkekimgcp/.ssh/authorized_keys
                                   chown -R berkekimgcp:berkekimgcp /home/berkekimgcp/.ssh
                                   chmod 700 /home/berkekimgcp/.ssh
                                   chmod 600 /home/berkekimgcp/.ssh/authorized_keys
                                   """
                                   )

webapp_instance_load_balancer = compute.Instance('webappberk2',
                                   machine_type='e2-medium',
                                   zone=zone,
                                   boot_disk={
                                       'initializeParams': {
                                           'image': 'debian-cloud/debian-11'
                                       }
                                   },
                                   metadata={
                                       "ssh-keys": f"root:{ssh_public_key}\nberkekimgcp:{ssh_public_key}"
                                   },
                                   network_interfaces=[{
                                       'network': network.id,
                                       'subnetwork': subnetwork.id,
                                       'accessConfigs': [{}]
                                   }],
                                   allow_stopping_for_update=True,
                                   metadata_startup_script=f"""
                                   #!/bin/bash
                                   useradd -m -s /bin/bash berkekimgcp
                                   mkdir -p /home/berkekimgcp/.ssh
                                   echo '{ssh_public_key}' > /home/berkekimgcp/.ssh/authorized_keys
                                   chown -R berkekimgcp:berkekimgcp /home/berkekimgcp/.ssh
                                   chmod 700 /home/berkekimgcp/.ssh
                                   chmod 600 /home/berkekimgcp/.ssh/authorized_keys
                                   """
                                   )
webapp_test_instance = compute.Instance('webappberktest',
                                        machine_type='e2-medium',
                                        zone=zone,
                                        boot_disk={
                                            'initializeParams': {
                                                'image': 'debian-cloud/debian-11'
                                            }
                                        },
                                        metadata={
                                            "ssh-keys": f"root:{ssh_public_key}\nberkekimgcp:{ssh_public_key}"
                                        },
                                        network_interfaces=[{
                                            'network': network.id,
                                            'subnetwork': subnetwork.id,
                                            'accessConfigs': [{}]
                                        }],
                                        allow_stopping_for_update=True,
                                        metadata_startup_script=f"""
                                        #!/bin/bash
                                        useradd -m -s /bin/bash berkekimgcp
                                        mkdir -p /home/berkekimgcp/.ssh
                                        echo '{ssh_public_key}' > /home/berkekimgcp/.ssh/authorized_keys
                                        chown -R berkekimgcp:berkekimgcp /home/berkekimgcp/.ssh
                                        chmod 700 /home/berkekimgcp/.ssh
                                        chmod 600 /home/berkekimgcp/.ssh/authorized_keys
                                        """
                                        )

database_instance = compute.Instance('databaseberk',
                                     machine_type='e2-small',
                                     zone=zone,
                                     boot_disk={
                                         'initializeParams': {
                                             'image': 'debian-cloud/debian-11'
                                         }
                                     },
                                     metadata={
                                         "ssh-keys": f"root:{ssh_public_key}\nberkekimgsp:{ssh_public_key}"
                                     },
                                     network_interfaces=[{
                                         'network': network.id,
                                         'subnetwork': subnetwork.id,
                                         'accessConfigs': [{}]
                                     }],
                                     allow_stopping_for_update=True,
                                     metadata_startup_script=f"""
                                     #!/bin/bash
                                     useradd -m -s /bin/bash berkekimgsp
                                     mkdir -p /home/berkekimgsp/.ssh
                                     echo '{ssh_public_key}' > /home/berkekimgsp/.ssh/authorized_keys
                                     chown -R berkekimgsp:berkekimgsp /home/berkekimgsp/.ssh
                                     chmod 700 /home/berkekimgsp/.ssh
                                     chmod 600 /home/berkekimgsp/.ssh/authorized_keys
                                     """
                                     )

jenkins_instance = compute.Instance('jenkinsberk',
                                    machine_type='e2-small',
                                    zone=zone,
                                    boot_disk={
                                        'initializeParams': {
                                            'image': 'debian-cloud/debian-11'
                                        }
                                    },
                                    metadata={
                                        "ssh-keys": f"root:{ssh_public_key}\nberkekimgcp:{ssh_public_key}"
                                    },
                                    network_interfaces=[{
                                        'network': network.id,
                                        'subnetwork': subnetwork.id,
                                        'accessConfigs': [{}]
                                    }],
                                    allow_stopping_for_update=True,
                                    metadata_startup_script=f"""
                                    #!/bin/bash
                                    useradd -m -s /bin/bash berkekimgcp
                                    mkdir -p /home/berkekimgcp/.ssh
                                    echo '{ssh_public_key}' > /home/berkekimgcp/.ssh/authorized_keys
                                    chown -R berkekimgcp:berkekimgcp /home/berkekimgcp/.ssh
                                    chmod 700 /home/berkekimgcp/.ssh
                                    chmod 600 /home/berkekimgcp/.ssh/authorized_keys
                                    """
                                    )

target_pool = compute.TargetPool("webapp-target-pool",
    region=region,
    instances=[
        webapp_instance.self_link,
        webapp_instance_load_balancer.self_link,
        webapp_test_instance.self_link
    ]
)
target_pool = compute.TargetPool("webapp-target-pool-2",
    region=region,
    instances=[
        webapp_instance.self_link,
        webapp_instance_load_balancer.self_link
    ]
)

health_check = compute.HttpHealthCheck("http-health-check",
    request_path="/",
    port=5000
)
forwarding_rule = compute.ForwardingRule("webapp-forwarding-rule",
    load_balancing_scheme="EXTERNAL",
    target=target_pool.id,
    port_range="5000",
    ip_protocol="TCP",
    region=region,
    ip_address=None  
)



pulumi.export('load_balancer_ip', forwarding_rule.ip_address)
pulumi.export('webappberk_ip', webapp_instance.network_interfaces[0].access_configs[0].nat_ip)
pulumi.export('databaseberk_ip', database_instance.network_interfaces[0].access_configs[0].nat_ip)
pulumi.export('jenkinsberk_ip', jenkins_instance.network_interfaces[0].access_configs[0].nat_ip)
pulumi.export('webappberktest_ip', webapp_test_instance.network_interfaces[0].access_configs[0].nat_ip)
pulumi.export('webappberk_ip_load_balancer2', webapp_instance_load_balancer.network_interfaces[0].access_configs[0].nat_ip)
