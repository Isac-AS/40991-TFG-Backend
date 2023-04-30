import contextlib
import json
import venv
import subprocess
import sys
import io


def print_output(result, message):
    output = {'result': result, 'message': message}
    # Serialize the output
    serialized_output = json.dumps(output)
    # Return serialized output through stdout
    print(serialized_output)


if __name__ == '__main__':
    # Read imput input
    standard_input = input()
    # Deserialize input
    input_dict = json.loads(standard_input)
    # Read the virtual environment's directory
    env_dir = input_dict['env_dir']
    requirements_file = input_dict['requirements_file']

    try:
        # Virtual environment creation
        venv.create(env_dir, with_pip=True)
    except Exception as e:
        error_message = "[ERROR] - [ATTEMPTING VIRTUAL ENV CREATION]:"
        print(error_message, file=sys.stderr)
        print(e, file=sys.stderr)
        print_output(False, "Error during virtual environment creation")

    try:
        # Install dependencies
        subprocess.run([f"{env_dir}/bin/pip", "install","-r", requirements_file], check=True)
    except Exception as e:
        error_message = "[ERROR] - [ATTEMPTING DEPENDENCY INSTALLATION]:"
        print(error_message, file=sys.stderr)
        print(e, file=sys.stderr)
        print_output(False, "Error during dependency installation")

    print_output(True, "Virtual environment created successfully!")
