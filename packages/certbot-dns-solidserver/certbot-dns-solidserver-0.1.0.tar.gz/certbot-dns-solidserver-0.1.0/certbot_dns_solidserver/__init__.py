"""
The `~certbot_dns_solidserver.dns_solidserver` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the SOLIDserver REST API.

Named Arguments
---------------
==========================================  =====================================
``--dns-solidserver-credentials``           SOLIDserver REST API credentials
                                            INI file. (Default:
                                            /etc/letsencrypt/solidserver.ini)
``--dns-solidserver-propagation-seconds``   The number of seconds to wait for DNS
                                            to propagate before asking the ACME
                                            server to verify the DNS record.
                                            (Default: 60)
==========================================  =====================================

Credentials
-----------
Use of this plugin requires a configuration file containing SOLIDserver REST API 
credentials.

.. code-block:: ini
   :name: solidserver.ini
   :caption: Example credentials file:
   # SOLIDSERVER API credentials used by Certbot
   dns_solidserver_hostname = "solidserver.example.org:443"
   dns_solidserver_username = "myapiuser"
   dns_solidserver_password = "mysecretpassword"
   dns_solidserver_dnsname = "smart.dns"
   dns_solidserver_viewname = "external"

The path to this file can be provided interactively or using the
``--dns-solidserver-credentials`` command-line argument. Certbot records the path
to this file for use during renewal, but does not store the file's contents.

.. caution::
   You should protect these API credentials as you would a password. Users who
   can read this file can use these credentials to issue arbitrary API calls on
   your behalf. Users who can cause Certbot to run using these credentials can
   complete a ``dns-01`` challenge to acquire new certificates or revoke
   existing certificates for associated domains, even if those domains aren't
   being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).
"""