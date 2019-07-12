import os

from textwrap import dedent
from tempfile import mkdtemp

from click.testing import CliRunner

from lancet.settings import LOCAL_CONFIG
from lancet.commands.configuration import setup as setup_command


def test_setup_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        user_input = ["john-doe", "12345", "67890"]
        user_path = f"{os.getcwd()}/{LOCAL_CONFIG}"

        result = runner.invoke(
            setup_command,
            env={"ENV_USER_CONFIG": user_path},
            input="\n".join(user_input),
        )
        assert result.exit_code == 0

        # print(result.output)
        text = dedent(f"""
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

            Configuration correctly written to "{user_path}".\n""")
        text = '\n'.join(text.split('\n')[1:])  # remove first line break
        assert result.output == text
