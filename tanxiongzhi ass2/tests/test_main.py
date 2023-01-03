import os

import pytest
from MemorySystem.MemorySystem import MemorySystem


def test_index_get(client):
    #  Read directory file

    me = MemorySystem()
    me.create_directory('.', "Directory1")
    me.create_directory('.', "Directory2")
    me.create_directory('.', "Directory3")

    index_response = client.get("/main_system/index")
    print(index_response.data)
    assert index_response.status_code == 200
    print('The root directory should include three new files: ')
    assert "Directory1" in str(index_response.data)
    assert "Directory2" in str(index_response.data)
    assert "Directory3" in str(index_response.data)


# create a file
def test_create_directory(client):

    assert client.get("/main_system/directory").status_code == 200
    print()
    res = client.post("/main_system/directory", data={"path": ".", "name": "Directory4"})
    print('The path of the new folder is: ')
    print(res.data)
    response = res.data
    assert response == b'./Directory4'


# Create binaries
def test_create_binary(client):
    res = client.post("/main_system/binaryfile", data={"path": ".", "name": "dummy.bin", "info": "some info"})
    print()
    assert res.status_code == 200
    response = res.data
    print(response)
    print('The path of the new folder is:')
    assert response == b'./dummy.bin:some info'
    response = client.get("/main_system/binaryfile?info=some info")
    print('Confirm the file type created: \n')
    print(response.data)
    assert response.data == b'some info'


#  Create Log file
def test_create_logtextfile(client):
    res = client.get("/main_system/logfile?info=some info")
    # assert client.get("/main_system/log_file", data={"path": ".", "name": "dummy.bin"}).status_code == 200
    client.post("/main_system/logfile", data={"path": ".", "name": "dummy.bin", "info": "some info"})
    print('Confirm the file type created: \n')
    response = res.data
    assert response == b'some info'


# create buffer file
def test_create_bufferfile(client):
    assert client.get("/main_system/bufferfile?item=file.buf").status_code == 200
    res = client.post("/main_system/bufferfile", data={"name": "file.buf", "path": "."})
    print(res.data)
    response = res.data
    assert response == b'./file.buf'


def test_move(client):
    # File move
    # create file called 'target'
    re = client.post("/main_system/bufferfile", data={"name": "dummy.buf", "path": "."})
    print(re.data)
    # move 'dummy' to 'Directory1'(This folder was created in the previous test)
    response = client.put("/main_system/index", data={"src": "dummy.buf", "dest": "Directory1", "name": "dummy.buf"})
    print(response.data)
    index_response = os.listdir('Directory1')
    print(index_response)
    assert response.status_code == 200
    assert response.data == b'Directory1/dummy.buf'
    print('Confirm that there is the object file in "Directory1"')
    assert "dummy.buf" in index_response


def test_delete(client):
    # file delete
    client.post("/main_system/bufferfile", data={"name": "dummy.buf", "path": "."})

    client.post("/main_system/binaryfile", data={"path": "d1", "name": "target2", "information": "1234"})
    index_response = os.listdir('Directory1')
    print('\nThe directory in the current folder "Directory1" is : ')
    print(index_response)
    assert "dummy.buf" in index_response
    response_delete = client.delete("/main_system/index?name=Directory1/dummy.buf")
    index_response = os.listdir('Directory1')
    print('After deletion:')
    assert "dummy.buf" not in index_response
    print(index_response)
    print(response_delete.data)
    assert response_delete.status_code == 200


def test_binaryfile_read(client):
    #  Binary file read file
    client.post("/main_system/binaryfile", data={"path": ".", "name": "file.bin", "info": "Dummy info"})
    response = client.get("/main_system/binaryfile?info=Dummy info")
    print(response.data)
    assert response.status_code == 200
    assert response.data == b'Dummy info'


def test_buffer_pop(client):
    print('Storage of test data')
    t1 = client.put("/main_system/bufferfile", data={"path": "b3", "item": "test1"})
    t2 = client.put("/main_system/bufferfile", data={"path": "b4", "item": "test2"})
    t3 = client.put("/main_system/bufferfile", data={"path": "b5", "item": "test3"})
    print('testing')
    assert t1.data == b"test1"
    assert t2.data == b"test2"
    assert t3.data == b"test3"


def test_buffer_push(client):
    print('Storage of test data: ')
    client.post("/main_system/bufferfile", data={"name": "file_test.buf", "path": "."})
    client.put("/main_system/bufferfile", data={"path": "dummy1.buf", "item": "a1"})
    client.put("/main_system/bufferfile",  data={"path": "dummy1.buf", "item": "a2"})

    response = client.get("/main_system/bufferfile?item=a1")
    response = client.get("/main_system/bufferfile?item=a2")
    print(response.data)
    print('Storage succeeded !')
    assert len(response.data) == 2






