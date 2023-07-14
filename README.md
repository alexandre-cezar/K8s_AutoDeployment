# K8s_AutoDeployment

This application automates the deployment of a task for users who cannot use a CI/CD pipeline to manage their deployments.

The app can download a YAML file from a given URL (outbound proxy connection is supported) or simply use a local YAML file as input.

Up to 3 different YAML files are supported in a single run.

One or multiple clusters can be target of a single deployment by providing different kube credentials for each cluster to the program (note: multiple kube credentials in a single file are not supported).

If a new namespace must be created as part of the deployment task, this can also be passed as an argument. If the deployment is being made for an existing namespace, just specify the target namespace in the YAML file directly.

# Usage

K8s_Auto_Deployment.py [-h] (--urls URLS [URLS ...] | --paths PATHS [PATHS ...]) [--auth AUTH] [--proxy PROXY] [--proxy-auth PROXY_AUTH]
                              --kubeconfigs KUBECONFIGS [KUBECONFIGS ...] [--namespace NAMESPACE]

# Arguments

-h, --help::
  Show this help message and exit.

--urls URLS [URLS ...]::
  URLs where to download YAML files from.

--auth AUTH::
  Username:password for basic URL authentication.

--proxy PROXY::
  Proxy address:port.

--proxy-auth PROXY_AUTH::
  Username:password for proxy authentication.

--paths PATHS [PATHS ...]::
  Paths to local YAML files (maximum of 3).

--kubeconfigs KUBECONFIGS [KUBECONFIGS ...]::
  Paths to kubeconfig files.

--namespace NAMESPACE::
  Namespace to be created before the YAML file is executed (optional).

