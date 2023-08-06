import fsspec
from .url_parsing import parse_url, to_url
from .file_interface import XetFile
from urllib.parse import urlparse
from .rpyxet import rpyxet
from .commit_transaction import CommitTransaction

import os

_manager = rpyxet.PyRepoManager()


def login(user, token, email=None, host=None):
    """
    Sets the active login credentials used to authenticate against Xethub.
    """
    _manager.override_login_config(user, token, email, host)


def open(file_url, mode="rb", user=None, token=None, **kwargs):
    """
    Open the file at the specific Xet file URL.

    Xet URLs should be of the form `xet://<repo_user>/<repo_name>/<branch>/<path-to-file>`, 
    with the `<path-to-file>' optional if the URL refers to a repository. 
    The xet:// prefix is inferred as needed or if the url is given as https://.  

    Optionally, the user and token can be passed in with the URL by prefixing 
    `xet://<user>[:token]@xethub.com/`.  For example, 
    `xet://user1:mytokenxyz@xethub.com/data_user/data_repo/main/data/survey.csv` would
    access the file `data/survey.csv` on the branch `main` of the repo `data_user/data_repo` 
    with credentials `user=user1` and `token=mytokenxyz`. 

    For example, to open the results.csv file in the main branch of the XetHub Flickr30k repo, 
    the following all work: 

    ```
    f = pyxet.open('xet://xethub.com/XetHub/Flickr30k/main/results.csv')
    f = pyxet.open('/XetHub/Flickr30k/main/results.csv')
    f = pyxet.open('https://xethub.com/XetHub/Flickr30k/main/results.csv'
    ```
    """

    fs = XetFS(file_url, None, user, token)
    return fs._open(file_url, mode=mode, **kwargs)


class XetFS(fsspec.spec.AbstractFileSystem):
    protocol = "xet"  # This allows pandas, etc. to implement "xet://"
    # Whether instances can be recycled; likely possible when we figure out conflicts.

    cachable = False  # We do our own caching.
    sep = "/"
    async_impl = False
    root_marker = "/"

    def __init__(self, domain='xethub.com'):
        """
        Opens the repository at `repo_url` as an fsspec file system handle, providing
        read-only operations such as ls, glob, and open.  

        Xet URLs should be of the form `xet://<repo_user>/<repo_name>/<branch>/`. 
        The xet:// prefix is inferred as needed or if the url is given as https://.  
        If branch is given as an explicit argument, it may be ommitted 
        from the url.  

        User and token are needed for private repositories and they
        can be set with `pyxet.login`.

        Examples: to open the public Flickr30k repository, the following all work:

        ```
        import pyxet
        fs = pyxet.XetFS()

        # List files.
        fs.ls('XetHub/Flickr30k/main')

        # Read the first 5 lines of a file
        b = fs.open('XetHub/Flickr30k/main/results.csv').read()
        ```

        """
        self.domain = domain

        # Init the base class.
        super().__init__()

    @classmethod
    def _strip_protocol(cls, path):
        """Turn path from fully-qualified to file-system-specific
        May require FS-specific handling, e.g., for relative paths or links.
        """

        if isinstance(path, list):
            return [cls._strip_protocol(p) for p in path]

        if path.startswith('xet://'):
            protostripped = path[5:]
        elif path.startswith('https://'):
            protostripped = path[8:]
        else:
            protostripped = path
        return protostripped.lstrip('/')

    def unstrip_protocol(self, name):
        """Format FS-specific path to generic, including protocol"""
        return 'xet://' + name.lstrip('/')

    @staticmethod
    def _get_kwargs_from_urls(path):
        """If kwargs can be encoded in the paths, extract them here
        This should happen before instantiation of the class; incoming paths
        then should be amended to strip the options in methods.
        Examples may look like an sftp path "sftp://user@host:/my/path", where
        the user and host should become kwargs and later get stripped.
        """
        return {}


    def info(self, url):
        # try to parse this as a URL
        # and if not try to parse it as a path
        url_path = parse_url(url, self.domain)
        attr = _manager.stat(url_path.remote, url_path.branch, url_path.path)
        if attr is None:
            raise FileNotFoundError(url)
        return {"name": to_url(url_path), "size": attr.size, "type": attr.ftype}

    def ls(self, path, detail=True, **kwargs):
        """List objects at path.
        This should include subdirectories and files at that location. The
        difference between a file and a directory must be clear when details
        are requested.
        The specific keys, or perhaps a FileInfo class, or similar, is TBD,
        but must be consistent across implementations.
        Must include:
        - full path to the entry (without protocol)
        - size of the entry, in bytes. If the value cannot be determined, will
          be ``None``.
        - type of entry, "file", "directory" or other
        Additional information
        may be present, appropriate to the file-system, e.g., generation,
        checksum, etc.
        May use refresh=True|False to allow use of self._ls_from_cache to
        check for a saved listing and avoid calling the backend. This would be
        common where listing may be expensive.
        Parameters
        ----------
        path: str
        detail: bool
            if True, gives a list of dictionaries, where each is the same as
            the result of ``info(path)``. If False, gives a list of paths
            (str).
        kwargs: may have additional backend-specific options, such as version
            information
        Returns
        -------
        List of strings if detail is False, or list of directory information
        dicts if detail is True.  These dicts would have: name (full path in the FS), 
        size (in bytes), type (file, directory, or something else) and other FS-specific keys.
        """
        # try to parse this as a URL
        # and if not try to parse it as a path
        url_path = parse_url(path, self.domain)
        if url_path.branch == '':
            raise ValueError('Incomplete path. must be of the form user/repo/branch/[path]')

        parse = urlparse(url_path.remote)
        path = parse.path
        components = path.lstrip('/').rstrip('/').split('/')
        if len(components) < 2:
            raise ValueError("URL not in recognized format.")
        prefix = '/'.join(components[:2]) + '/' + url_path.branch

        files, file_info = _manager.listdir(url_path.remote, url_path.branch, url_path.path)

        if detail:
            return [{"name": prefix + '/' + fname, "size": finfo.size, "type": finfo.ftype}
                    for fname, finfo in zip(files, file_info)]
        else:
            return files

    def _open(
        self,
        path,
        mode="rb",
        **kwargs,
    ):
        """
        Return raw bytes-mode file-like from the file-system.

        Reads can be performed from any where, but writes must be performed
        within the context of a transaction which must be scoped to within a
        single repository branch.
        """

        url_path = parse_url(path, self.domain)

        transaction = getattr(self, "_transaction", None)

        if transaction is None and not mode.startswith('r'):
            raise RuntimeError(
                "Write access to files is only allowed within a commit transaction.")

        if not mode.startswith('r'):
            if not self._intrans:
                raise RuntimeError("Write only allowed in the context of a commit transaction."
                                   "Use `with fs.commit(...):` to enable write access.")

        if mode.startswith('r'):
            repo_handle = _manager.get_repo(url_path.remote)
            branch = url_path.branch
            handle = repo_handle.open_for_read(branch, url_path.path)
            return XetFile(handle)
        elif mode.startswith('w'):
            if transaction.repo_info.remote != url_path.remote:
                raise ValueError("Cannot write to different repositories in the same transaction")
            if transaction.repo_info.branch != url_path.branch:
                raise ValueError("Cannot write to different branches in the same transaction")
            transaction.check_transaction_limit()
            handle = self._transaction._transaction_handler.open_for_write(url_path.path)
            return XetFile(handle)
        else:
            raise ValueError("Mode '%s' not supported.", mode)

    def rm(self, path):
        """
        Delete a file.

        Deletions must be performed within the context of a transaction which must
        be scoped to within a single repository branch.
        """
        transaction = getattr(self, "_transaction", None)

        if transaction is None:
            raise RuntimeError(
                "Write access to files is only allowed within a commit transaction.")
        path = parse_url(path, self.domain)
        if transaction.repo_info.remote != path.remote:
            raise ValueError("Cannot write to different repositories in the same transaction")
        if transaction.repo_info.branch != path.branch:
            raise ValueError("Cannot write to different branches in the same transaction")
        transaction.rm(path)


    def cp_file(self, path1, path2):
        """
        Copies a file from path1 to path2.

        Copies must be performed within the context of a transaction which must
        be scoped to within a single repository branch.
        """
        transaction = getattr(self, "_transaction", None)

        if transaction is None:
            raise RuntimeError(
                "Write access to files is only allowed within a commit transaction.")
        parsed_path1 = parse_url(path1, self.domain)
        parsed_path2 = parse_url(path2, self.domain)
        if parsed_path1.remote != parsed_path2.remote:
            raise NotImplementedError("Direct Copy across repositories is not implemented yet")
        if transaction.repo_info.remote != parsed_path2.remote:
            raise ValueError("Cannot write to different repositories in the same transaction")
        if transaction.repo_info.branch != parsed_path2.branch:
            raise ValueError("Cannot write to different branches in the same transaction")
        # no op on directories
        if self.isdir(path1):
            return
        transaction.copy(parsed_path1, parsed_path2)


    @property
    def transaction(self):
        """
        Begin a transaction context for a given repository and branch.
        The entire transaction is committed atomically at the end of the 
        transaction. All writes must be performed into this branch.

        ```
        with fs.transaction('user/repo/branch', 'optional commit message'):
            file = fs.open('user/repo/main/hello.txt','w')
            file.write('hello world')
            file.close()
        """
        if self._transaction is None:
            return lambda *args, **kwargs: self.start_transaction(*args, **kwargs)
        return self._transaction

    def _create_transaction_handler(self, repo_info):
        repo_handle = _manager.get_repo(repo_info.remote)
        return repo_handle.begin_write_transaction(repo_info.branch)

    def start_transaction(self, repo_and_branch, commit_message=None):
        """
        Begin a write transaction for a repository and branch.
        The entire transaction is committed atomically at the end of the 
        transaction. All writes must be performed into this branch

        repo_and_branch is of the form 'user/repo/branch' or 'xet://user/repo/branch'
        ```
        fs.start_transaction('user/repo/branch', 'my commit message')
        file = fs.open('user/repo/main/hello.txt','w')
        file.write('hello world')
        file.close()
        fs.end_transaction()
        ```
        """

        if self._intrans:
            raise RuntimeError("Commit transaction already in progress.")

        self._intrans = True
        url_path = parse_url(repo_and_branch, self.domain)
        if url_path.remote == '':
            raise ValueError("No repository specified")
        if url_path.branch == '':
            raise ValueError("No branch specified")
        if url_path.path != '':
            raise ValueError("No path should be specified")
        self._transaction = CommitTransaction(self, url_path, commit_message)

        return self.transaction

    def cancel_transaction(self):
        """Cancels any active transactions"""
        self._transaction.complete(False)
        self._transaction = None
        self._intrans = False

    def end_transaction(self):
        """Finish write transaction, non-context version"""
        self._transaction.complete()
        self._transaction = None
        self._intrans = False


fsspec.register_implementation("xet", XetFS, clobber=True)
