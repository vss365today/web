from sys import argv
from toml import load


def get_package(package: dict) -> str:
    return f"{package['name']}=={package['version']}"


def filter_packages(packages: list, key: str) -> list:
    return list(filter(lambda p: p["category"] == key, packages))


# Does the user want to include the dev packages?
try:
    get_dev_packages = argv[1].upper() == "--DEV"
except IndexError:
    get_dev_packages = False

# Load the lock file contents and get the respective package for each category
poetry_lock = load(open("./poetry.lock"))
all_packages = filter_packages(poetry_lock['package'], "main")

# Write the dev packages if requested
if get_dev_packages:
    all_packages += filter_packages(poetry_lock['package'], "dev")

# Open the requirements file for writing
with open("requirements.txt", "wt") as f:
    # Write all the requested packages
    for package in all_packages:
        f.write(f"{get_package(package)}\n")
