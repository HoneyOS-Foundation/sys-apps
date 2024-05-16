"""
Packages all the binaries into a simple archive
"""
import tomllib
import os
import tempfile
import shutil

# Create the dist directory if it doesn't exist
if not os.path.exists("dist"):
    os.mkdir("dist")

temp = tempfile.TemporaryDirectory()

# Read tbe workspace to figure out what crates there are
workspace_file = open("workspace.toml")
workspace_toml = tomllib.loads(workspace_file.read())
workspace_file.close()
# Load the members from the workspace
members: list = workspace_toml["members"]

# Compile each crate and copy it;s binary to the temp dir
for crate in members:
    os.system("cd " + crate +
              " && cargo build --release --target wasm32-unknown-unknown")
    shutil.copyfile(
        crate + "/target/wasm32-unknown-unknown/release/" + crate + ".wasm", temp.name + "/" + crate + ".wasm")

# Zip the temp dir
print("Packaging binaries")
shutil.make_archive("dist/bin", 'zip', temp.name)

temp.cleanup()
