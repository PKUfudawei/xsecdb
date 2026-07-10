#!/usr/bin/env python3
import os
from tqdm import tqdm


def generate_condor_scripts(executable_dir='./executable', condor_dir='./condor'):
    if not os.path.exists('./genXsec_cfg.py'):
        os.system("wget https://raw.githubusercontent.com/cms-sw/genproductions/refs/heads/master/Utilities/calculateXSectionAndFilterEfficiency/genXsec_cfg.py")

    condor_dir = os.path.abspath(condor_dir)
    for sub_dir in ('submit', 'log', 'error', 'output'):
        os.makedirs(os.path.join(condor_dir, sub_dir), exist_ok=True)

    executable_scripts = os.listdir(executable_dir)
    for executable_script in tqdm(executable_scripts, desc="Generating condor submit files"):
        process_name = executable_script.split('.')[0]
        executable_script = os.path.abspath(os.path.join(executable_dir, executable_script))
        submit_file = os.path.abspath(os.path.join(condor_dir, f"submit/{process_name}.submit"))

        with open(submit_file, 'w+', encoding='utf-8') as f:
            f.write('\n'.join([
                "universe = vanilla",
                "+JobFlavour = testmatch",
                f"JobBatchName = {process_name}",
                "use_x509userproxy = true",
                f"executable = {executable_script}",
                "should_transfer_files = YES",
                "when_to_transfer_output = ON_EXIT_OR_EVICT",
                f"transfer_input_files = {os.path.abspath('./genXsec_cfg.py')}",
                'transfer_output_files = ""',
                f"error = {submit_file.replace('submit', 'error')}",
                f"output = {submit_file.replace('submit', 'output')}",
                f"log = {submit_file.replace('submit', 'log')}",
                "queue 1",
            ]))


def submit_condor_jobs(submit_dir='./condor/submit'):
    for submit_file in tqdm(os.listdir(submit_dir), desc=f"Submitting all jobs under {submit_dir}"):
        os.system(f"condor_submit {os.path.join(submit_dir, submit_file)} &> /dev/null")


if __name__ == "__main__":
    generate_condor_scripts()
    submit_condor_jobs()
