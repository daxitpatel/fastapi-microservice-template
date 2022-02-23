# fastapi-microservice-template

1. Required Dependency

   - Python version - 3.11


2. Setup python using pyenv locally

   - Step to install pyenv

      1. Install Dependency

          - For Ubuntu
          ```bash
          sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl python3-dev
          ```

          - For macOS
          ```bash
          brew install openssl readline sqlite3 xz zlib
          ```

      2. curl https://pyenv.run | bash

      3. sudo nano .bashrc

      4. add below command if not present -> [.bashrc file](SnapShots/bashrc.png)
          ```bash
          export PATH="$HOME/.pyenv/bin:$PATH"
          eval "$(pyenv init -)"eval 
          "$(pyenv virtualenv-init -)"
          ```

      5. Restart the terminal
         ```bash
         exec "$SHELL"     # Or just restart your terminal
         ```

      6. pyenv install --list | grep " 3\.[678]"

      7. pyenv install -v <python version>

      8. pyenv local <python version>

      9. python -m venv venv

      10. source venv/bin/activate

**_NOTE:_**  Skip Step 3 if you have performed Step 2

3. Setup Virtual Environment locally using pycharm

   - Feel free to setup virtual environment using shell.
      1. Go to Files > Settings
      2. Python Interpreter -> [Python Interpreter](SnapShots/python_interpreter.png)
      3. Add Interpreter -> [Add Interpreter](SnapShots/add_interpreter.png)
      4. Select Python 3.11  # this will create a new Python 3.11 Virtual Environment


4. Install Requirements.txt file

   - Execute the below given commands in terminal
     1. pip install --upgrade pip
     2. pip install -r requirements.txt


5. Copy Environment file for local environment

   - Will be used for local development and with third party docker containers
   ```bash
      $ cp sample.env .env
   ```


6. Set PyCharm configurations to run service

   - Install **Environment Pycharm plugin** as below 
      - Install EnvFile
        - Go To Files > Settings > Plugins -> [Env Plugin](SnapShots/Plugin.png)
        - Search for EnvFile and Install it.

   - Configure project to run within pycharm

      - Go To Run
      - Edit Configurations
      - Add Python configuration -> [Python configuration](SnapShots/python_configure.png)
      - Give name 'Channel'
      - Select script path to run.py [script path](SnapShots/script_path.png)
      - Select Python Interpreter that we created in step 2
      - Select env in the configuration [Add env](SnapShots/add_env.png)


7. Run Python run.py

   - You can run service using -> [Run Project](SnapShots/run_project.png)
   - You can run service using python command from terminal
      ```bash
      $ python run.py
   	  ```

### Run locally

#### Run with compose

Create network:

    docker network create fastapi-microservice_network --subnet=172.19.23.100/24 --ipv6=false

The network can also be created running docker compose in the `fastapi-microservice-template` project




## Cronjob/Scheduler

|               **Schedular name**               |                      **Endpoint**                      | **Method** | **execution timing** | **Timeout** | **Active/Suspended** | **Retry on failure** |
|:----------------------------------------------:|:------------------------------------------------------:|------------|----------------------|-------------|----------------------|----------------------|
| fastapi-microservice-rmq-healthcheck-scheduler | http://fastapi-microservice:5015/consumer-health-test  | GET        | Every 5 minute       | 30s         | Active               | Yes                  |