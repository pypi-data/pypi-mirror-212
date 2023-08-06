# to run: python3 -m pytest test_parse_xml.py

import os
import tempfile
from faker import Faker
import pytest
from citros import Citros

NUM_TEST_RUNS = 10

faker = Faker()

def generate_cmake_content(executables):
    content = "\n".join([f"add_executable({exe} src/{exe}.cpp)" for exe in executables])
    install_targets = " ".join(executables)
    content += f"\n\ninstall(TARGETS {install_targets} DESTINATION lib/${{PROJECT_NAME}})\n"
    return content


def cmake_data():
    for _ in range(NUM_TEST_RUNS):
        executables = [faker.pystr_format() for _ in range(faker.random_int(min=1, max=5))]
        yield executables, generate_cmake_content(executables)


@pytest.mark.parametrize("executables,cmake_content", cmake_data())
def test_parse_makefile(executables, cmake_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        cmake_path = os.path.join(tmpdir, "CMakeLists.txt")
        with open(cmake_path, "w") as f:
            f.write(cmake_content)

        with Citros() as citros: 
            result = citros.parser_ros2.parse_makefile(tmpdir)

        assert result["cmake"] == cmake_path
        nodes = result["nodes"]
        assert len(nodes) == len(executables)
        for node in nodes:
            assert "name" in node
            assert node["name"] in executables
            assert "entry_point" in node
            assert node["entry_point"] == ""
            assert "path" in node
            assert node["path"] == ""
            assert "parameters" in node
            assert node["parameters"] == []


def test_parse_makefile_no_install():
    with tempfile.TemporaryDirectory() as tmpdir:
        cmake_path = os.path.join(tmpdir, "CMakeLists.txt")
        with open(cmake_path, "w") as f:
            f.write("add_executable(foo src/foo.cpp)")

        with Citros() as citros: 
            with pytest.raises(ValueError) as e:
                citros.parser_ros2.parse_makefile(tmpdir)
            assert str(e.value) == f"{cmake_path} is not formatted correctly: no 'install' command found."


def test_parse_makefile_no_targets():
    with tempfile.TemporaryDirectory() as tmpdir:
        cmake_path = os.path.join(tmpdir, "CMakeLists.txt")
        with open(cmake_path, "w") as f:
            f.write("install(TARGETS DESTINATION lib/${PROJECT_NAME})")

        with Citros() as citros: 
            with pytest.raises(ValueError) as e:
                citros.parser_ros2.parse_makefile(tmpdir)
            assert str(e.value) == f"{cmake_path} is not formatted correctly: no targets in 'install' command."


def test_parse_makefile_multiline_install():
    executables = [faker.pystr_format() for _ in range(faker.random_int(min=1, max=5))]

    with tempfile.TemporaryDirectory() as tmpdir:
        cmake_path = os.path.join(tmpdir, "CMakeLists.txt")
        with open(cmake_path, "w") as f:
            f.write("install(TARGETS \n")
            for exe in executables:
                f.write(f"{exe} \n")
            f.write("DESTINATION lib/${PROJECT_NAME})")

        with Citros() as citros: 
              result = citros.parser_ros2.parse_makefile(tmpdir)

        assert result["cmake"] == cmake_path
        nodes = result["nodes"]
        assert len(nodes) == len(executables)
        for node in nodes:
            assert "name" in node
            assert node["name"] in executables
            assert "entry_point" in node
            assert node["entry_point"] == ""
            assert "path" in node
            assert node["path"] == ""
            assert "parameters" in node
            assert node["parameters"] == []