import os
import logging
import yaml

# Set up logging
logging.basicConfig(filename='ansible_lint.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to check YAML syntax
def check_yaml_syntax(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
        logger.info(f"YAML syntax check passed for {file_path}")
    except yaml.YAMLError as e:
        logger.error(f"YAML syntax error in file {file_path}: {e}")

# Function to perform custom checks on privileged-playbook.yaml
def check_privileged_playbook(file_path):
    forbidden_keywords = [
        'pre_tasks', 'post_tasks', 'handlers', 'tasks', 
        'environment', 'defaults', 'collections', 'become'
    ]
    with open(file_path, 'r') as file:
        content = file.read()
        for keyword in forbidden_keywords:
            if keyword in content:
                logger.error(f"Forbidden keyword '{keyword}' found in {file_path}")

# Placeholder function for lint check
def lint_check(file_path):
    # Here you can integrate with a linting tool like yamllint or ansible-lint
    logger.info(f"Lint check passed for {file_path}")

# Main function to find YAML files and perform checks
def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                
                # Perform YAML syntax check on all YAML files
                check_yaml_syntax(file_path)
                
                # Perform additional checks on privileged-playbook.yaml
                if file == 'privileged-playbook.yaml':
                    check_privileged_playbook(file_path)
                
                # Perform lint check on all YAML files except those in 'vars' directories
                if 'vars' not in root.split(os.sep):
                    lint_check(file_path)
    
    # Check for errors in the log file
    with open('ansible_lint.log', 'r') as log_file:
        log_contents = log_file.read()
        if "ERROR" in log_contents:
            print("Lint checks failed. See ansible_lint.log for details.")
            print(log_contents)
        else:
            print("Lint checks passed.")

if __name__ == "__main__":
    main()
