import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

HERE = os.path.dirname(os.path.abspath(__file__))

### Why are so many lines commented?
# Currently jupyter-server-proxy does not support url-parameters, yet.
# A pull request is waiting to be merged: https://github.com/jupyterhub/jupyter-server-proxy/pull/226
# Be aware! Until then, we need to comment the support for password and encryption.

# def _xprahtml5_urlparams():
#    from getpass import getuser
#
#    url_params = '?' + '&'.join([
#        'username=' + getuser(),
#        'password=' + _xprahtml5_passwd,
#        'encryption=AES',
#        'key=' + _xprahtml5_aeskey,
#        'sharing=true',
#    ])
#
#    return url_params


def _xprahtml5_mappath(path):

#    # always pass the url parameter
    if path in ('/', '/index.html', ):
#        url_params = _xprahtml5_urlparams()
        path = '/index.html'  # + url_params

    return path


def setup_xprahtml5():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """
    from pathlib import Path
    from tempfile import gettempdir, mkstemp
#    from random import choice
#    from string import ascii_letters, digits

    global _xprahtml5_passwd, _xprahtml5_aeskey

#    # password generator
#    def _get_random_alphanumeric_string(length):
#        letters_and_digits = ascii_letters + digits
#        return (''.join((choice(letters_and_digits) for i in range(length))))
#
    # ensure a known secure sockets directory exists, as /run/user/$UID might not be available
    socket_path = os.path.join(gettempdir(), 'xpra_sockets_' + str(os.getuid()))
    Path(socket_path).mkdir(mode=0o700, parents=True, exist_ok=True)
    logger.info('Created secure socket directory for Xpra: ' + socket_path)

#    # generate file with random one-time-password
#    _xprahtml5_passwd = _get_random_alphanumeric_string(16)
#    try:
#        fd_passwd, fpath_passwd = mkstemp()
#        logger.info('Created secure password file for Xpra: ' + fpath_passwd)
#
#        with open(fd_passwd, 'w') as f:
#            f.write(_xprahtml5_passwd)
#
#    except Exception:
#        logger.error("Passwd generation in temp file FAILED")
#        raise FileNotFoundError("Passwd generation in temp file FAILED")
#
#    # generate file with random encryption key
#    _xprahtml5_aeskey = _get_random_alphanumeric_string(16)
#    try:
#        fd_aeskey, fpath_aeskey = mkstemp()
#        logger.info('Created secure encryption key file for Xpra: ' + fpath_aeskey)
#
#        with open(fd_aeskey, 'w') as f:
#            f.write(_xprahtml5_aeskey)
#
#    except Exception:
#        logger.error("Encryption key generation in temp file FAILED")
#        raise FileNotFoundError("Encryption key generation in temp file FAILED")
#
#    # launchers url file including url parameters
#    urlfile = 'index.html' + _xprahtml5_urlparams()

    # create command
    cmd = [
        os.path.join(HERE, 'share/launch_xpra.sh'),
        'start',
        '--html=on',
        '--bind-tcp=0.0.0.0:{port}',
        # '--socket-dir="' + socket_path + '/"',  # fixme: socket_dir not recognized
        # '--server-idle-timeout=86400',  # stop server after 24h with no client connection
        # '--exit-with-client=yes',  # stop Xpra when the browser disconnects
        '--start=xterm -fa Monospace',
        # '--start=xfce4-session',
        # '--start-child=xterm', '--exit-with-children',
#        '--tcp-auth=file:filename=' + fpath_passwd,
#        '--tcp-encryption=AES',
#        '--tcp-encryption-keyfile=' + fpath_aeskey,
        '--clipboard-direction=both',
        '--no-mdns',  # do not advertise the xpra session on the local network
        '--no-bell',
        '--no-speaker',
        '--no-printing',
        '--no-microphone',
        '--no-notifications',
        '--no-systemd-run',  # do not delegated start-cmd to the system wide proxy server instance
        # '--dpi=96',  # only needed if Xserver does not support dynamic dpi change
#        '--sharing',  # this allows to open the desktop in multiple browsers at the same time
        '--no-daemon',  # mandatory
    ]
    logger.info('Xpra command: ' + ' '.join(cmd))

    return {
        'environment': {  # as '--socket-dir' does not work as expected, we set this
            'XDG_RUNTIME_DIR': socket_path,
        },
        'command': cmd,
        'mappath': _xprahtml5_mappath,
        'absolute_url': False,
        'timeout': 90,
        'new_browser_tab': True,
        'launcher_entry': {
            'enabled': True,
            'icon_path': os.path.join(HERE, 'share/xpra-logo.svg'),
            'title': 'Xpra Desktop',
#            'urlfile': urlfile,
        },
    }
