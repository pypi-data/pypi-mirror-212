#!/usr/bin/env python
import argparse
import os

import yaml

import json


def json_to_github_actions(json_data, cli_params=None):
    json_dict = json.loads(json_data)

    actions_base_structure = {
        "name": "JSON to GitHub Actions YAML",
        "on": "workflow_dispatch",
        "jobs": {}
    }

    def create_execution_environment_jobs(execution_environments):
        job_name_base = "setup_environment_"
        job_number = 1
        jobs = {}

        for env in execution_environments:
            job_name = job_name_base + str(job_number)
            job_number += 1

            if env["language"] == "python":
                install_command = f"python -m pip install -r requirements.txt"
                language_command = f"python {json_dict['script_name']}"
            elif env["language"] == "julia":
                install_command = f"julia -e 'import Pkg; Pkg.add([\"CSV\", \"DataFrames\", \"ZipFile\", \"CodecZlib\", \"Dates\", \"GZip\", \"HTTP\", \"JSON\", \"ArgParse\"])'"
                language_command = f"julia {json_dict['script_name']}"

            steps_params_run = ''
            for parameters in json_dict["json_parameters"]:
                param_str = []
                for key, value in parameters.items():
                    param_str.append(f'--{key} "${{{{ matrix.parameters.{key} }}}}"')
                steps_params_run += ' '.join(param_str) + os.linesep
                break

            job_details = {
                "runs-on": "ubuntu-latest",
                "strategy": {
                    "max-parallel": int(json_dict["max_parallel"]),
                    "matrix": {"parameters": json_dict["json_parameters"]}
                },
                "steps": [
                    {
                        "name": f"Checkout repository and setup {env['language']} environment",
                        "uses": "actions/checkout@v3",
                        "with": {
                            "repository": json_dict["repo_url"].replace("https://github.com/", ""),
                            "ref": "main"
                        }
                    },
                ]
            }
            if env["language"] == "python":
                job_details["steps"].append({
                    "name": "SetUp Python",
                    "uses": "actions/setup-python@v4",
                    "with": {
                        "python-version": env["version"]
                    }
                })
            elif env["language"] == "julia":
                job_details["steps"].append({
                    "name": "Set up Julia",
                    "uses": "julia-actions/setup-julia@v1",
                    "with": {
                        "version": env["version"]
                    }
                })
            job_details["steps"].append({
                "name": "Run script",
                "run": f"{install_command} && cd {json_dict['script_dir'].strip('/')} && {language_command} {steps_params_run}"
            })
            job_details["steps"].append({
                "name": "Upload artifact",
                "uses": "actions/upload-artifact@v3",
                "with": {
                    "name": f'id_${{{{github.run_id}}}}',
                    "path": json_dict['output_directory']
                }
            })
            jobs[job_name] = job_details
        return jobs

    execution_environment_jobs = create_execution_environment_jobs(json_dict["execution_environment"])
    actions_base_structure["name"] = json_dict['script_name'].split('.')[0] + '.yml'
    actions_base_structure["jobs"].update(execution_environment_jobs)

    yaml_data = yaml.dump(actions_base_structure, sort_keys=False)

    # ensure the directory of yaml_file exists
    if cli_params is not None:
        if os.path.dirname(cli_params.yaml_file) != '':
            os.makedirs(os.path.dirname(cli_params.yaml_file), exist_ok=True)

    return yaml_data


def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert JSON to a GitHub Actions YAML file.")
    parser.add_argument("--json_file", type=str, help="Path to the input JSON file.", required=True)
    parser.add_argument("--yaml_file", type=str, help="Path to the output YAML file.", required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()

    with open(args.json_file, "r") as f:
        json_data = f.read()

    yaml_data = json_to_github_actions(json_data, args)

    with open(args.yaml_file, "w") as f:
        f.write(yaml_data)


if __name__ == "__main__":
    main()
