# Referenced:
# https://stackoverflow.com/a/8577226/11039508

import os
import tempfile
import subprocess


# Handles running the code in the specified language
# Returns the output from running the code (stdout and stderr) with the exit status
class CodeDriver:
    def run(lang, code):
        exit_status = -1
        output = ""
        error = ""
        err = False
        # Creates temporary file to writes code to it
        # Then runs the code appropriately
        fd, path = tempfile.mkstemp()
        try:
            # Writes code to the temp file
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(code)
            
            # Runs the code
            if (lang == 'python'):
                result = subprocess.run(['python3', path], 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            else:
                err = True

            if not err:
                exit_status = result.returncode
                output = result.stdout.decode("utf-8") 
                error = result.stderr.decode("utf-8")   

        finally:
            os.remove(path)

        return exit_status, output, error

