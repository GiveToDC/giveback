# giveback
There are individual function READMEs in function folders.

## Environment Variables
 **If you use the production token in test environments (Local and GitHub) then the tests will make a bunch of API calls to the GiveCard production API!** The **only** place the production key should end up is assigned as a secret in Google Secret Manager!

 We prepend `'Bearer '` in code, so these variables should just be the token.
### Local
For running tests locally create a `.env` file in the root of the project with the dev token.
```yaml
bearer_token="<TOKEN>"
```

### GitHub actions
To run the tests as part of a GitHub workflow the dev token is assigned as a repository secret called `GIVECARD_DEV_BEARER_TOKEN`.
```yaml
    - name: Test with pytest
      env:
        BEARER_TOKEN: ${{ secrets.GIVECARD_DEV_BEARER_TOKEN }}
      run: |
        python tests.py
```

### Google Cloud
Cloud deployed functions get their environment variables from Secret Manager, we select what secrets the functions see from Secret Manager in `cloudbuild.yaml` with an argument in the deploy command.
```yaml
  - --set-secrets=BEARER_TOKEN=givecard_dev_token:latest
```
To change what token a function operates with would just require changing `givecard_dev_token` to the name of the production token stored in Secret Manager.

## File Structure

```yaml
.
├── .github
│	└── workflows
│		└── test.yml				# GitHub actions workflow to run tests on pushes to any branch
├── functions					# Function folder
│   └── example_function			# Each Google Cloud Function is it's own folder
│       ├── main.py					# The function body
│		├── README.md				# Function specific README
│		├──	requirements.txt		# Requirements to run this specific Cloud Function
│		└── tests.py				# Function specific tests to be ran locally and as a GitHub action
├── .gitignore					
├── cloudbuild.yaml				# Google Cloud Build integration deploys functions according to this config
├── README.md
├── requirements.txt			# Requirements for running the project locally
└── tests.py 					# Script to loop through each function's tests
```



## Running tests
1. [Create and activate a Python venv](https://docs.python.org/3/library/venv.html)
2. Install requirements with `pip install -r requirements.txt`
3. Run all tests with `python tests.py` or navigate into a function folder and run its tests with `pytest`

## CI/CD
Initially intended to use [Terraform](https://www.terraform.io/), but seemed like overkill for the limited initial functionality, this would have all Google Cloud Resources provisioned through code (.tf files). Seems relatively feasible to 'export' an entire project from Google Cloud and generate Terraform code for it if Terraform becomes a desirable solution in the future.

### Cloud Build
Currently, instructions to deploy cloud functions are described in the `cloudbuild.yaml` folder, which is read whenever there are changes to main.

#### Setup
1. Go to Cloud Build > Triggers > Create Trigger
2. Name the trigger, this trigger will be responsible for building all cloud functions, not a singular one
3. Configure trigger invoke condition (in this case, pushes to the main branch)
4. Select GitHub (Cloud Build GitHub App), you will need to authenticate with GitHub and give the integration permissions
5. Defaults of an autodetected cloudbuild.yaml and the repository as the location fine.
6. Go to Cloud Build > Settings and enable the service account permissions Cloud Functions Developer and Service Accounts User.
7. Enable Cloud Resource Manager API if not already enabled.
8. We can now create our `cloudbuild.yaml` in the codebase.

```yaml
steps:
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk' # The name of the step specifies what container to run
  args:	# These args comprise a command ran in the container, in this case a call to 'gcloud functions deploy'
  - gcloud
  - functions
  - deploy
  - load_cards	# Specifies what the cloud function will be called
  - --region=us-east1	# Set the region
  - --trigger-topic=load_cards	# Subscribe to the topic
  - --runtime=python311		# Choose the Python runtime
  - --gen2	# Opt for a gen2 Google Cloud Function
  - --set-secrets=BEARER_TOKEN=givecard_dev_token:latest	# Environment variable using Google Secret Manager
  dir: 'functions/load_cards' # And we want to run this in our cloud function directory
```
Registering more functions could easily be done by copy pasting this block and changing things as needed.
**Will overwrite functions if they already exist in the Cloud Project** 

## Potential TODOs
- Make it so that Cloud Build will **only** do a build if it has to, instead of rebuilding on changes to things like READMEs
- Tests ran on Google Cloud, on top of GitHub actions
- Research whether there's a less 'full on' way to provision Cloud Resources in code than [Terraform](https://www.terraform.io/) (although Terraform is probably fine)
