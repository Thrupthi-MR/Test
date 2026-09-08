import os
import json


class FileWriter:
    """
    Handles writing pull request information
    to report and JSON files.
    """

    def write_report(
        self,
        pr_details,
        files,
        output_file
    ):
        """
        Write pull request details and changed file
        information to a text report.

        Args:
            pr_details (dict): Pull request details.
            files (list): List of changed files.
            output_file (str): Output report file path.
        """
        os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as report:

            report.write(
                "PR REPORT\n"
            )

            report.write(
                "=" * 40 + "\n\n"
            )

            report.write(
                f"PR Number : {pr_details['number']}\n"
            )

            report.write(
                f"Title     : {pr_details['title']}\n"
            )

            report.write(
                f"Author    : {pr_details['author']}\n"
            )

            report.write(
                f"State     : {pr_details['state']}\n\n"
            )

            report.write(
                "FILES CHANGED\n"
            )

            report.write(
                "=" * 40 + "\n\n"
            )

            for file in files:

                report.write(
                    f"File Name : {file['filename']}\n"
                )

                report.write(
                    f"Status    : {file['status']}\n"
                )

                report.write(
                    f"Additions : {file['additions']}\n"
                )

                report.write(
                    f"Deletions : {file['deletions']}\n"
                )

                report.write(
                    "-" * 40 + "\n"
                )

    def write_pr_list_json(
        self,
        pull_requests,
        output_file
    ):
        """
        Write pull request list to a JSON file.

        Args:
            pull_requests (list): Pull request data.
            output_file (str): Output JSON file path.
        """
        os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as json_file:

            json.dump(
                pull_requests,
                json_file,
                indent=4
            )