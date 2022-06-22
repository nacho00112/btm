
import re
from setuptools import setup, find_packages

print("Getting btm version information...")

with open(".meta_version", "r") as meta_version:
    meta_version_config = dict(
            list(map(
                    str.strip, each.split(":")
                    ))
            for each in re.sub(r"\n\n+", "\n", re.sub("#.*", "", meta_version.read())).splitlines()
            )

version_method = meta_version_config.get("method", "none")
if version_method == "none":
    version = meta_version_config.get("current", "1.0.0")
elif version_method.strip() == "timeversion":
    from datetime import datetiime
    version = str(datetime.today().timestamp())
elif version_method.strip() == "autoinc":
    version = meta_version_config["current"].strip()
else:
    raise Exception("Invalid `version_method`. Check your .meta_version.")

print("This is btm v%s" % version)

kwargs = dict(
        author = "Nacho00112",
        version = version,
        license = "mit",
        python_requires = ">=3.7",
        url = "https://github.com/nacho00112/btm",
        download_url = "https://github.com/nacho00112/btm/archive/v%s.tar.gz" % version,
        author_email = "thurealrubiogame@gmail.com",
        packages = find_packages(),
        platforms = "any",
        # The requirements.txt file support comentaries with "#" like python
        install_requires = re.sub("#.*", "", open("requirements.txt").read()).split(),
        entry_points={"console_scripts": []},
        # above option specifies what commands to install,
        # e.g: entry_points={"console_scripts": ["yapypy=yapypy.cmd:compiler"]}
        )

print("Generating btm/info.py...")

with open("btm/info.py", "w") as btm_info:
    btm_info.write('''
"""
This file is automatically generated by the setup.py,
contains useful information about this package.
"""

__all__ = %s

''' % list(map(str.upper, kwargs.keys())))
    for name, info in kwargs.items():
        btm_info.write("%s = %r\n" % (name.upper(), info))
    btm_info.write("\n")

print("btm/info.py is successfully generated")

with open("README.md") as README:
    README = README.read()
    
try:
    setup(
        name = "btm",
        description = "Modify Python Built-in Types",
        long_description = README,
        long_description_content_type = "text/markdown",
        classifiers = [
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
        zip_safe = False,
        **kwargs,
        )
except SystemExit: # Catch for increment the version if the method is autoinc
    pass

print("Versioning method is setted to:", version_method)

if version_method == "autoinc":
    print("Incrementing the version...")
    version = int(version.replace(".", "")) + 1
    version = list(str(version))
    length = 3
    while len(version) < length:
        version.insert(0, "0")
    for num in range(length-1):
        version.insert(-1 + num * -2, ".")
    version = "".join(version)
    with open(".meta_version", "w") as meta_version:
        meta_version.write("method: autoinc\ncurrent: %s" % version)
    print("Then now the next version is:", version)

else:
    with open(".meta_version", "w") as meta_version:
        meta_version.write("method: %s\ncurrent: %s" % (version_method, version))


