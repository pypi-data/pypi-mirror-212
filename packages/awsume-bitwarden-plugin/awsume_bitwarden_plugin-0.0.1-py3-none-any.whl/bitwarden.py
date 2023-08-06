import argparse
import colorama
import traceback
import sys

from subprocess import Popen, PIPE

from awsume.awsumepy import hookimpl, safe_print
from awsume.awsumepy.lib import profile
from awsume.awsumepy.lib.logger import logger


# Truncate proxied subprocess output to avoid stack trace spam
MAX_OUTPUT_LINES = 2


def get_mfa_serial(profiles, target_name):
    mfa_serial = profile.get_mfa_serial(profiles, target_name)
    if not mfa_serial:
        logger.debug("No MFA required")
    return mfa_serial


def get_otp(title):
    with Popen(
        ["bw", "--raw", "--nointeraction", "get", "totp", title],
        stdout=PIPE,
        stderr=PIPE,
    ) as op:
        if op.stderr is None or op.stdout is None:
            raise ValueError("could not read stdout or stderr")

        linecount = 0
        while True:
            msg = op.stderr.readline().decode()

            if msg == "" and op.poll() is not None:
                break
            elif msg != "" and linecount < MAX_OUTPUT_LINES:
                safe_print("bitwarden: " + msg, colorama.Fore.RED)
                linecount += 1
            else:
                logger.debug(msg.strip("\n"))
        if op.returncode != 0:
            return None

        return op.stdout.readline().decode().strip("\n")


# Find canonical profile name (e.g. with fuzzy matching rules).
def canonicalize(config, profiles, name):
    target_name = profile.get_profile_name(config, profiles, name, log=False)
    if profiles.get(target_name) is not None:
        return target_name
    else:
        return None


# Print sad message to console with instructions for filing a bug report.
# Log stack trace to stderr in lieu of safe_print.
def handle_crash():
    safe_print(
        "Error invoking bitwarden plugin; please file a bug report:\n  %s"
        % ("https://github.com/danto7/awsume-bitwarden-plugin/issues/new/choose"),
        colorama.Fore.RED,
    )
    traceback.print_exc(file=sys.stderr)


@hookimpl
def pre_get_credentials(config: dict, arguments: argparse.Namespace, profiles: dict):
    try:
        target_profile_name = canonicalize(
            config, profiles, arguments.target_profile_name
        )
        if target_profile_name is not None:
            mfa_serial = get_mfa_serial(profiles, target_profile_name)
            if mfa_serial and not arguments.mfa_token:
                arguments.mfa_token = get_otp(mfa_serial)
                if arguments.mfa_token:
                    safe_print(
                        "Obtained MFA token from bitwarden item: %s" % (mfa_serial),
                        colorama.Fore.CYAN,
                    )
    except Exception:
        handle_crash()
