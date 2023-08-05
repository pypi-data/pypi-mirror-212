'''
# CDK NAT ASG Provider

![npm version](https://img.shields.io/npm/v/cdk-nat-asg-provider)
![PyPi version](https://img.shields.io/pypi/v/cdk-nat-asg-provider)
![Release](https://github.com/fonzcastellanos/cdk-nat-asg-provider/workflows/release/badge.svg)
![License](https://img.shields.io/github/license/fonzcastellanos/cdk-nat-asg-provider)

Use this [AWS Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/v2/guide/home.html) library to configure and deploy [network address translation (NAT) instances](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_NAT_Instance.html) individually within their own [auto scaling group (ASG)](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html) to improve reliability and availability.

Works with AWS CDK <strong>v2</strong>.

## Problem

Although the [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) offered by AWS have high availability, high bandwidth scalability, and minimal administration needs, they can be too expensive for small scale applications. A cheaper alternative, one that AWS mentions in its documentation but does not recommend, is to configure and manage your own NAT instances. One way of doing this is with the CDK using [`NatInstanceProvider`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.NatInstanceProvider.html).

```python
import { aws_ec2 as ec2 } from 'aws-cdk-lib';

// Factory method constructs and configures a `NatInstanceProvider` object
const provider = ec2.NatProvider.instance({
  instanceType: new ec2.InstanceType('t2.micro'),
});

const vpc = new ec2.Vpc(this, 'Vpc', {
  natGatewayProvider: provider,
});
```

A major downside of this approach is that the created NAT instances will not be automatically replaced if they are stopped for whatever reason.

## Solution

To provide better fault tolerance and availability, I implemented a NAT provider called `NatAsgProvider` that places each created NAT instance in its own ASG.

```python
import { aws_ec2 as ec2 } from 'aws-cdk-lib';
import { NatAsgProvider } from 'cdk-nat-asg-provider';

const provider = new NatAsgProvider({});

const vpc = new ec2.Vpc(this, 'Vpc', {
  natGatewayProvider: provider,
});
```

Like `NatInstanceProvider`, `NatAsgProvider` extends [`NatProvider`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.NatProvider.html).

## How it works

The number of NAT instances to create and the placement of those NAT instances is dictated by the configuration of the relevant `VPC` object using the following configuration properties provided to the `VPC` constructor:

* [`natGatewaySubnets`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html#natgatewaysubnets)

  * Selects the subnets that will have NAT instances
  * By default, all public subnets are selected
* [`natGateways`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html#natgateways)

  * The number of NAT instances to create
  * By default, one NAT instance per AZ

At a high-level, this is how `NatAsgProvider` achieves its purpose:

* Enables NAT in the EC2 instances, which are running Amazon Linux 2
* Places each NAT instance in its own ASG, configured by a [launch template](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-templates.html)
* Uses [`cfn-signal`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-signal.html) in conjunction with a [`CreationPolicy`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-creationpolicy.html) and [`UpdatePolicy`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html) to suspend work on the stack until the NAT instance signals successful creation or update, respectively, of its ASG
* Attaches an additional [elastic network interface (ENI)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) to each NAT instance

  * Each of these ENI is assigned an [elastic IP (EIP) address](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)
  * Sets the default gateway to be the newly attached ENI

## Installation

### TypeScript (npm)

```shell
npm install cdk-nat-asg-provider
```

or

```shell
yarn install cdk-nat-asg-provider
```

### Python (PyPI)

```shell
pip install cdk-nat-asg-provider
```

## Usage

For general usage, check out the [API documentation](API.md).

### Example: Manual testing of NAT configuration

I implemented a test environment similar to the one described in the [AWS VPC docs](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_NAT_Instance.html#nat-test-configuration). It allows you to manually check whether instances in private subnets can access the internet through the NAT instances by using the NAT instances as bastion servers.

The implementation is in [src/manual.integ.ts](src/manual.integ.ts). It's worth taking a look if you're confused about how to configure `Vpc` and `NatAsgProvider`.

To **deploy** the manual integration test, execute the `sh` script `scripts/manual-integ-test` and use the `deploy` command:

```shell
./scripts/manual-integ-test deploy <ACCOUNT> <AWS_REGION> <KEY_PAIR_NAME> [MAX_AZS]
```

`MAX_AZS` is optional.

To **destroy** the manual integration test, execute the same script with same arguments using the `destroy` command:

```shell
./scripts/manual-integ-test destroy <ACCOUNT> <AWS_REGION> <KEY_PAIR_NAME> [MAX_AZS]
```

## Project configuration via `projen`

[`projen`](https://github.com/projen/projen) synthesizes and maintains project configuration. Most of the configuration files, such as `package.json`, `.gitignore`, and those defining Github Actions workflows, are managed by `projen` and are read-only. To add, remove, or modify configuration files, edit [`.projenrc.js`](.projenrc.js) and then run `npx projen`. Check out `projen`'s [documentation website](https://projen.io) for more details.

## Contributing

Feel free to open issues to report bugs or suggest features. Contributions via pull requests are much appreciated.

## License

Released under the [Apache 2.0](LICENSE) license.
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable)
class NatAsgProvider(
    _aws_cdk_aws_ec2_ceddda9d.NatProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nat-asg-provider.NatAsgProvider",
):
    '''(experimental) ``NatAsgProvider`` is a NAT provider that places each NAT instance in its own auto scaling group to improve fault tolerance and availability.

    ``NatAsgProvider`` extends ``NatProvider``:

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.NatProvider.html
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        key_pair: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        traffic_direction: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatTrafficDirection] = None,
    ) -> None:
        '''
        :param instance_type: (experimental) The EC2 instance type of the NAT instances. Default: t2.micro
        :param key_pair: (experimental) The name of the SSH key pair granting access to the NAT instances.
        :param security_group: (experimental) The security group associated with the NAT instances. Default: A security group will be created.
        :param traffic_direction: (experimental) The allowed traffic directions through the NAT instances. If you set this to a value other than ``ec2.NatTrafficDirection.INBOUND_AND_OUTBOUND``, you must configure the security group for the NAT instances either by providing a fully configured security group through the ``securityGroup`` property or by using the ``NatAsgProvider`` object's ``securityGroup`` or ``connections`` properties after passing the ``NatAsgProvider`` object to a ``Vpc`` object. Default: ``aws-cdk-lib.aws_ec2.NatTrafficDirection.INBOUND_AND_OUTBOUND``

        :stability: experimental
        '''
        props = NatAsgProviderProps(
            instance_type=instance_type,
            key_pair=key_pair,
            security_group=security_group,
            traffic_direction=traffic_direction,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="configureNat")
    def configure_nat(
        self,
        *,
        nat_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
        private_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''(experimental) Called by the VPC to configure NAT.

        Don't call this directly, the VPC will call it automatically.

        :param nat_subnets: The public subnets where the NAT providers need to be placed.
        :param private_subnets: The private subnets that need to route through the NAT providers. There may be more private subnets than public subnets with NAT providers.
        :param vpc: The VPC we're configuring NAT for.

        :stability: experimental
        '''
        opts = _aws_cdk_aws_ec2_ceddda9d.ConfigureNatOptions(
            nat_subnets=nat_subnets, private_subnets=private_subnets, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "configureNat", [opts]))

    @jsii.member(jsii_name="configureSubnet")
    def configure_subnet(self, subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet) -> None:
        '''(experimental) Configures subnet with the gateway.

        Don't call this directly, the VPC will call it automatically.

        :param subnet: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184a627c1e0d161db9765df0020e6448bbbdc653d1716896f093911988882812)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(None, jsii.invoke(self, "configureSubnet", [subnet]))

    @builtins.property
    @jsii.member(jsii_name="configuredGateways")
    def configured_gateways(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig]:
        '''(experimental) Return list of gateways spawned by the provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig], jsii.get(self, "configuredGateways"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with the security group of the NAT instances.

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Connections.html
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''(experimental) The security group associated with the NAT instances.

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.ISecurityGroup.html
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))


@jsii.data_type(
    jsii_type="cdk-nat-asg-provider.NatAsgProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "key_pair": "keyPair",
        "security_group": "securityGroup",
        "traffic_direction": "trafficDirection",
    },
)
class NatAsgProviderProps:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        key_pair: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        traffic_direction: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatTrafficDirection] = None,
    ) -> None:
        '''(experimental) Properties to configure ``NatAsgProvider``.

        :param instance_type: (experimental) The EC2 instance type of the NAT instances. Default: t2.micro
        :param key_pair: (experimental) The name of the SSH key pair granting access to the NAT instances.
        :param security_group: (experimental) The security group associated with the NAT instances. Default: A security group will be created.
        :param traffic_direction: (experimental) The allowed traffic directions through the NAT instances. If you set this to a value other than ``ec2.NatTrafficDirection.INBOUND_AND_OUTBOUND``, you must configure the security group for the NAT instances either by providing a fully configured security group through the ``securityGroup`` property or by using the ``NatAsgProvider`` object's ``securityGroup`` or ``connections`` properties after passing the ``NatAsgProvider`` object to a ``Vpc`` object. Default: ``aws-cdk-lib.aws_ec2.NatTrafficDirection.INBOUND_AND_OUTBOUND``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af8ce722e82004ed6755c9f667c245b1a2dc875c9cc9a1fe59b9036173984d9)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument traffic_direction", value=traffic_direction, expected_type=type_hints["traffic_direction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if security_group is not None:
            self._values["security_group"] = security_group
        if traffic_direction is not None:
            self._values["traffic_direction"] = traffic_direction

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The EC2 instance type of the NAT instances.

        :default: t2.micro

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.InstanceType.html
        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the SSH key pair granting access to the NAT instances.

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
        :stability: experimental
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The security group associated with the NAT instances.

        :default: A security group will be created.

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.ISecurityGroup.html
        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def traffic_direction(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatTrafficDirection]:
        '''(experimental) The allowed traffic directions through the NAT instances.

        If you set this to a value other than
        ``ec2.NatTrafficDirection.INBOUND_AND_OUTBOUND``, you must
        configure the security group for the NAT instances either by providing
        a fully configured security group through the ``securityGroup`` property
        or by using the ``NatAsgProvider`` object's ``securityGroup`` or
        ``connections`` properties after passing the ``NatAsgProvider`` object to a
        ``Vpc`` object.

        :default: ``aws-cdk-lib.aws_ec2.NatTrafficDirection.INBOUND_AND_OUTBOUND``

        :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.NatTrafficDirection.html
        :stability: experimental
        '''
        result = self._values.get("traffic_direction")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatTrafficDirection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NatAsgProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NatAsgProvider",
    "NatAsgProviderProps",
]

publication.publish()

def _typecheckingstub__184a627c1e0d161db9765df0020e6448bbbdc653d1716896f093911988882812(
    subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af8ce722e82004ed6755c9f667c245b1a2dc875c9cc9a1fe59b9036173984d9(
    *,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    key_pair: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    traffic_direction: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatTrafficDirection] = None,
) -> None:
    """Type checking stubs"""
    pass
