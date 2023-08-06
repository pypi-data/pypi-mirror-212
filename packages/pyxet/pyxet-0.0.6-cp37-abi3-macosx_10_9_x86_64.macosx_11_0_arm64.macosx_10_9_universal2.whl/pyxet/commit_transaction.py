import fsspec

TRANSACTION_LIMIT=2048

class CommitTransaction(fsspec.transaction.Transaction):
    """
    Handles a commit using the transaction interface. A transaction can only
    be performed within the context of a single repository and branch.

    There is a transaction limit of 2048 entries. If the number of changes 
    exceed this limit, an automatic commit will be performed.
    """

    def __init__(self, fs, repo_info, commit_message=None):
        if commit_message is None:
            import datetime
            commit_message = "Commit " + datetime.datetime.now().isoformat()

        self.commit_message = commit_message
        self._transaction_handler = fs._create_transaction_handler(repo_info)
        self.fs = fs
        self.repo_info = repo_info

        super().__init__(fs)

    def __repr__(self):
        return f"Transaction for {self.repo_info}"

    def __str__(self):
        return f"Transaction for {self.repo_info}"

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End transaction and commit, if exit is not due to exception"""
        # only commit if there was no exception
        self.complete(commit=exc_type is None)
        self.fs._intrans = False
        self.fs._transaction = None

    def start(self):
        self.fs._intrans = True

    def complete(self, commit=True):
        if commit:
            self._transaction_handler.commit(self.commit_message)
        else:
            self._transaction_handler.cancel()
        self._transaction_handler = None
        self.fs._intrans = False
        self.fs._transaction = None

    def check_transaction_limit(self):
        if self._transaction_handler.transaction_size() >= TRANSACTION_LIMIT:
            import sys
            sys.stderr.write("Transaction limit has been reached. Forcing a commit.\n")
            sys.stderr.flush()
            self._transaction_handler.commit(self.commit_message)
            self._transaction_handler = self.fs._create_transaction_handler(self.repo_info)

    def copy(self, src_repo_info, dest_repo_info):
        assert(src_repo_info.remote == dest_repo_info.remote)
        assert(dest_repo_info.remote == self.repo_info.remote)
        assert(dest_repo_info.branch == self.repo_info.branch)
        self.check_transaction_limit()
        self._transaction_handler.copy(src_repo_info.branch, src_repo_info.path, dest_repo_info.path)

    def rm(self, repo_info):
        assert(repo_info.remote == self.repo_info.remote)
        assert(repo_info.branch == self.repo_info.branch)
        self.check_transaction_limit()
        self._transaction_handler.delete(repo_info.path)
