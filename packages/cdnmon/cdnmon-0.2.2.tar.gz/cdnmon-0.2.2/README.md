## Introduction

This project provides IP range data of multiple CDN vendors via a Python package named `cdnmon`.

## Installation

```
pip install -i https://pypi.org/simple/ cdnmon
```

## Usage

### List all supported CDNs

```python
import cdnmon

endpoint = cdnmon.Endpoint(access_token="")
cdns = endpoint.list_cdns()
```

### Find a CDN

```python
import cdnmon

endpoint = cdnmon.Endpoint(access_token="")
cdn = endpoint.find_cdn(name="cloudflare")
print(cdn)
```

### Get the IP ranges of a specific CDN

```python
import cdnmon

endpoint = cdnmon.Endpoint(access_token="")
cdn = endpoint.find_cdn(name="cloudflare")
latest_ipv4_networks = cdn.ipv4_networks[-1]
for latest_ipv4_network in cdn.latest_ipv4_networks:
    print(latest_ipv4_network.networks)
    print(latest_ipv4_network.updated_at)
    print(latest_ipv4_network.source)
```

## FAQ

### How to obtain an access token?

Please contact <wangyihanger@gmail.com>.
