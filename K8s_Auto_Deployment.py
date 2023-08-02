#Author - Alexandre S. Cezar
import argparse
import os
import subprocess
import requests
import time

def download_defender(url, auth=None, proxy=None, proxy_auth=None, verify=True):
    headers = {}
    if auth:
        headers['Authorization'] = 'Basic ' + auth
    proxies = {}
    if proxy:
        proxies['http'] = proxy
        proxies['https'] = proxy
        if proxy_auth:
            proxies['http'] = 'http://' + proxy_auth + '@' + proxy
            proxies['https'] = 'https://' + proxy_auth + '@' + proxy

    # Create a requests Session and set SSL certificate verification
    session = requests.Session()
    session.verify = verify

    # Make the request using the Session
    response = session.get(url, headers=headers, proxies=proxies)
    response.raise_for_status()
    return response.content

def connect_to_cluster(kubeconfig):
    os.environ['KUBECONFIG'] = kubeconfig

def create_namespace(namespace):
    subprocess.run(['kubectl', 'create', 'namespace', namespace])

def apply_yaml_file(filename, namespace):
    subprocess.run(['kubectl', 'apply', '-f', filename, '-n', namespace])

def get_pods(namespace):
    subprocess.run(['kubectl', 'get', 'pods', '-n', namespace])

def disconnect_from_cluster():
    os.environ.pop('KUBECONFIG', None)

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--urls', nargs='+', help='URLs to download YAML files from')
    group.add_argument('--paths', nargs='+', help='Paths to local YAML files (maximum of 3)')
    parser.add_argument('--auth', help='Username:password for authentication')
    parser.add_argument('--proxy', help='Proxy address:port')
    parser.add_argument('--proxy-auth', help='Username:password for proxy authentication')
    parser.add_argument('--kubeconfigs', required=True, nargs='+', help='Paths to kubeconfig files')
    parser.add_argument('--namespace', help='Namespace name for YAML file')
    args = parser.parse_args()

    # Step 1: Validate the number of YAML files
    if args.paths and len(args.paths) > 3:
        print("Error: Maximum of 3 YAML files can be specified.")
        return

    # Step 2: Download or read YAML contents
    yaml_contents = []
    if args.urls:
        for url in args.urls:
            yaml_content = download_defender(url, args.auth, args.proxy, args.proxy_auth)
            yaml_contents.append(yaml_content)
    elif args.paths:
        for path in args.paths:
            with open(path, 'rb') as file:
                yaml_contents.append(file.read())

    # Step 3: Iterate over kubeconfigs and apply YAML files to clusters
    for kubeconfig in args.kubeconfigs:
        print(f"Processing kubeconfig: {kubeconfig}")
        print("----------------------------------")

        # Step 3.1: Connect to the Kubernetes cluster
        connect_to_cluster(kubeconfig)

        # Step 3.2: Create namespace if provided
        if args.namespace:
            create_namespace(args.namespace)

        # Step 3.3: Apply YAML files to the cluster
        for i, yaml_content in enumerate(yaml_contents):
            with open('temp.yaml', 'wb') as file:
                file.write(yaml_content)
            apply_yaml_file('temp.yaml', args.namespace)

            # Step 3.4: Sleep for 20 seconds before displaying the "kubectl get pods" output
            time.sleep(20)

            # Step 3.5: Get pods in the namespace
            get_pods(args.namespace)

            # Print separator between YAML files
            print("----------------------------------")

        # Step 3.6: Disconnect from the Kubernetes cluster
        disconnect_from_cluster()

        # Print separator between clusters
        print("----------------------------------")

        # Sleep for 10 seconds before processing the next cluster
        time.sleep(10)

    # Clean up temporary file
    os.remove('temp.yaml')

if __name__ == '__main__':
    main()



