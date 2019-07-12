from textwrap import dedent
from tempfile import mkdtemp

from click.testing import CliRunner

from lancet.commands.configuration import hello

from ..settings import USER_CONFIG



def test_hello_world():
    user_input = ["john-doe", "12345", "67890"]
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(hello, args="-f", input="\n".join(user_input))
        assert result.exit_code == 0

        # import os
        # print('#######')
        # print(os.getcwd())

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

            Configuration correctly written to "{USER_CONFIG}".\n""")
        text = '\n'.join(text.split('\n')[1:])  # remove first line break
        assert result.output == text
