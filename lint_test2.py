.
import logging
import re
import yaml
import os

# Configure logging to write to a file
logging.basicConfig(filename='ansible.log', level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Define lint functions with identifiers and detailed logging

def check_always_run(playbook):
    rule_id = "LSIAC001"
    description = "Instead of always_run, use check_mode."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if task.get('always_run'):
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses always_run. Consider using check_mode instead.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking always_run: {exc}")

def check_become_user(playbook):
    rule_id = "LSIAC002"
    description = "become_user will not actually change the user."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if task.get('become_user'):
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses become_user, which will not actually change the user.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking become_user: {exc}")

def check_when_jinja2(playbook):
    rule_id = "LSIAC003"
    description = "when lines should not include Jinja2 variables."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'when' in task:
                        when_cond = task['when']
                        if isinstance(when_cond, str) and '{{' in when_cond and '}}' in when_cond:
                            logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses Jinja2 variables in when condition.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking when conditions: {exc}")

def check_sudo_usage(playbook):
    rule_id = "LSIAC004"
    description = "Usage of sudo/sudo_user is deprecated; instead, use become, become_user."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'sudo' in task or 'sudo_user' in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses deprecated sudo/sudo_user.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking sudo usage: {exc}")

def check_bare_variables(playbook):
    rule_id = "LSIAC005"
    description = "Using bare variables is deprecated."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    for key, value in task.items():
                        if isinstance(value, str) and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
                            logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses bare variable '{value}'.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking bare variables: {exc}")

def check_octal_permissions(playbook):
    rule_id = "LSIAC006"
    description = "Octal permission should contain a leading zero."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'mode' in task:
                        mode = task['mode']
                        if isinstance(mode, str) and not mode.startswith('0'):
                            logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses octal permission without leading zero '{mode}'.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking octal permissions: {exc}")

def check_command_usage(playbook):
    rule_id = "LSIAC007"
    description = "Using command rather than a module."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'command' in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses command module. Consider using appropriate module instead.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking command usage: {exc}")

def check_command_env_vars(playbook):
    rule_id = "LSIAC008"
    description = "Environment variables don't work as a part of command."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'command' in task and 'environment' in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses environment variables with command module.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking environment variables with command: {exc}")

def check_task_names(playbook):
    rule_id = "LSIAC009"
    description = "All tasks should be named."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'name' not in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task without a name found.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking task names: {exc}")

def check_changed_tasks(playbook):
    rule_id = "LSIAC010"
    description = "Tasks that run changed should likely be handlers."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if task.get('changed_when'):
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' that runs changed should likely be a handler.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking changed tasks: {exc}")

def check_rm_rf_usage(playbook):
    rule_id = "LSIAC011"
    description = "The use of rm -rf command is not allowed."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'command' in task and 'rm -rf' in task['command']:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses rm -rf command.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking rm -rf usage: {exc}")

def check_disallowed_keywords(playbook):
    rule_id = "LSIAC012"
    description = "Disallowed keywords in privileged-playbook.yaml: pre_tasks, post_tasks, handlers, tasks, environment, defaults, collections, become."
    disallowed_keywords = [
        'pre_tasks:', 'post_tasks:', 'handlers:', 'tasks:', 
        'environment:', 'defaults:', 'collections:', 'become:'
    ]
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for keyword in disallowed_keywords:
                if keyword in yaml.dump(content):
                    logger.error(f"{rule_id} - {description} - {playbook} - File contains disallowed keyword '{keyword}'.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking disallowed keywords: {exc}")

def basic_yaml_check(file_path):
    """Perform basic YAML syntax validation."""
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
    except yaml.YAMLError as exc:
        logger.error(f"YAML Syntax Error in file {file_path}: {exc}")

def lint_playbooks(playbooks):
    for playbook in playbooks:
        if os.path.isfile(playbook):
            if '@LINT_IGNORE' not in open(playbook).read():
                basic_yaml_check(playbook)
                check_always_run(playbook)
                check_become_user(playbook)
                check_when_jinja2(playbook)
                check_sudo_usage(playbook)
                check_bare_variables(playbook)
                check_octal_permissions(playbook)
                check_command_usage(playbook)
                check_command_env_vars(playbook)
                check_task_names(playbook)
                check_changed_tasks(playbook)
                check_rm_rf_usage(playbook)
                check_disallowed_keywords(playbook)

def lint_vars_directory(vars_dir):
    """Lint YAML files in the vars directory with basic checks."""
    for root, _, files in os.walk(vars_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                basic_yaml_check(os.path.join(root, file))

def evaluate_log_file(log_file):
    """Evaluate the log file for errors and print them."""
    with open(log_file, 'r') as file:
        lines = file.readlines()
    
    errors_found = any('ERROR' in line for line in lines)
    
    if errors_found:
        print("Errors found in Ansible linting. See ansible.log for details.")
        for line in lines:
            if 'ERROR' in line:
                print(line.strip())
        return False
    else:
        print("No errors found in Ansible linting.")
        return True

def main(playbooks, vars_dir):
    # Lint playbooks and vars directory
    lint_playbooks(playbooks)
    lint_vars_directory(vars_dir)
    
    # Evaluate the log file
    log_file = 'ansible.log'
    if not evaluate_log_file(log_file):
        exit(1)  # Exit with failure status if errors are found

if __name__ == "__main__":
    playbooks = ['playbook1.yaml', 'playbook2.yaml']  # Replace with your playbook files
    vars_dir = 'vars'  # Replace with your vars directory
    main(playbooks, vars_dir)
