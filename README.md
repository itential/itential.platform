# Ansible Collection - itential.platform

# License

This project is licensed unser the GPLv3 open source license.  See
[LICENSE](LICENSE)

## Setup Instructions

### 1. Install Dependencies
Install all required Python packages:
```sh
pip install -r requirements.txt
```

### 2. Install Itential Core Collection
Since the code depends on the `itential.core` Ansible collection, install it using:
```sh
ansible-galaxy collection install itential.core
```

### 3. Run Unit Tests with Coverage
To execute tests and check code coverage:
```sh
coverage run -m pytest tests/ -v
coverage report -m
```

If you encounter an error related to forks, you might have to set this environmental variable:
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

## Available Modules

### Job Worker Management
- **activate_job_worker**: Activate the job worker for a Platform system
  ```yaml
  - name: Activate Platform job worker
    itential.platform.activate_job_worker:
  ```

- **deactivate_job_worker**: Deactivate the job worker for a Platform system
  ```yaml
  - name: Deactivate Platform job worker
    itential.platform.deactivate_job_worker:
  ```

### Task Worker Management
- **activate_task_worker**: Activate the task worker for a Platform system
  ```yaml
  - name: Activate Platform task worker
    itential.platform.activate_task_worker:
  ```

- **deactivate_task_worker**: Deactivate the task worker for a Platform system
  ```yaml
  - name: Deactivate Platform task worker
    itential.platform.deactivate_task_worker:
  ```

### System Information
- **get_system_health**: Retrieve the health status of a Platform system
  ```yaml
  - name: Get Platform system health
    itential.platform.get_system_health:
  ```

- **get_worker_status**: Get the current status of Platform workers
  ```yaml
  - name: Get Platform worker status
    itential.platform.get_worker_status:
  ```

### Job and Task Management
- **get_jobs**: Retrieve a list of jobs from a Platform system
  ```yaml
  - name: Get Platform jobs
    itential.platform.get_jobs:
  ```

- **get_tasks**: Retrieve a list of tasks from a Platform system
  ```yaml
  - name: Get Platform tasks
    itential.platform.get_tasks:
  ```

### System Administration
- **restart_adapter**: Restart a specific adapter in the Platform system
  ```yaml
  - name: Restart Platform adapter
    itential.platform.restart_adapter:
      adapter_name: "my-adapter"
  ```

- **restart_application**: Restart the Platform application
  ```yaml
  - name: Restart Platform application
    itential.platform.restart_application:
  ```

### Connection Parameters
Each module requires the following connection parameters which can be defined in your Ansible environment:
- `host`: The hostname or IP of the Platform instance
- `port`: The port number for the Platform API
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
