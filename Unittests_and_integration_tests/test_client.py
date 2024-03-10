#!/usr/bin/env python3
""" Unittests for client.py """

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class """
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """ Test org method """
        mock_get_json.return_value = {"name": org_name}
        github_org_client = GithubOrgClient(org_name)
        self.assertEqual(github_org_client.org, {"name": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """ Test _public_repos_url method """
        org_name = "google"
        repo_url = f"https://api.github.com/orgs/{org_name}"
        mock_org.return_value = {"repos_url": repo_url}
        github_org_client = GithubOrgClient(org_name)
        self.assertEqual(github_org_client._public_repos_url, repo_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """ Test public_repos method """
        mock_get_json.return_value = [
            {"name": "google"},
            {"name": "abc"}
        ]
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            github_org_client = GithubOrgClient("google")
            repos = github_org_client.public_repos()
            self.assertEqual(repos, ["google", "abc"])
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ Test has_license method """
        github_org_client = GithubOrgClient("org_name")
        result = github_org_client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ TestIntegrationGithubOrgClient class """
    @classmethod
    def setUpClass(cls):
        """ setUpClass """
        requests_json = unittest.mock.Mock()
        requests_json.json.side_effect = [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]

        cls.get_patcher = patch('requests.get', return_value=requests_json)
        cls.get_patcher.start()

    def test_public_repos(self):
        """ Test public_repos method """
        github_org_client = GithubOrgClient("google")
        repos = github_org_client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """ Test public_repos method with license """
        github_org_client = GithubOrgClient("google")
        repos = github_org_client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """ tearDownClass to stop the patcher """
        cls.get_patcher.stop()
