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
    description = os.getenv("PR_BODY")

    print("\nPR Description:")
    print(description)


    token = os.getenv("PAT_TOKEN")
    
    print(token is not None)

    client = GitHubClient(token)

    pr_manager = PRManager(client)
    parsed_data = pr_manager.parse_pr_description(
        description
    )

    print("\nParsed Data:")
    print(parsed_data)
    repo_data = pr_manager.parse_repo_url(
        parsed_data["repo_url"]
    )

    print("\nRepository Data:")
    print(repo_data)

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

    # print("\nUpdating PR Description...")

    # result = pr_manager.update_pr_description(
    #     "Thrupthi-MR",
    #     "Test",
    #     49,
    #     "PR updated using GitHub API and Python OOP project."
    # )

    # print("\nUpdated Description:")
    # print(result["body"])

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    report_file = os.path.join(
        base_dir,
        "output",
        "pr_report.txt"
    )

    json_file = os.path.join(
        base_dir,
        "output",
        "pr_list.json"
    )


    writer.write_report(
        pr_details,
        files,
        report_file
    )

    print(
        f"\nReport generated successfully: "
        f"{report_file}"
    )
    print("\nLast Pull Requests:")

    print("\nUsing Values:")

    print(
        repo_data["owner"]
    )

    print(
        repo_data["repo"]
    )

    print(
        parsed_data["count"]
    )

    print("\nLast Pull Requests:")

    pull_requests = pr_manager.get_pull_requests(
        repo_data["owner"],
        repo_data["repo"],
        state="closed",
        count=parsed_data["count"]
    )


    for pr in pull_requests:
        print(pr)

    writer.write_pr_list_json(
        pull_requests,
        json_file
    )

    print(
        f"\nPR JSON report generated: "
        f"{json_file}"
    )

if __name__ == "__main__":
    main()

