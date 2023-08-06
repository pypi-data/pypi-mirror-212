
# Awsume Bitwarden Plugin

> The initial code was copied from [xeger](https://github.com/xeger/awsume-bitwarden-plugin). Thanks for this great starting point ❤️

_Awsume 4+ only_.

This is a plugin that automates the entry of MFA tokens using Bitwarden.
It fetches the totp token automatically from your Bitwarden vault.

## Support

If you experience any problems, please [file a bug report](https://github.com/danto7/awsume-bitwarden-plugin/issues/new?assignees=xeger&template=bug_report.md).

## Installation

### Install This Plugin

```
pip3 install awsume-bitwarden-plugin
```

If you've installed awsume with `pipx`, this will install the console plugin in awsume's virtual environment:

```
pipx inject awsume awsume-bitwarden-plugin
```

### Requirements

* bitwarden cli
* bitwarden needs to be unklocked and the session token has to be in the `BW_SESSION` env variable

### Configure AWSume

This plugin needs to know which bitwarden vault item to use for each MFA token.
You can specify the arn of the mfa device as an additional uri in your bitwarden item.


## Troubleshooting

If you experience any trouble, invoke `awsume` with the `--debug` flag and look for log entries that contain `bitwarden`.

The specific command that this plugin invokes is `bw get totp "mfa device arn here"`; make sure it succeeds without prompting a password when you invoke it manually.

If you can't solve your problem, [create a GitHub issue](https://github.com/danto7/awsume-bitwarden-plugin/issues/new) with diagnostic details and we'll try to help you.
