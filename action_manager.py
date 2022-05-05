from contextlib import contextmanager
import os
import re
import paramiko
import time


class SshClient:
    """A wrapper of paramiko.SSHClient"""
    TIMEOUT = 10

    def __init__(self, connection_string, **kwargs):
        self.key = kwargs.pop("key", None)
        self.client = kwargs.pop("client", None)
        self.connection_string = connection_string
        try:
            self.username, self.password, self.host = re.search("(\w+):(\w+)@(.*)", connection_string).groups()
        except (TypeError, ValueError):
            raise Exception("Invalid connection sting should be 'user:pass@ip'")
        try:
            self.host, self.port = self.host.split(":", 1)
        except (TypeError, ValueError):
            self.port = "22"
        self.connect(self.host, int(self.port), self.username, self.password, self.key)

    def reconnect(self):
        self.connect(self.host, int(self.port), self.username, self.password, self.key)

    def connect(self, host, port, username, password, key=None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False, **kwargs):
        should_close = False
        if not self.is_connected():
            self.reconnect()
            should_close = True
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command, **kwargs)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()

        result = {'out': stdout.readlines(),
                  'err': stderr.readlines(),
                  'retval': stdout.channel.recv_exit_status()}
        if should_close:
            self.close()
        return result

    @contextmanager
    def _get_sftp(self):
        yield paramiko.SFTPClient.from_transport(self.client.get_transport())

    def put_in_dir(self, src, dst):
        if not isinstance(src, (list, tuple)):
            src = [src]
        print(self.execute('''python -c "import os;os.makedirs('%s')"''' % dst))
        with self._get_sftp() as sftp:
            for s in src:
                sftp.put(s, dst + os.path.basename(s))

    def get(self, src, dst):
        with self._get_sftp() as sftp:
            sftp.get(src, dst)

    def rm(self, *remote_paths):
        for p in remote_paths:
            self.execute("rm -rf {0}".format(p), sudo=True)

    def mkdir(self, dirname):
        print(self.execute("mkdir {0}".format(dirname)))

    def remote_open(self, remote_file_path, open_mode):
        with self._get_sftp() as sftp:
            return sftp.open(remote_file_path, open_mode)

    def is_connected(self):
        transport = self.client.get_transport() if self.client else None
        return transport and transport.is_active()
