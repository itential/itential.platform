# Ansible Collection - itential.platform

## License

This project is licensed under the GPLv3 open source license.  See
[LICENSE](LICENSE)

## Setup Instructions

### 1. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Install Itential Core Collection

Since the code depends on the `itential.core` Ansible collection, install it using:

```bash
ansible-galaxy collection install itential.core
```

### 3. Run Unit Tests with Coverage

To execute tests and check code coverage:

```bash
coverage run -m pytest tests/ -v
coverage report -m
```

If you encounter an error related to forks, you might have to set this environmental variable:
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

## Available Modules

### Job Worker Management

- **activate_job_worker**: Activate the job worker for an Itential Platform system

```yaml
- name: Activate Itential Platform job worker
  itential.platform.activate_job_worker:
```

- **deactivate_job_worker**: Deactivate the job worker for an Itential Platform system

```yaml
- name: Deactivate Itential Platform job worker
  itential.platform.deactivate_job_worker:
```

### Task Worker Management

- **activate_task_worker**: Activate the task worker for an Itential Platform system

```yaml
- name: Activate Itential Platform task worker
  itential.platform.activate_task_worker:
```

- **deactivate_task_worker**: Deactivate the task worker for an Itential Platform system

```yaml
- name: Deactivate Itential Platform task worker
  itential.platform.deactivate_task_worker:
```

### System Information

- **get_system_health**: Retrieve the health status of an Itential Platform system

```yaml
- name: Get Itential Platform system health
  itential.platform.get_system_health:
```

- **get_worker_status**: Get the current status of Itential Platform workers

```yaml
- name: Get Itential Platform worker status
  itential.platform.get_worker_status:
```

### Job and Task Management

- **get_jobs**: Retrieve a list of jobs from an Itential Platform system

```yaml
- name: Get Itential Platform jobs
  itential.platform.get_jobs:
```

- **get_tasks**: Retrieve a list of tasks from an Itential Platform system

```yaml
- name: Get Itential Platform tasks
  itential.platform.get_tasks:
```

### System Administration

- **restart_adapter**: Restart a specific adapter in the Itential Platform system

```yaml
- name: Restart Itential Platform adapter
  itential.platform.restart_adapter:
    adapter_name: "my-adapter"
```

- **restart_application**: Restart the Itential Platform application

```yaml
- name: Restart Itential Platform application
  itential.platform.restart_application:
```

- **set_adapter_log_level**: Change the log level/transport of an adapter.
  
```yaml
  - name: Restart Itential Platform application
    itential.platform.restart_applications:
```

### Misc
- **auth_token**: Retrieves the auth token from an Itential Platform system
  
```yaml
  - name: Retrieve auth token
    itential.platform.auth_token:
```

- **generic_request**: Makes an api reqeust given a method and endpoint
  
```yaml
  - name: Retrieve authorization accounts
    itential.platform.generic_request:
      method: GET
      endpoint: "/authorization/accounts"
```

## Module Utils

This collection includes 3 utils which are used by the action plugins.

- **host**: A schema used to gather information from the ansible_task vars.

- **login**: A utility that authenticates with the platform and returns the authentication token.

- **request**: A utility that authenticates then constructs and sends an api request. Takes task_vars, method, endpoint, params, and data as arguments.

### Connection Parameters

Each module requires the following connection parameters which can be defined in your Ansible environment:

- `host`: The hostname or IP of the Itential Platform instance
- `port`: The port number for the Itential Platform API
- `use_tls`: Whether to use HTTPS (default: true)
- `verify`: Whether to verify SSL certificates (default: true)
- `disable_warnings`: Whether to disable SSL warning messages (default: false)

Authentication (requires one of the following):

- Option 1: Username/Password
  - `username`: The username for authentication
  - `password`: The password for authentication
- Option 2: Auth Token
  - `auth_token`: A pre-existing authentication token

For detailed documentation on each module, use the `ansible-doc` command:

```bash
ansible-doc itential.platform.<module_name>
```
