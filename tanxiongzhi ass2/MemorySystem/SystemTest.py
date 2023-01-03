from MemorySystem.MemorySystem import MemorySystem, Directory, MAX_BUF_FILE_SIZE, DIR_MAX_ELEMS
import pytest


@pytest.fixture
def test_memory_system() -> MemorySystem:
    fs = MemorySystem()
    fs.create_directory('.', "Directory1")
    return fs

@pytest.fixture
def create_more_directory() -> MemorySystem:
    ms = MemorySystem()
    ms.create_directory('.', "Directory1")
    ms.create_directory('.', "Directory2")
    ms.create_directory('./Directory1', "Directory11")
    ms.create_directory('./Directory1', "Directory12")
    ms.create_directory('./Directory2', "Directory21")

    return ms


def test_attain_node(memory_system: MemorySystem):
    node = memory_system.get_tree_node("./Directory1/Directory12")

    assert isinstance(node, Directory)
    assert node.name == "Directory12"



def test_string_to_path_1():
    ms = MemorySystem()
    ms.create_directory('.', "Directory1")
    ms.create_directory('./Directory1', "Nested_Directory")

    result = ms.string_to_path(".")

    assert len(result) == 1
    assert result[0].name == "~"


def test_string_to_path_2():
    ms = MemorySystem()
    ms.create_directory('.', "T_0")
    ms.create_directory('./T_0', "T_1_1")
    ms.create_directory('./T_0', "T_1_2")
    ms.create_directory('./T_0/T_1_1', "T_2_1")
    ms.create_directory('./T_0/T_1_2', "T_2_2")

    result = ms.string_to_path("./T_0/T_1_1/../T_1_2/T_2_2")

    assert len(result) == 4
    assert result[0].name == "~"
    assert result[1].name == "T_0"
    assert result[2].name == "T_1_2"
    assert result[3].name == "T_2_2"


def test_create_binary_file(memory_system: MemorySystem):
    file = memory_system.create_binary_file("./Directory1", "file.bin", "0")

    assert memory_system.base_root.son[0].son[0].name == "file.bin"
    assert memory_system.base_root.son[0].son[0].information == "Dummy info"


def test_create_log_file(memory_system: MemorySystem):
    file = memory_system.create_log_file("./Directory1", "file.log", "Log info")

    assert memory_system.base_root.son[0].son[0].name == "file.log"
    assert memory_system.base_root.son[0].son[0].information == "Log info"


def test_create_buffer(memory_system: MemorySystem):
    file = memory_system.create_buffer("./Directory1", "file.buf")

    assert memory_system.base_root.son[0].son[0].name == "file.buf"
    assert len(memory_system.base_root.son[0].son[0].items) == 0


def test_delete(memory_system: MemorySystem):
    memory_system.create_buffer("./Directory1/Directory11", "dummy.buf")

    buffer_file = memory_system.get_tree_node("./Directory1/Directory11/dummy.buf")
    folder = memory_system.get_tree_node("./Directory1/Directory11")

    assert(len(folder.son) == 1)
    buffer_file.delete()


def test_move(memory_system: MemorySystem):
    memory_system.create_buffer("./Directory1/Directory11", "dummy.buf")
    buffer_file_folder = memory_system.get_tree_node("./Directory1/Directory11")
    buffer_file_folder.move_dir("dummy.buf", "./Directory2")

    original_folder = memory_system.get_tree_node("./Directory1/Directory11")
    destination_folder = memory_system.get_tree_node("./Directory2")

    assert len(original_folder.son) == 0
    assert len(destination_folder.son) == 1
    assert destination_folder.son[0].name == "dummy.buf"


def test_file_read(memory_system: MemorySystem):
    memory_system.create_binary_file("./Directory1/Directory11", "dummy.bin", "some info")
    bin_file = memory_system.get_tree_node("./Directory1/Directory11/dummy.bin")

    assert (bin_file.read() == "more info")
    memory_system.create_log_file("./Directory1/Directory11", "dummy.log", "some info")
    log_file = memory_system.get_tree_node("./Directory1/Directory11/dummy.log")
    log_file.append("more info")

    assert (log_file.read() == "more info")


def test_buffer_push(memory_system: MemorySystem):
    memory_system.create_buffer("./Directory1/Directory11", "dummy.buf")
    buffer = memory_system.get_tree_node("./Directory1/Directory11/dummy.buf")

    assert len(buffer.items) == 0

    buffer.push(1)
    buffer.push(2)
    buffer.push(3)

    assert len(buffer.items) == 3


    memory_system.create_directory(".", "Dummy")
