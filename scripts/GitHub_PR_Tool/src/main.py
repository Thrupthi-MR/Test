"""Main entry point for GitHub Pull Request Tool."""

import os

from github_client import GitHubClient
from pr_manager import PRManager
from file_writer import FileWriter



def main():
    """
    Fetch pull request details, fetch changed files,
    update the PR description, and generate a report.
    """

    import os

    token = os.getenv("GITHUB_TOKEN")

    client = GitHubClient(token)

    pr_manager = PRManager(client)

    writer = FileWriter()

    pr_details = pr_manager.get_pr_details(
        "Thrupthi-MR",
        "Test",
        49
    )

    print("PR Details:")
    print(pr_details)

    print("\nChanged Files:")

    files = pr_manager.get_pr_files(
        "Thrupthi-MR",
        "Test",
        49
    )

    for file in files:
        print(file)

    print("\nUpdating PR Description...")

    result = pr_manager.update_pr_description(
        "Thrupthi-MR",
        "Test",
        49,
        "PR updated using GitHub API and Python OOP project."
    )

    print("\nUpdated Description:")
    print(result["body"])


    writer.write_report(
        pr_details,
        files,
        "../output/pr_report.txt"
    )

    print(
        "\nReport generated successfully: "
        "../output/pr_report.txt"
    )
    print("\nLast Pull Requests:")

    pull_requests = pr_manager.get_pull_requests(
        "Thrupthi-MR",
        "Test",
        state="closed",
        count=10
    )


    for pr in pull_requests:
        print(pr)

    writer.write_pr_list_json(
        pull_requests,
        "../output/pr_list.json"
    )

    print(
        "\nPR JSON report generated: "
        "../output/pr_list.json"
    )

if __name__ == "__main__":
    main()

