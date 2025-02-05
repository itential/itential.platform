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
