## Model chosen

Out of the six models tested, the third one (XGBoost with Feature Importance and with Balance) was selected. The main reason for this choice is that it achieves a recall of approximately 69% for class 1.

## Development
For this project, I used [pipenv](https://pipenv.pypa.io/en/latest/) to manage Python dependencies. The Python version used is 3.10, but the setup should also work on newer versions.
You can initialize the virtual environment and install the Python dependencies by running:

    pipenv install --dev
    
Then, activate the environment with:

    pipenv shell
    
Inside the virtual environment, you can run tests using the following make commands:

    make model-test
    male api-test
    make stress-test
    
    
## Deployment
A Dockerfile is included to facilitate deployment of the API. DigitalOcean was chosen as the cloud provider. The public API is available at:

    https://walrus-app-os58h.ondigitalocean.app
    
## CI/CD
GitHub Actions are configured in two separate workflows:
1. CI workflow:
  - Runs Python linters (black, flake8, isort) to check code style and consistency.
  - Executes tests to ensure everything is working as expected.
2. CD workflow:
  - Triggers a new deployment on DigitalOcean when changes are merged into the main branch.
