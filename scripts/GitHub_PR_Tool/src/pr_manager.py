from itertools import count


class PRManager:
    """Handles pull request operations and business logic."""

    def __init__(self, github_client):
        """ Initialize the pull request manager.
        Args:
            github_client (GitHubClient):
                GitHub API client instance.
        """
        self.github_client = github_client

    def get_pr_details(
        self,
        owner,
        repo,
        pr_number
    ):
        """
        Return formatted pull request details.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            pr_number (int): Pull request number.

        Returns:
            dict: Formatted pull request details.
        """

        data = self.github_client.get_pr(
            owner,
            repo,
            pr_number
        )
        
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
        Return changed file information for a pull request.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            pr_number (int): Pull request number.

        Returns:
            list: Changed file details.
        """


        files = self.github_client.get_pr_files(
            owner,
            repo,
            pr_number
        )

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

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            state (str): Pull request state.
            count (int): Number of pull requests.

        Returns:
            list: Formatted pull request details.
        """

        api_state = state

        if state == "merged":
            api_state = "closed"

        pull_requests = self.github_client.get_pull_requests(
            owner,
            repo,
            api_state,
            count
        )

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

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            pr_number (int): Pull request number.
            description (str): Updated description.

        Returns:
            dict: Updated pull request information.
        """

        return self.github_client.update_pr_description(  ### Method call from main
            owner,
            repo,
            pr_number,
            description
        )
    def parse_pr_description(
        self,
        description
    ):
        """
        Parse pull request description and extract
        number_of_prs and repo_url values.

        Args:
            description (str): Pull request description.

        Returns:
            dict: Parsed pull request configuration
                containing count and repository URL.
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
        Parse repository URL and extract
        owner and repository name.

        Args:
            repo_url (str): GitHub repository URL.

        Returns:
            dict: Repository owner and name.
        """

        parts = repo_url.rstrip("/").split("/")

        return {
            "owner": parts[-2],
            "repo": parts[-1]
        }