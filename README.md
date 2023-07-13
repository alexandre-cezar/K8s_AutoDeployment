= K8s_AutoDeployment

This application automates the deployment of a task for users who cannot use a pipeline for automated deployments.

It can download the YAML file from a given URL (outbound proxy connection is supported) or use a local YAML file as input.

Up to 3 different YAML files are supported in a single run.

Multiple clusters can be supported by providing different kube credentials (multiple kube credentials in a single file are not supported).

If a new namespace must be created as part of the deployment, it can be passed as an argument. If the deployment is being made for an existing namespace, just specify the namespace in the YAML file directly.

== Usage

[source, bash]
----
K8s_Auto_Deployment.py [-h] (--urls URLS [URLS ...] | --paths PATHS [PATHS ...]) [--auth AUTH] [--proxy PROXY] [--proxy-auth PROXY_AUTH]
                              --kubeconfigs KUBECONFIGS [KUBECONFIGS ...] [--namespace NAMESPACE]
----

=== Optional Arguments

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

