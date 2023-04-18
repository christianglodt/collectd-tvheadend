#!/usr/bin/env python3

import urllib
import urllib.request
import json
import collectd

base_url = 'http://localhost:9981'
headers = {}

def config(conf):
    global base_url
    global headers

    for node in conf.children:
        if node.key == 'BaseURL':
            base_url = node.values[0]
        if node.key == 'Header':
            headers[node.values[0]] = node.values[1]

def read(data=None):
    global base_url
    global headers

    req = urllib.request.Request(f'{base_url}/api/status/inputs', headers=headers)
    data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    for entry in data['entries']:
        input = entry['input']
        if entry['signal_scale'] == 1:
            signal_pct = entry['signal'] / 65535.0
            collectd.Values(type='gauge').dispatch(values=[signal_pct], plugin='tvheadend_input', plugin_instance=input, type_instance='signal_pct')

        if entry['signal_scale'] == 2:
            signal_db = entry['signal'] / 1000.0
            collectd.Values(type='gauge').dispatch(values=[signal_db],plugin='tvheadend_input', plugin_instance=input, type_instance='signal_db')

        if entry['snr_scale'] == 1:
            snr_pct = entry['snr'] / 65535.0
            collectd.Values(type='gauge').dispatch(values=[snr_pct], plugin='tvheadend_input', plugin_instance=input, type_instance='snr_pct')

        if entry['snr_scale'] == 2:
            snr_db = entry['snr'] / 1000.0
            collectd.Values(type='gauge').dispatch(values=[snr_db], plugin='tvheadend_input', plugin_instance=input, type_instance='snr_db')

        for var_name in ('ber', 'bps', 'cc', 'ec_bit', 'ec_block', 'subs', 'tc_bit', 'tc_block', 'te', 'unc', 'weight'):
            v = entry.get(var_name, None)
            if v is not None:
                collectd.Values(type='gauge').dispatch(values=[v], plugin='tvheadend_input', plugin_instance=input, type_instance=var_name)

collectd.register_config(config)
collectd.register_read(read)
