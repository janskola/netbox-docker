# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

PLUGINS = [
    "netbox_diode_plugin",
    'netbox_dns',
]

PLUGINS_CONFIG = {
    "netbox_diode_plugin": {
        # Address where NetBox can reach Diode inside Docker network or host
#        "diode_target_override": "grpc://docker-host:8096/diode",
        "diode_target_override": "grpcs://diode.domisk.eu/diode",
        "netbox_to_diode_client_secret": "JlLIifqiy4OxsgKXwUXbpRNHRMP6ZOGgaxku6YEUM=",
    }
#    'netbox_dns': {
#        'zone_defaults': {
#            'soa_rname': 'hostmaster.example.com',
#            'soa_mname': 'ns1.example.com',
#        }
#    }
}
