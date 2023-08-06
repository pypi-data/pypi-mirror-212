"""
Provides URL parsing for Xet Repos
"""
from collections import namedtuple
from urllib.parse import urlparse, quote
import unittest


XetPathInfo = namedtuple('XetPathInfo', ('remote', 'branch', 'path'))


def to_url(path_info):
    assert(isinstance(path_info, XetPathInfo))
    parse = urlparse(path_info.remote)
    p = path_info.path
    if p.endswith('/'):
        p = p[:-1]
    if p.startswith('/'):
        p = p[1:]
    if len(p) == 0:
        return parse._replace(path=f"{path_info.branch}").geturl()
    else:
        return parse._replace(path=f"{path_info.branch}/{p}").geturl()




def parse_url(url, force_domain='xethub.com'):
    """
    Parses a Xet URL of the form 
     - xet://user/repo/branch/[path]
     - /user/repo/branch/[path]

    Into a XetPathInfo which forms it as remote=https://[domain]/user/repo
    branch=[branch] and path=[path].
    """
    url = url.lstrip('/')
    parse = urlparse(url)
    if parse.scheme == '':
        parse=parse._replace(scheme='xet')

    if parse.scheme != 'xet':
        raise ValueError('Invalid protocol')

    # Handle the case where we are xet://user/repo. In which case the domain
    # parsed is not xethub.com and domain="user".
    # we rewrite the parse the handle this case early.
    if parse.netloc != force_domain:
        if parse.netloc == 'xethub.com':
            parse = parse._replace(netloc=force_domain)
        else:
            # this is of the for xet://user/repo/...
            # join user back with path
            newpath = f"/{parse.netloc}{parse.path}"
            # replace the netloc
            true_netloc = force_domain 
            parse = parse._replace(netloc=true_netloc, path=newpath)

    # Split the known path and try to split out the user/repo/branch/path components
    path = parse.path
    components = path.split('/')
    # path always begin with a '/', so 1st component is always empty
    # so the minimum for a remote is xethub.com/user/repo
    if len(components) < 3:
        raise ValueError("URL not in recognized format.")

    branch = ""
    if len(components) >= 4:
        branch = components[3]

    path = "" 
    if len(components) >= 5:
        path = '/'.join(components[4:])

    # we leave url with the first 3 components. i.e. "/user/repo"
    replacement_parse_path = '/'.join(components[:3])
    parse = parse._replace(path=replacement_parse_path, scheme="https")


    return XetPathInfo(parse.geturl(), branch, path)


class ParseUrlTest(unittest.TestCase):
    def test_parse_xet_url(self):
        parse = parse_url("xet://xethub.com/user/repo/branch/hello/world")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "hello/world")

        parse = parse_url("xet://xethub.com/user/repo/branch/hello/world/")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "hello/world/")

        parse = parse_url("xet://xethub.com/user/repo/branch/")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        parse = parse_url("xet://xethub.com/user/repo/branch")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        parse = parse_url("xet://xethub.com/user/repo")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "")
        self.assertEqual(parse.path, "")

        parse = parse_url("xet://xethub.com/user/repo/branch", force_domain='xetbeta.com')
        self.assertEqual(parse.remote, "https://xetbeta.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        with self.assertRaises(ValueError):
            self.parse = parse_url("xet://xethub.com/user")

    def test_parse_xet_url_truncated(self):
        parse = parse_url("xet://user/repo/branch/hello/world")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "hello/world")

        parse = parse_url("xet://user/repo/branch/hello/world/")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "hello/world/")

        parse = parse_url("xet://user/repo/branch/")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        parse = parse_url("xet://user/repo/branch")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        parse = parse_url("xet://user/repo")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "")
        self.assertEqual(parse.path, "")

        parse = parse_url("xet://user/repo/branch", force_domain='xetbeta.com')
        self.assertEqual(parse.remote, "https://xetbeta.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        with self.assertRaises(ValueError):
            self.parse = parse_url("xet://user")


    def test_parse_plain_path(self):
        parse = parse_url("/user/repo/branch/hello/world")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "hello/world")

        parse = parse_url("/user/repo/branch/hello/world/")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "hello/world/")

        parse = parse_url("/user/repo/branch/")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        parse = parse_url("/user/repo/branch")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        parse = parse_url("/user/repo")
        self.assertEqual(parse.remote, "https://xethub.com/user/repo")
        self.assertEqual(parse.branch, "")
        self.assertEqual(parse.path, "")

        parse = parse_url("/user/repo/branch", force_domain='xetbeta.com')
        self.assertEqual(parse.remote, "https://xetbeta.com/user/repo")
        self.assertEqual(parse.branch, "branch")
        self.assertEqual(parse.path, "")

        with self.assertRaises(ValueError):
            self.parse = parse_url("xet://xethub.com/user")


