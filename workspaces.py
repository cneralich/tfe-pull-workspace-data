def get_workspace_data(hostname, organization, USER_TOKEN):
    import requests
    import json

    headers = {"Authorization": "Bearer %s" % (USER_TOKEN)}

    workspaces_url = "https://%s/api/v2/organizations/%s/workspaces" % (hostname, organization)
    get_workspaces = requests.get(url=workspaces_url, headers=headers)
    format_workspaces_data = json.loads(get_workspaces.content)
    workspaces = format_workspaces_data.get("data")

    for workspace in workspaces:
        try:
            # Pull Workspace Data
            workspace_id = workspace.get("id")
            workspace_name = workspace.get("attributes").get("name")
            latest_run = workspace.get("relationships").get("latest-run").get("data").get("id")
            current_state = workspace.get("relationships").get("current-state-version").get("data").get("id")

            # Pull Runs Data
            runs_url = "https://app.terraform.io/api/v2/runs/%s" % (latest_run)
            get_runs = requests.get(url=runs_url, headers=headers)
            format_runs_data = json.loads(get_runs.content)
            status = format_runs_data.get("data").get("attributes").get("status")
            status_timestamps = format_runs_data.get("data").get("attributes").get("status-timestamps")

            # Pull State Data
            states_url = "https://app.terraform.io/api/v2/workspaces/%s/current-state-version" % (workspace_id)
            get_states = requests.get(url=states_url, headers=headers)
            format_states_data = json.loads(get_states.content)
            state_created_at = format_states_data.get("data").get("attributes").get("created-at")
            download_url = format_states_data.get("data").get("attributes").get("hosted-state-download-url")
            version = format_states_data.get("data").get("attributes").get("serial")
            vcs_commit_url = format_states_data.get("data").get("attributes").get("vcs-commit-url")
            vcs_commit_sha = format_states_data.get("data").get("attributes").get("vcs-commit-sha")

            print "WORKSPACE NAME: %s\nSTATUS: %s\nTIMESTAMPS: %s\nSTATE CREATED AT: %s\nSTATE DOWNLOAD: %s\nSTATE VERSION: %s\nVCS COMMIT: %s\nVCS SHA: %s\n" % (workspace_name, status, status_timestamps, state_created_at, download_url, version, vcs_commit_url, vcs_commit_sha)
        except:
            print "WORKSPACE NAME: %s\nSTATUS: NO RUNS OR STATE\n" % (workspace_name)

# To call the above, you just need to pass the required values.  For example:
# get_workspace_data("app.terraform.io", "my-tfe-organization", "xxxxxxxx.atlasv1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
