import os
from textwrap import dedent

from click.testing import CliRunner

from ..commands.configuration import setup as setup_command
from ..settings import LOCAL_CONFIG, USER_CONFIG


def test_setup_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        user_input = ["3", "john-doe", "john-doe", "12345", "67890"]
        lancet_path = "{}/{}".format(os.getcwd(), LOCAL_CONFIG)

        result = runner.invoke(
            setup_command,
            env={"LANCET_TEST_USER_CONFIG": lancet_path},
            input="\n".join(user_input),
        )
        assert result.exit_code == 0

        text = dedent(
            """
            Welcome to the Lancet setup wizard.
            Please choose a tracker:
            (1) Gitlab, (2) Jira, (3) Both: 3

            Step 1 of 4
            Enter your Gitlab username:
            Username: john-doe

            Step 2 of 4
            Enter your Jira username:
            Username: john-doe

            Step 3 of 4
            Enter the Harvest account ID:
            (You can get it from https://id.getharvest.com/developers)
            Accound ID: 12345

            Step 4 of 4
            Enter the Harvest ID found on your profile's URL:
            (You can get it from https://divio.harvestapp.com/people/<YOUR_ID>/)
            User ID: 67890

            Configuration correctly written to "{}".\n""".format(lancet_path)
        )
        text = "\n".join(text.split("\n")[1:])  # remove first line break
        assert result.output == text

        with open(lancet_path) as f:
            text = dedent(
                """
                [lancet]

                [tracker:gitlab]
                username = john-doe

                [scm-manager:gitlab]
                username = john-doe

                [tracker:jira]
                url = https://divio-ch.atlassian.net
                username = john-doe

                [timer:harvest]
                username = 12345
                user_id = 67890

                """)
            text = "\n".join(text.split("\n")[1:])  # remove first line break
            assert text == f.read()
