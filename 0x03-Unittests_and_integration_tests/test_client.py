#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test_org/repos"
            }
            self.assertEqual(
                client._public_repos_url, "https://api.github.com/orgs/test_org/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        client = GithubOrgClient("test_org")
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=property
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://fakeurl.com"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fakeurl.com")

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    [
        {
            "org_payload": fixtures.org_payload,
            "repos_payload": fixtures.repos_payload,
            "expected_repos": fixtures.expected_repos,
            "apache2_repos": fixtures.apache2_repos,
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
