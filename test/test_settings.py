from unittest import TestCase, skip
import subprocess

import boto3


class TestSettings(TestCase):
    @skip('Use in future ')
    def test_module_installed(self):
        self.assertEqual(subprocess.call('python -m aws_bkp_rest'), 0)

    def test_aws_cli_installed(self):
        self.assertEqual(subprocess.call('aws --version ', shell=True), 0, msg='Please install awscli firts')

    def test_list_bucket(self):
        client = boto3.client('s3')
        self.assertIsInstance(client.list_buckets(), dict)
