import os
from textwrap import dedent

from click.testing import CliRunner

from ..commands.configuration import setup as setup_command
from ..settings import LOCAL_CONFIG


def test_setup_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        user_input = ["john-doe", "12345", "67890"]
        user_path = "{}/{}".format(os.getcwd(), LOCAL_CONFIG)

        result = runner.invoke(
            setup_command,
            env={"LANCET_USER_CONFIG": user_path},
            input="\n".join(user_input),
        )
        assert result.exit_code == 0

        text = dedent(
            """
            Step 1 of 3
            Enter your Gitlab username:
            Username: john-doe

            Step 2 of 3
            Add the company wide account ID.
            You can get it from https://id.getharvest.com/developers.
            Accound ID: 12345

            Step 3 of 3
            Add the user ID found on your profile's URL:
            https://divio.harvestapp.com/people/<YOUR_ID>/.
            User ID: 67890

            Configuration correctly written to "{}".\n""".format(user_path)
        )
        text = "\n".join(text.split("\n")[1:])  # remove first line break
        assert result.output == text
