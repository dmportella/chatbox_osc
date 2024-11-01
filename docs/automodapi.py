import argparse
import pathlib
from pathlib import Path


def generate_rst_files(package_root_path: str, doc_root_path: str) -> None:
    """Generate reStructuredText (RST) files for the current Python Package.

    Parameters
    ----------
    package_root_path : str
        The root directory path of your Python Package. For example: src/your_package.
    doc_root_path : str
        The root directory path of your documentation. The directory must include
        a `source` folder.
    """
    package_root_path_object = Path(package_root_path)
    doc_root_path_object = Path(doc_root_path)
    py_files = list(package_root_path_object.glob("**/*.py"))
    api_rst_file_path = doc_root_path_object / "source" / "api.rst"
    with api_rst_file_path.open("w", encoding="utf8") as api_rst_file:
        pkg_name = package_root_path_object.name
        api_rst_file.write(f"{pkg_name}\n")
        api_rst_file.write("=" * len(pkg_name) + "\n\n")
        if package_root_path_object / "__init__.py" in py_files:
            api_rst_file.write(f".. automodapi:: {pkg_name}.__init__\n")
            api_rst_file.write("   :no-inheritance-diagram:\n\n")
            api_rst_file.write("   :include-all-objects:\n\n")
        if package_root_path_object / "__main__.py" in py_files:
            api_rst_file.write(f".. automodapi:: {pkg_name}.__main__\n")
            api_rst_file.write("   :no-inheritance-diagram:\n\n")
            api_rst_file.write("   :include-all-objects:\n\n")
        if package_root_path_object / "main.py" in py_files:
            api_rst_file.write(f".. automodapi:: {pkg_name}.main\n")
            api_rst_file.write("   :no-inheritance-diagram:\n\n")
            api_rst_file.write("   :include-all-objects:\n\n")
        api_rst_file.write(f"{pkg_name} Submodules\n")
        api_rst_file.write("-" * len(f"{pkg_name} Submodules") + "\n\n")
        for py_file in py_files:
            module_name = _get_module_name(package_root_path_object, py_file)
            if module_name.startswith("_") or module_name == "main":
                continue
            rst_filename = f"{module_name}.rst"
            rst_path = doc_root_path_object / "source" / rst_filename
            with rst_path.open("w", encoding="utf8") as rst_file:
                rst_file.write(f"{module_name}\n")
                rst_file.write("=" * len(module_name) + "\n\n")
                rst_file.write(f".. automodapi:: {pkg_name}.{module_name}\n")
                rst_file.write("   :no-inheritance-diagram:\n")
                rst_file.write("   :include-all-objects:\n")
            api_rst_file.write(".. toctree::\n")
            api_rst_file.write("   :maxdepth: 1\n\n")
            api_rst_file.write(f"   {module_name}\n\n")


def _get_module_name(package_root_path_object: Path, py_file: Path) -> str:
    relative_path = py_file.relative_to(package_root_path_object)
    module_name = relative_path.stem
    return module_name.replace(pathlib.os.sep, ".")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate .rst files for automodapi")
    parser.add_argument("src_root_path", help="Path to the package src folder")
    parser.add_argument("doc_root_path", help="Path to the docs folder")
    args = parser.parse_args()
    generate_rst_files(args.src_root_path, args.doc_root_path)
