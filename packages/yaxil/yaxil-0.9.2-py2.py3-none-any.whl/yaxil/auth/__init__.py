from collections import namedtuple

XnatAuth = namedtuple('XnatAuth', [
    'url',
    'username',
    'password',
    'cookie'
])
'''
Container to hold XNAT authentication information. Fields include the ``url``,
``username``, ``password``, and ``cookie``.
'''

def test_auth(auth):
    '''
    Validate credentials against XNAT

    Example:
        >>> import yaxil
        >>> auth = yaxil.auth('doctest')
        >>> yaxil.test_auth(auth)
        True
    '''
    baseurl = auth.url.rstrip('/')
    url = f'{baseurl}/data/projects'
    r = requests.get(
        url,
        auth=basicauth(auth),
        params={
            'columns': 'ID'
        }
    )
    if r.status_code == requests.codes.UNAUTHORIZED:
        return False
    return True

def auth(alias=None, host=None, username=None, password=None, cfg='~/.xnat_auth'):
    '''
    Create authentication object from an ``xnat_auth`` file, function arguments, 
    or environment variables (``XNAT_HOST``, ``XNAT_USER``, and ``XNAT_PASS``), 
    in that order

    Example:
        >>> import os
        >>> import yaxil.auth as yauth
        >>> os.environ['XNAT_HOST'] = 'https://xnat.example.com'
        >>> os.environ['XNAT_USER'] = 'username'
        >>> os.environ['XNAT_PASS'] = '*****'
        >>> yauth.auth2()
        XnatAuth(url='https://xnat.example.com', username='username', password='*****')
    '''
    result = tuple()
    # First, look for authentication data in ~/.xnat_auth
    if alias:
        logger.debug(f'returning authentication data from {cfg}')
        return _auth(alias)
    # Second, look for authentication data from --host, --user, --password function arguments
    authargs = (host, username)
    if any(authargs):
        if not all(authargs):
            raise AuthError('you must supply --host, --username and --password (or password prompt)')
        logger.debug('returning authentication data from command line')
        if not password:
            password = gp.getpass('Enter XNAT passphrase:')
        obj = XnatAuth(
            url=host,
            username=username,
            password=password,
            cookie=None
        )
        return start_session(obj)
    # Third, look for authentication data in environment variables
    host = os.environ.get('XNAT_HOST', None)
    username = os.environ.get('XNAT_USER', None)
    password = os.environ.get('XNAT_PASS', None)
    authargs = (host, username)
    if any(authargs):
        if not all(authargs):
            raise AuthError('you must set $XNAT_HOST, $XNAT_USER, and $XNAT_PASS (or password prompt)')
        logger.debug('returning authentication data from environment variables')
        if not password:
            password = gp.getpass('Enter XNAT passphrase:')
        obj = XnatAuth(
            url=host,
            username=username,
            password=password,
            cookie=None
        )
        return start_session(obj)
    raise AuthError('you must provide authentication data using xnat_auth, command line, or environment variables')

def _auth(alias=None, url=None, cfg="~/.xnat_auth"):
    '''
    Read connection details from an xnat_auth XML file

    Example:
        >>> import yaxil
        >>> yaxil.auth('doctest')
        XnatAuth(url='...', username='...', password='...')

    :param alias: XNAT alias
    :type alias: str
    :param url: XNAT URL
    :type url: str
    :param cfg: Configuration file
    :type cfg: str
    :returns: Named tuple of (url, username, password)
    :rtype: :mod:`yaxil.XnatAuth`
    '''
    if not alias and not url:
        raise ValueError('you must provide an alias or url argument')
    if alias and url:
        raise ValueError('cannot provide both alias and url arguments')
    # check and parse config file
    cfg = os.path.expanduser(cfg)
    if not os.path.exists(cfg):
        raise AuthError("could not locate auth file %s" % cfg)
    tree = etree.parse(os.path.expanduser(cfg))
    # search by alias or url
    res = None
    if alias:
        res = tree.findall("./%s" % alias)
    if url:
        res = tree.findall("./*/[url='%s']" % url)
    if not res:
        raise AuthError("failed to locate xnat credentials within %s" % cfg)
    elif len(res) > 1:
        raise AuthError("found too many sets of credentials within %s" % cfg)
    res = res.pop()
    # get url
    url = res.findall("url")
    if not url:
        raise AuthError("no url for %s in %s" % (alias, cfg))
    elif len(url) > 1:
        raise AuthError("too many urls for %s in %s" % (alias, cfg))
    # get username
    username = res.findall("username")
    if not username:
        raise AuthError("no username for %s in %s" % (alias, cfg))
    elif len(username) > 1:
        raise AuthError("too many usernames for %s in %s" % (alias, cfg))
    # get password
    password = res.findall("password")
    if not password:
        password = gp.getpass('Enter XNAT passphrase:')
    elif len(password) > 1:
        raise AuthError("too many passwords for %s in %s" % (alias, cfg))
    else:
        password = password.pop().text
    obj = XnatAuth(
        url=url.pop().text,
        username=username.pop().text,
        password=password,
        cookie=None
    )
    return start_session(obj)

