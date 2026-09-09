import requests


class GitHubClient:
    """
    Handles GitHub REST API operations such as
    retrieving pull request details, fetching
    changed files, updating pull request
    descriptions, and listing pull requests.
    """

    def __init__(self, token):
        """
        Initialize the GitHub client.

        Args:
            token (str): GitHub personal access token.
        """

        self.token = token

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get_pr(self, owner, repo, pr_number):
        """
        Fetch pull request details.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            pr_number (int): Pull request number.

        Returns:
            dict: Pull request details.
        """

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls/{pr_number}"
        )

        print(url)

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        return response.json()

    def get_pr_files(
        self,
        owner,
        repo,
        pr_number
    ):
        """
        Fetch files changed in a pull request.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            pr_number (int): Pull request number.

        Returns:
            list: Changed file details.
        """

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls/{pr_number}/files"
        )

        print(url)

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        return response.json()

    def update_pr_description(
        self,
        owner,
        repo,
        pr_number,
        description
    ):
        """
        Update pull request description.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            pr_number (int): Pull request number.
            description (str): Updated description.

        Returns:
            dict: Updated pull request information.
        """

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls/{pr_number}"
        )

        payload = {
            "body": description
        }

        response = requests.patch(
            url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        return response.json()

    def get_pull_requests(
        self,
        owner,
        repo,
        state="open",
        count=10
    ):
        """
        Fetch pull requests from a repository.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            state (str): Pull request state.
            count (int): Number of pull requests.

        Returns:
            list: Pull request data.
        """

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls"
        )

        params = {
            "state": state,
            "per_page": count
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        return response.json()