# Lite Monitoring System

A lightweight monitoring system for checking the availability of hosts, services, and websites, designed for quick deployment and setup with a focus on Telegram notifications.

This system consists of a service developed in Python 3.9.

The service includes the following monitoring modules:
- **URL Module**: Checks the availability of resources via HTTP/S protocol.
- **BURL Module**: Essentially an analogue of the URL module, but with the ability to check the received content.
- **SIP Module**: Checks the availability of the Asterisk telephony server by sending an OPTIONS request.
- **MONGO Module**: Checks the availability of the primary Mongo database, as well as tests for searching, writing, and deleting collections.
- **SOCKET Module**: Checks the availability of network services on the host or the host itself.

The service can be deployed on hosts in different subnets to monitor the target object from various points within the local network.
