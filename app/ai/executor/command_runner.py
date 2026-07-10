import subprocess


class CommandRunner:


    def run(self, command):

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "status":"SUCCESS",
                "output":result.stdout
            }

        except Exception as e:

            return {
                "status":"ERROR",
                "error":str(e)
            }


runner = CommandRunner()
