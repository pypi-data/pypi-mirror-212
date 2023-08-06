certbot-dns-solidserver
=====================

SOLIDserver DNS Authenticator plugin for Certbot

This plugin automates the process of completing a ``dns-01`` challenge by
creating, and subsequently removing, TXT records using the SOLIDserver REST API.

Configuration of SOLIDserver
---------------------------

In the ``Administration -> Users`` you have to have a user, with the following rights
* DNS zone functions
* DNS record functions


Installation
------------
```
pip install certbot-dns-solidserver
```


Named Arguments
---------------

To start using DNS authentication for solidserver, pass the following arguments on
certbot's command line:

Argument | Description
-|-
``--authenticator dns-solidserver`` | Select the authenticator plugin (Required)
``--dns-solidserver-credentials`` | SOLIDserver REST User credentials INI file. (Default: ``/etc/letsencrypt/solidserver.ini``)
``--dns-solidserver-propagation-seconds`` | Waiting time for DNS to propagate before asking the ACME server to verify the DNS record. (Default: 10)


Credentials
-----------

An example ``solidserver.ini`` file:

    # Sample SOLIDserver INI file
    # Default location /etc/letsencrypt/solidserver.ini
    #
    dns_solidserver_hostname="your.solidserver.host"
    dns_solidserver_username="myremoteuser"
    dns_solidserver_password="verysecureremoteuserpassword"
    dns_solidserver_dnsname="my.dns.server"
    dns_solidserver_viewname="external"

The path to this file can be provided interactively or using the
``--dns-solidserver-credentials`` command-line argument. Certbot
records the path to this file for use during renewal, but does not store the
file's contents.

**CAUTION:** You should protect these API credentials as you would the
password to your solidserver account. Users who can read this file can use these
credentials to issue arbitrary API calls on your behalf. Users who can cause
Certbot to run using these credentials can complete a ``dns-01`` challenge to
acquire new certificates or revoke existing certificates for associated
domains, even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).


Examples
--------

To acquire a single certificate for both ``example.com`` and
``*.example.com``, waiting 900 seconds for DNS propagation:

    certbot certonly \
     --authenticator dns-solidserver \
     --dns-solidserver-credentials /etc/letsencrypt/.secrets/domain.tld.ini \
     --dns-solidserver-propagation-seconds 900 \
     --server https://acme-v02.api.letsencrypt.org/directory \
     --agree-tos \
     --rsa-key-size 4096 \
     -d 'example.com' \
     -d '*.example.com'


Notes
------

This is based on the work in [certbot-dns-ipsconfig](https://github.com/m42e/certbot-dns-ispconfig) and the [eiprest](https://gitlab.com/charlyhong/eiprest)
SOLIDserver REST client python package.
