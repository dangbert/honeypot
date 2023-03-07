#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import json
from typing import List
import shutil

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__)) 
INSTANCES_DIR = os.path.join(SCRIPT_DIR, 'instances')
DOCKER_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../docker'))

def main():
    parser = argparse.ArgumentParser(description="Easily update/manage site deployments.")
    parser.add_argument('instance', type=str, help="Name of folder in terraform/instances/ (e.g. 'example')")

    parser.add_argument('-b', '--build', action="store_true", help="build docker image")
    parser.add_argument('-p', '--push', action="store_true", help="push docker image to server, and restart website")
    parser.add_argument('--ssh', action="store_true", help="ssh into server")
    #parser.add_argument('-s', '--stop', action="store_true", help="stop EC2 instance")

    args = parser.parse_args()

    # allow args.instance to be absolute path or just name of folder e.g. "example"
    tfDir = os.path.abspath(os.path.join(INSTANCES_DIR, args.instance))
    if os.path.samefile(os.path.abspath(os.path.join(args.instance, '..')), INSTANCES_DIR):
        tfDir = os.path.abspath(args.instance)
    print(f"using terraform dir: '{tfDir}'\n")
    assert os.path.isdir(tfDir)

    data = getTfOutput(tfDir)

    ops = 0 # num operations performed
    if args.build:
        ensureEnv(DOCKER_DIR)
        print(f"building docker image...")
        runCmd(['sudo', 'docker-compose', 'build'], cwd=DOCKER_DIR)
        print(f"exporting image to tar file...")
        runCmd(['sudo', 'docker', 'image', 'save', 'honey_flask', '-o', 'image.tar'], cwd=DOCKER_DIR)
        runCmd(['sudo', 'chmod', '664', 'image.tar'], cwd=DOCKER_DIR)
        ops += 1

    if args.push:
        fname = os.path.join(DOCKER_DIR, 'image.tar')
        assert(os.path.exists(fname))
        print(f"copying to server: '{fname}'")
        print(f"copying docker resources to server...\n")
        # copy just image.tar
        #runCmd(['scp', '-i', data['ssh']['key'], fname, f"{data['ssh']['remote']}:"], cwd=tfDir)

        # copy entire docker directory (TODO: better to rsync https://unix.stackexchange.com/a/127355)
        runCmd(['scp', '-i', data['ssh']['key'], '-r', DOCKER_DIR, f"{data['ssh']['remote']}:"], cwd=tfDir)
        ops += 1

    if args.ssh:
        # TODO: not currently working (terminal output not visible)
        print(f"this command isn't fully supported, but you can manually run:")
        runCmd(['ssh', '-i', data['ssh']['key'], data['ssh']['remote']], cwd=tfDir, verbose=True, dryRun=True)
        ops += 1

    if ops == 0:
        parser.print_help(sys.stderr)
        exit(1)
    print(f"\ndeploy.sh successfully finished {ops} operation(s)!")

def getTfOutput(tfDir: str):
    rawOut = subprocess.getoutput(f"cd '{tfDir}' && terraform output -json")
    return json.loads(rawOut)['data']['value']


def runCmd(cmd: List[str], cwd='.', verbose=False, dryRun=False):
    """Run a shell command, returning the exitcode."""
    if verbose or dryRun:
        print(
            f"\n{'running' if not dryRun else 'would run'} command:"
        )
        print(" ".join(cmd))
    if dryRun:
        return

    res = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=cwd)
    if res.returncode != 0:
        print(f"***command failed with code {res.returncode}")
        print(" ".join(cmd))
    return res.returncode

def ensureEnv(dockerDir: str):
    """Ensure .env file exists"""
    envPath = os.path.join(dockerDir, '.env')
    if os.path.exists(envPath):
        return

    templateEnv = os.path.join(dockerDir, '.env.sample')
    assert os.path.exists(templateEnv)

    shutil.copy(templateEnv, envPath)
    print(f"\ncreated default .env file: '{envPath}'")
    input("Edit this file if desired then press Enter to continue...")

        
if __name__ == "__main__":
    main()
