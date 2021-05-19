# Referenced:
# https://stackoverflow.com/a/8577226/11039508

import os
import tempfile
import subprocess


# Handles running the code in the specified language
# Returns the output from running the code (stdout and stderr) with the exit status
class CodeDriver:
    def handleSub(args):
        return subprocess.run(args, 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    def run(lang, code):
        # Creates temporary file to writes code to it
        # Then runs the code appropriately
        fd, path = tempfile.mkstemp()
        try:
            # Writes code to the temp file
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(code)
            
            # Runs the code
            if (lang == 'python'):
                # Runs python script
                result = CodeDriver.handleSub(['python3', path])

                exit_status = result.returncode
                output = result.stdout.decode("utf-8") 
                error = result.stderr.decode("utf-8")   
            elif (lang == 'c'):
                # Compiles C code
                exec_path = path + "-exec"
                compiler_result = CodeDriver.handleSub(['gcc', '-x', 'c', path, '-o', exec_path])
                
                exit_status = compiler_result.returncode
                output = compiler_result.stdout.decode("utf-8") 
                error = compiler_result.stderr.decode("utf-8")
                
                # Runs compiled executable if the code comiled succesfully
                if (exit_status == 0):
                    run_result = CodeDriver.handleSub(exec_path)

                    exit_status = run_result.returncode
                    output += "\n" + run_result.stdout.decode("utf-8")
                    error += "\n" + run_result.stderr.decode("utf-8")

                    # Removes created executable
                    os.remove(exec_path)

            else:
                exit_status = -1
                output = ""
                error = ""

        finally:
            os.remove(path)

        return exit_status, output, error

