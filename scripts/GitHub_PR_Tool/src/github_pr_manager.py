import requests


class GitHubPRManager:
    """
    Handles GitHub API operations and pull request
    business logic.
    """

    def __init__(self, token):
        """
        Initialize the GitHub client.

        Args:
            token (str): GitHub personal access token.
        """
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get_pr_details(
        self,
        owner,
        repo,
        pr_number
    ):
        """
        Return formatted pull request details.
        """
        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls/{pr_number}"
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        data = response.json()

        return {
            "number": data["number"],
            "title": data["title"],
            "description": data["body"],
            "author": data["user"]["login"],
            "state": data["state"]
        }

    def get_pr_files(
        self,
        owner,
        repo,
        pr_number
    ):
        """
        Return changed file information.
        """
        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls/{pr_number}/files"
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        files = response.json()

        return [
            {
                "filename": file["filename"],
                "status": file["status"],
                "additions": file["additions"],
                "deletions": file["deletions"]
            }
            for file in files
        ]

    def get_pull_requests(
        self,
        owner,
        repo,
        state="open",
        count=10
    ):
        """
        Return formatted pull request list.
        """
        api_state = state

        if state == "merged":
            api_state = "closed"

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/pulls"
        )

        params = {
            "state": api_state,
            "per_page": count
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        pull_requests = response.json()

        if state == "merged":
            pull_requests = [
                pr
                for pr in pull_requests
                if pr["merged_at"] is not None
            ]

        return [
            {
                "number": pr["number"],
                "title": pr["title"],
                "author": pr["user"]["login"]
            }
            for pr in pull_requests
        ]

    def update_pr_description(
        self,
        owner,
        repo,
        pr_number,
        description
    ):
        """
        Update pull request description.
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

    def parse_pr_description(
        self,
        description
    ):
        """
        Parse PR description and extract values.
        """
        count = 10
        repo_url = None

        for line in description.splitlines():
            line = line.strip()

            if line.startswith("number_of_prs="):
                count = int(
                    line.split("=", 1)[1]
                )

            elif line.startswith("repo_url="):
                repo_url = line.split(
                    "=",
                    1
                )[1]

        return {
            "count": count,
            "repo_url": repo_url
        }

    def parse_repo_url(
        self,
        repo_url
    ):
        """
        Extract owner and repository name
        from repository URL.
        """
        parts = repo_url.rstrip("/").split("/")

        return {
            "owner": parts[-2],
            "repo": parts[-1]
        }