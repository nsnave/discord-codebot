# Referenced:
# https://stackoverflow.com/a/8577226/11039508
# https://stackoverflow.com/a/2257449/11039508

import os
import tempfile
import subprocess

from sandbox import Sandbox
import string
import random
import time
import requests


# Handles running the code in the specified language
# Returns the output from running the code (stdout and stderr) with the exit status
class CodeDriver:
    # Unpacks the return code, stdout, and stderr from a subprocess.CompletedProcess object
    def unpack(self, result):
        exit_status = result.returncode
        output = result.stdout.decode("utf-8") 
        error = result.stderr.decode("utf-8")   
    
        return exit_status, output, error
    

    # Runs a command-line command piping stdout and stderr
    def handleSub(self, args, input_arg=None):
        return subprocess.run(args, 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            input=input_arg)


    # Handles runing code that requires two command-line calls
    # Typically, used for code that requires being compiled as opposed to an interpreter
    def handleCompiled(self, comp_args, exec_args, exec_path):
        # Compiles the code
        compiler_result = self.handleSub(comp_args)
        
        exit_status, output, error = self.unpack(compiler_result)
        
        # Runs compiled file if the code comiled succesfully
        if (exit_status == 0):
            run_result = self.handleSub(exec_args)

            run_exit, run_out, run_err = self.unpack(run_result)

            exit_status = run_exit
            output += "\n" + run_out
            error += "\n" + run_err

            # Removes compiled file
            os.remove(exec_path)
        
        return exit_status, output, error


    # Runs the file at `path` containing appropriately given a language `lang`
    # Returns the exit status, stdout, and stderr
    def runFile(self, lang, path):
        # Runs the code
        if (lang == 'python'):
            # Runs Python code
            result = self.handleSub(['python3', path])
            exit_status, output, error = self.unpack(result)
        elif (lang == 'c'):
            # Runs C code
            exec_path = path + "-exec"
            comp_args = ['gcc', '-x', 'c', path, '-o', exec_path]
            exit_status, output, error = self.handleCompiled(comp_args, exec_path, exec_path)
        elif (lang == 'c++'):
            # Runs C code
            exec_path = path + "-exec"
            comp_args = ['g++', '-x', 'c++', path, '-o', exec_path]
            exit_status, output, error = self.handleCompiled(comp_args, exec_path, exec_path)
        elif (lang == 'java'):
            # Runs Java code
            exec_path = path + "-exec.java"
            comp_args = ['cp', path, exec_path]
            exec_args = ['java', exec_path]
            exit_status, output, error = self.handleCompiled(comp_args, exec_args, exec_path)
        elif (lang == "sml"):
            # Runs SML/NJ Code
            input_arg = 'use "' + path + '";\n'
            result = self.handleSub(['sml'], input_arg.encode('utf-8'))
            exit_status, output, error = self.unpack(result)
            
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
            result = self.handleSub(['node', path])
            exit_status, output, error = self.unpack(result)
        elif (lang == "bash"):
            # Runs Bash Code
            result = self.handleSub(['bash', path])
            exit_status, output, error = self.unpack(result)
        else:
            # Language Not Supported
            exit_status = -1
            output = ""
            error = 'Language "' + lang + '" is currently not supported. For a list of supported languages run the `help code` command.' 

        return exit_status, output, error


    # Runs the code provided verbatim in `code` in the language specified by `lang`
    # Returns the exit status, stdout, and stderr
    def run(self, lang, code):
        # Creates temporary file to writes code to it
        # Then runs the code appropriately
        fd, path = tempfile.mkstemp()
        try:
            # Writes code to the temp file
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(code)

            exit_status, output, error = self.runFile(lang, path)
        except:
            exit_status = -1
            output = ""
            error = "CodeBot has encountered an unexpected error."
        finally:
            os.remove(path)

        return exit_status, output, error




def genHere(input_arg):
    new_here = lambda : ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    here = new_here()
    while here in input_arg:
        here = new_here()

    return ' <<' + here + "\n" + input_arg + here


# Child class of CodeDriver
# Handles running the code in the specified language within a secure sandboxed environment
# Returns the output from running the code (stdout and stderr) with the exit status
class CodeDriverSecure(CodeDriver):

    def unpack(self, obj):
        return obj['exit'], obj['out'], obj['err']

    def handleSub(self, args, input_arg=None):

        cmd = " ".join(args)

        if (input_arg != None):
            cmd += genHere(input_arg)

        return self.sandbox.exec(cmd)

    def run(self, lang, code):
        # Creates sandbox
        self.sandbox = Sandbox()
        
        # Waits for sandbox server to be running by attempting HEAD requests
        addr = 'http://localhost:' + str(self.sandbox.port)
        while True:
            try:
                requests.head(addr)
                # If request didn't fail, sandbox server up
                break
            except:
                # Still need to wait
                time.sleep(0.01)

        # Creates file containing code to run in the sandbox
        path = "/.codebot/code"
        cmd = "cat > " + path + genHere(code)
        temp = self.sandbox.exec(cmd)

        if (temp['exit'] != 0):
            # Error occured while creating code file
            exit_status = -1
            output = ""
            error = "CodeBot has encountered an unexpected error."
        else:
            # Runs the code in the sandbox
            exit_status, output, error = self.runFile(lang, path)

        # Closes the sandbox
        del self.sandbox

        return exit_status, output, error

