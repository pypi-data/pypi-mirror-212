'''
<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg" alt="Apache 2.0 License"></a>
  <a href="https://www.npmjs.com/package/cdktf-gke-auth"><img src="https://badge.fury.io/js/cdktf-gke-auth.svg" alt="npm version"></a>
  <a href="https://github.com/01walid/cdktf-gke-auth/actions/workflows/build.yml"><img src="https://github.com/01walid/cdktf-gke-auth/actions/workflows/build.yml/badge.svg" alt="Build badge"></a>
  <a href="https://github.com/01walid/cdktf-gke-auth/actions/workflows/release.yml"><img src="https://github.com/01walid/cdktf-gke-auth/actions/workflows/release.yml/badge.svg" alt="Release badge"></a>
</p>

# cdktf-gke-auth

Easily authenticate against a Google Kubernetes Engine (GKE) within your CDK for Terraform stack. Without the need to
resort to [Google's terraform GKE auth](https://github.com/terraform-google-modules/terraform-google-kubernetes-engine/tree/v26.1.1/modules/auth) module. You can avoid running `cdktf get` as pre-synth step.

## Example usage (Typescript)

Install the construct with: `yarn install cdktf-gke-auth`.

```python
import { GoogleProvider } from "@cdktf/provider-google/lib/provider";
import { TerraformOutput, TerraformStack } from "cdktf";
import { Construct } from "constructs";
import { GKEAuth } from 'cdktf-gke-auth';

export class MyKubeStack extends TerraformStack {
  constructor(scope: Construct, name: string) {
    super(scope, name);

    new GoogleProvider(this, "google-provider", {});

    const auth = new GKEAuth(this, "gke-auth", {
      clusterName: "my-cluster",
      location: "europe-west1",
      projectId: "my-project",
    });

    // init the Kubernetes provider like so:
    // new KubernetesProvider(this, "kubernetes", {
    //   ...auth.authCredentials
    // });

    // Or a helm provider like so:
    //  new HelmProvider(this, "helm", {
    //   kubernetes: auth.authCredentials,
    // });
  }
}
```

The `GKEAuth` instance expose `host`, `clusterCaCertificate`, `clusterCaCertificatePEM`, and `token` you can use to authenticate using
any of the kubernetes popular cdktf providers.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import cdktf as _cdktf_9a9027ec
import cdktf_cdktf_provider_google.data_google_client_config as _cdktf_cdktf_provider_google_data_google_client_config_6cd2ae20
import cdktf_cdktf_provider_google.data_google_container_cluster as _cdktf_cdktf_provider_google_data_google_container_cluster_6cd2ae20
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdktf-gke-auth.AuthCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_ca_certificate": "clusterCaCertificate",
        "host": "host",
        "token": "token",
    },
)
class AuthCredentials:
    def __init__(
        self,
        *,
        cluster_ca_certificate: builtins.str,
        host: builtins.str,
        token: builtins.str,
    ) -> None:
        '''
        :param cluster_ca_certificate: 
        :param host: 
        :param token: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba90e7c257be36144934039cc0a19d9ef6cf64b1c94e73ca1a7334437127b3ac)
            check_type(argname="argument cluster_ca_certificate", value=cluster_ca_certificate, expected_type=type_hints["cluster_ca_certificate"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_ca_certificate": cluster_ca_certificate,
            "host": host,
            "token": token,
        }

    @builtins.property
    def cluster_ca_certificate(self) -> builtins.str:
        result = self._values.get("cluster_ca_certificate")
        assert result is not None, "Required property 'cluster_ca_certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> builtins.str:
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_cdktf_9a9027ec.ITerraformDependable)
class GKEAuth(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-gke-auth.GKEAuth",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster_name: builtins.str,
        location: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_name: 
        :param location: 
        :param project_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71514e77038348f5442dde297a2d25dd17d9df0eabb64fc9c335dc5902ded582)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GkeControlPlaneProps(
            cluster_name=cluster_name, location=location, project_id=project_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authCredentials")
    def auth_credentials(self) -> AuthCredentials:
        return typing.cast(AuthCredentials, jsii.get(self, "authCredentials"))

    @builtins.property
    @jsii.member(jsii_name="clientConfig")
    def client_config(
        self,
    ) -> _cdktf_cdktf_provider_google_data_google_client_config_6cd2ae20.DataGoogleClientConfig:
        return typing.cast(_cdktf_cdktf_provider_google_data_google_client_config_6cd2ae20.DataGoogleClientConfig, jsii.get(self, "clientConfig"))

    @builtins.property
    @jsii.member(jsii_name="clusterCaCertificate")
    def cluster_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCaCertificate"))

    @builtins.property
    @jsii.member(jsii_name="clusterCaCertificatePEM")
    def cluster_ca_certificate_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCaCertificatePEM"))

    @builtins.property
    @jsii.member(jsii_name="clusterInfo")
    def cluster_info(
        self,
    ) -> _cdktf_cdktf_provider_google_data_google_container_cluster_6cd2ae20.DataGoogleContainerCluster:
        return typing.cast(_cdktf_cdktf_provider_google_data_google_container_cluster_6cd2ae20.DataGoogleContainerCluster, jsii.get(self, "clusterInfo"))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="kubeConfigRaw")
    def kube_config_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeConfigRaw"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="cdktf-gke-auth.GkeControlPlaneProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "location": "location",
        "project_id": "projectId",
    },
)
class GkeControlPlaneProps:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        location: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param cluster_name: 
        :param location: 
        :param project_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ff4487bf931715058231b7757c5544cdc0826cb62ded6e7e2bca28c1dc6b8f)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "location": location,
            "project_id": project_id,
        }

    @builtins.property
    def cluster_name(self) -> builtins.str:
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeControlPlaneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AuthCredentials",
    "GKEAuth",
    "GkeControlPlaneProps",
]

publication.publish()

def _typecheckingstub__ba90e7c257be36144934039cc0a19d9ef6cf64b1c94e73ca1a7334437127b3ac(
    *,
    cluster_ca_certificate: builtins.str,
    host: builtins.str,
    token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71514e77038348f5442dde297a2d25dd17d9df0eabb64fc9c335dc5902ded582(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster_name: builtins.str,
    location: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ff4487bf931715058231b7757c5544cdc0826cb62ded6e7e2bca28c1dc6b8f(
    *,
    cluster_name: builtins.str,
    location: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
