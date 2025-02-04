# Ansible Collection - itential.platform

# License

This project is licensed unser the GPLv3 open source license.  See
[LICENSE](LICENSE)

# Project Dependencies

This project requires the following dependencies:

- **Python** 
- **Ansible**
- **Itential Core Collection** from Ansible Galaxy  
  Install with:  
  ```sh
  ansible-galaxy collection install itential.core

Unit tests require the following dependencies:
- **pytest** (unit tests)
Install with:
    ```sh
    pip install pytest
- **pytest-ansible**
Install with:
    ```sh
    pip install pytest-ansible 
- **Coverage**
Install with:
    ```sh
    pip install coverage 
To see a coverage report you can use:
    ```coverage run -m pytest tests/ -v ```

Then:
    ```coverage report```