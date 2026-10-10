
import subprocess
import sys


def run_command(command):
    """Run a command and display its output."""
    print("\n" + "=" * 60)
    print("COMMAND:", " ".join(command))
    print("=" * 60)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
            check=False
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print("MESSAGES:")
            print(result.stderr)

        if result.returncode != 0:
            print("Command failed with exit code:", result.returncode)

        return result.returncode == 0

    except FileNotFoundError:
        print("ERROR: kubectl was not found.")
        print("Install kubectl and ensure it is available in PATH.")
        return False

    except subprocess.TimeoutExpired:
        print("ERROR: Command timed out.")
        return False


def main():
    print("TASK 12: KUBERNETES DEPLOYMENT MONITOR")
    print("Checking cluster and application resources...")

    checks = [
        ["kubectl", "cluster-info"],
        ["kubectl", "get", "nodes"],
        ["kubectl", "get", "deployments"],
        ["kubectl", "get", "pods", "-o", "wide"],
        ["kubectl", "get", "services"],
        ["kubectl", "rollout", "status",
         "deployment/task12-web-deployment",
         "--timeout=120s"],
    ]

    failures = 0

    for command in checks:
        if not run_command(command):
            failures += 1

    print("\n" + "=" * 60)

    if failures == 0:
        print("MONITORING COMPLETED: All checks passed.")
    else:
        print("MONITORING COMPLETED WITH", failures, "failed check(s).")
        print("Review the command output and troubleshoot the issue.")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
