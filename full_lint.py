.
Directory Structure:
markdown
Copy code
ansible_lint/
├── __init__.py
├── lint_rules/
│   ├── __init__.py
│   ├── always_run.py
│   ├── become_user.py
│   ├── when_jinja2.py
│   ├── sudo_usage.py
│   ├── bare_variables.py
│   ├── octal_permissions.py
│   ├── command_usage.py
│   ├── command_env_vars.py
│   ├── task_names.py
│   ├── changed_tasks.py
│   ├── rm_rf_usage.py
│   └── disallowed_keywords.py
├── utils/
│   ├── __init__.py
│   ├── yaml_utils.py
│   └── logging_utils.py
└── main.py
ansible_lint/lint_rules/__init__.py
python
Copy code
import os
import importlib

def load_lint_rules():
    lint_rules = {}
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Strip .py extension
            module = importlib.import_module(f"ansible_lint.lint_rules.{module_name}")
            for attr in dir(module):
                if callable(getattr(module, attr)) and attr.startswith('check_'):
                    lint_rules[attr] = getattr(module, attr)
    return lint_rules
ansible_lint/lint_rules/alway_run.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

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
ansible_lint/lint_rules/become_user.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_become_user(playbook):
    rule_id = "LSIAC002"
    description = "become_user will not actually change user."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if task.get('become_user'):
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses become_user. Consider revising user privilege escalation methods.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking become_user: {exc}")
ansible_lint/lint_rules/when_jinja2.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_when_jinja2(playbook):
    rule_id = "LSIAC003"
    description = "when lines should not include Jinja2 variables."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'when' in task:
                        for condition in task['when']:
                            if '{{' in condition and '}}' in condition:
                                logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' has Jinja2 variables in 'when' clause.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking Jinja2 variables in 'when': {exc}")
ansible_lint/lint_rules/sudo_usage.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_sudo_usage(playbook):
    rule_id = "LSIAC004"
    description = "Usage of sudo/sudo_user is deprecated. Instead use become, become_user."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'sudo' in task or 'sudo_user' in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses deprecated sudo or sudo_user.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking sudo usage: {exc}")
ansible_lint/lint_rules/bare_variables.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_bare_variables(playbook):
    rule_id = "LSIAC005"
    description = "Using bare variables is deprecated."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    for key, value in task.items():
                        if isinstance(value, str) and '{{' in value and '}}' in value:
                            logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses bare variables.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking bare variables: {exc}")
ansible_lint/lint_rules/octal_permissions.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_octal_permissions(playbook):
    rule_id = "LSIAC006"
    description = "Octal permission should contain a leading zero."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'file' in task:
                        mode = task.get('mode')
                        if isinstance(mode, int) and not str(mode).startswith('0'):
                            logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses octal permission without leading zero.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking octal permissions: {exc}")
ansible_lint/lint_rules/command_usage.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_command_usage(playbook):
    rule_id = "LSIAC007"
    description = "Using command rather than module."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'command' in task and 'module' not in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' uses command instead of a module.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking command usage: {exc}")
ansible_lint/lint_rules/command_env_vars.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_command_env_vars(playbook):
    rule_id = "LSIAC008"
    description = "Environment variables don’t work as a part of command."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'command' in task and 'environment' in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' has environment variables with command.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking command environment variables: {exc}")
ansible_lint/lint_rules/task_names.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

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
ansible_lint/lint_rules/changed_tasks.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_changed_tasks(playbook):
    rule_id = "LSIAC010"
    description = "Tasks that run changed should likely be handlers."
    try:
        with open(playbook, 'r') as file:
            content = yaml.safe_load(file)
            for play in content:
                for task in play.get('tasks', []):
                    if 'changed' in task:
                        logger.error(f"{rule_id} - {description} - {playbook} - Task '{task.get('name', 'Unnamed task')}' runs changed. Consider making it a handler.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking changed tasks: {exc}")
ansible_lint/lint_rules/rm_rf_usage.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

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
ansible_lint/lint_rules/disallowed_keywords.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def check_disallowed_keywords(playbook):
    rule_id = "LSIAC012"
    description = "Disallowed keywords are present in playbook."
    disallowed_keywords = ['pre_tasks:', 'post_tasks:', 'handlers:', 'tasks:', 'environment:', 'defaults:', 'collections:', 'become:']

    try:
        with open(playbook, 'r') as file:
            content = file.read()
            for keyword in disallowed_keywords:
                if keyword in content:
                    logger.error(f"{rule_id} - {description} - {playbook} - The keyword '{keyword}' is not allowed in the playbook.")
    except Exception as exc:
        logger.error(f"{rule_id} - {description} - {playbook} - Error checking disallowed keywords: {exc}")
ansible_lint/utils/yaml_utils.py
python
Copy code
import yaml
from ..utils.logging_utils import logger

def basic_yaml_check(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
    except yaml.YAMLError as exc:
        logger.error(f"YAML Error in {file_path}: {exc}")
ansible_lint/utils/logging_utils.py
python
Copy code
import logging

# Set up logging
logging.basicConfig(filename='ansible.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
ansible_lint/main.py
python
Copy code
import os
from ansible_lint.lint_rules import load_lint_rules
from ansible_lint.utils.yaml_utils import basic_yaml_check
from ansible_lint.utils.logging_utils import logger

def lint_playbooks(playbooks, lint_rules):
    for playbook in playbooks:
        if os.path.isfile(playbook):
            if '@LINT_IGNORE' not in open(playbook).read():
                basic_yaml_check(playbook)
                for rule_name, rule_function in lint_rules.items():
                    rule_function(playbook)

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
    lint_rules = load_lint_rules()  # Load all lint rules dynamically
    lint_playbooks(playbooks, lint_rules)
    lint_vars_directory(vars_dir)

    # Evaluate the log file
    log_file = 'ansible.log'
    if not evaluate_log_file(log_file):
        exit(1)  # Exit with failure status if errors are found

if __name__ == "__main__":
    playbooks = ['playbook1.yaml', 'playbook2.yaml']  # Replace with your playbook files
    vars_dir = 'vars'  # Replace with your vars directory
    main(playbooks, vars_dir)
How to Use
Place the lint rule scripts in the ansible_lint/lint_rules/ directory.
Define your lint rules in separate files, following the pattern shown above.
Run the main.py script with the list of playbooks and the vars directory. It will apply all lint rules and log errors to ansible.log.
This modular approach makes it easy to add or remove lint rules by simply modifying the contents of the lint_rules directory without altering the main script.






