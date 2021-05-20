# Referenced:
# https://stackoverflow.com/a/8577226/11039508

import os
import tempfile
import subprocess


# Handles running the code in the specified language
# Returns the output from running the code (stdout and stderr) with the exit status
class CodeDriver:
    def unpack(result):
        exit_status = result.returncode
        output = result.stdout.decode("utf-8") 
        error = result.stderr.decode("utf-8")   
    
        return exit_status, output, error
    
    def handleSub(args, input_arg=None):
        return subprocess.run(args, 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            input=input_arg)

    def handleCompiled(comp_args, exec_args, exec_path):
        # Compiles the code
        compiler_result = CodeDriver.handleSub(comp_args)
        
        exit_status = compiler_result.returncode
        output = compiler_result.stdout.decode("utf-8") 
        error = compiler_result.stderr.decode("utf-8")
        
        # Runs compiled file if the code comiled succesfully
        if (exit_status == 0):
            run_result = CodeDriver.handleSub(exec_args)

            exit_status = run_result.returncode
            output += "\n" + run_result.stdout.decode("utf-8")
            error += "\n" + run_result.stderr.decode("utf-8")

            # Removes compiled file
            os.remove(exec_path)
        
        return exit_status, output, error

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
                # Runs Python code
                result = CodeDriver.handleSub(['python3', path])
                exit_status, output, error = CodeDriver.unpack(result)
            elif (lang == 'c'):
                # Runs C code
                exec_path = path + "-exec"
                comp_args = ['gcc', '-x', 'c', path, '-o', exec_path]
                exit_status, output, error = CodeDriver.handleCompiled(comp_args, exec_path, exec_path)
            elif (lang == 'java'):
                # Runs Java code
                exec_path = path + "-exec.java"
                comp_args = ['cp', path, exec_path]
                exec_args = ['java', exec_path]
                exit_status, output, error = CodeDriver.handleCompiled(comp_args, exec_args, exec_path)
            elif (lang == "sml"):
                # Runs SML/NJ Code
                input_arg = 'use "' + path + '";\n'
                result = CodeDriver.handleSub(['sml'], input_arg.encode('utf-8'))
                exit_status, output, error = CodeDriver.unpack(result)
                
                if (exit_status == 0):
                    # Removes unneeded interpreter output
                    output_lines = output.split('\n')
                    adj = -3 if (output_lines[-3] == "val it = () : unit") else -2
                    output = '\n'.join(output_lines[2:adj])

                    # Changes exit status if needed
                    if (adj == -2):
                        exit_status = 1
            elif (lang == "js" or lang == "javascript"):
                # Runs JavaScript Code
                result = CodeDriver.handleSub(['node', path])
                exit_status, output, error = CodeDriver.unpack(result)
            else:
                exit_status = -1
                output = ""
                error = ""

        finally:
            os.remove(path)

        return exit_status, output, error

