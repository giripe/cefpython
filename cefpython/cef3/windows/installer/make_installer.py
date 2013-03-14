import sys
import os
import platform
import argparse
import re

ISCC = r"c:\Program Files (x86)\Inno Setup 5\ISCC.exe"
if "INNO5" in os.environ:
    ISCC = os.environ["INNO5"]

TEMPLATE_FILE = os.getcwd()+r"\innosetup.template"
ISS_FILE = os.getcwd()+r"\innosetup.iss"

def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("-v", "--version", help="cefpython version",
            required=True)
    args = parser.parse_args()
    assert re.search(r"^v\d+$", args.version), "Invalid version string"

    vars = {}
    vars["PACKAGE_NAME"] = "cefpython3"
    vars["APP_VERSION"] = args.version
    vars["PYTHON_VERSION"] = (str(sys.version_info.major) + "."
            + str(sys.version_info.minor))
    vars["PYTHON_VERSION_NODOT"] = (str(sys.version_info.major) + ""
            + str(sys.version_info.minor))
    vars["PYTHON_ARCHITECTURE"] = platform.architecture()[0]
    vars["BINARIES_DIR"] = os.path.realpath(os.getcwd()+r"\..\binaries")
    vars["PYD_FILE"] = (vars["BINARIES_DIR"]+r"\cefpython_py"
            + str(sys.version_info.major) + str(sys.version_info.minor)
            + ".pyd")
    vars["INSTALLER_DIR"] = os.getcwd()

    print("Reading template: %s" % TEMPLATE_FILE)

    f = open(TEMPLATE_FILE)
    template = f.read()
    f.close()

    f = open(ISS_FILE, "w")
    f.write(template % vars)
    f.close()

    print("Saved: %s" % ISS_FILE)

    initPyTemplate = os.getcwd()+r"\__init__.py.template"
    initPyInstall = os.getcwd()+r"\__init__.py.install"

    f = open(initPyTemplate)
    initPyTemplateCode = f.read()
    f.close()

    f = open(initPyInstall, "w")
    f.write(initPyTemplateCode % vars)
    f.close()
    print("Saved: %s" % initPyInstall)

    iscc_command = '"'+ ISCC + '" ' + ISS_FILE
    print("Running ISCC: %s" % iscc_command)
    os.system(iscc_command)

if __name__ == "__main__":
    main()