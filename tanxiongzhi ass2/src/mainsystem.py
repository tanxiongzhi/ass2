import functools
import os
import shutil

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request, make_response
from flask import url_for
from MemorySystem.MemorySystem import Directory, BinaryFile, BufferFile, TreeNode, MemorySystem

bp = Blueprint("main_system", __name__, url_prefix="/main_system")


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("main_system.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/index", methods=["GET", "PUT", "DELETE"])
def index():  # root directory
    me = MemorySystem()

    if request.method == "GET":
        #  Get the file list
        print()
        path = request.args.get("path", '.')
        index_response = os.listdir(path)
        l = []
        for dir in index_response:
            t = dir.split('\\')
            l.append(t[-1])
            print(t[-1], end=',')

        return l

    elif request.method == "PUT":
        # Move instruction
        src = request.form.get("src")
        dest = request.form.get("dest")
        name = request.form.get("name")
        buffer_file_folder = me.get_tree_node(src)

        if not src or not dest:
            return make_response({"status": "error", "message": "You need to specify src and dest to move elements!"},
                                 400)

        try:
            # d.move_dir(src, dest)
            shutil.move(src, dest)
        except:
            return make_response({"status": "erorr"}, 404)

        return dest + '/' + src

    elif request.method == "DELETE":
        # Delete Instruction
        name = request.args.get("name")

        try:
            me.delete_file(name)
            return name

        except ValueError as e:
            return make_response({"status": "error", "message": str(e)}, 400)


@bp.route("/directory", methods=["GET", "POST"])
def directory():
    me = MemorySystem()
    if request.method == "GET":
        #  Catalogue
        path = request.args.get("path", '.')
        index_response = os.listdir(path)
        l = []
        for dir in index_response:
            t = dir.split('\\')
            l.append(t[-1])
            print(t[-1], end=',')

        return l

    elif request.method == "POST":
        print()
        # Create the new folder
        path = request.form["path"]
        name = request.form["name"]
        error = None

        if not path:
            error = "Path is required."

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)

        try:
            me.create_directory(path, name)

        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)

        return path + '/' + name

    return render_template("main_system/directory.html")


@bp.route("/binaryfile", methods=["GET", "POST"])
def binary():
    me = MemorySystem()
    if request.method == "GET":
        #  Read a binary file
        print()
        info = request.args.get("info")
        return info

    elif request.method == "POST":
        #  Create some binaries files
        path = request.form.get("path")
        name = request.form.get("name")
        info = request.form.get("info")

        if not path or not name:
            return make_response({"status": "error", "message": "Arguments path and name are required"}, 400)

        if not info:
            return make_response({"status": "error", "message": "Argument information is required"}, 400)

        try:

            me.create_binary_file(path, name, info)

        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)

        return path + '/' + name + ':' + info

    return render_template("main_system/binary_file.html")


@bp.route("/logfile", methods=["GET", "POST"])
def logfile():
    me = MemorySystem()
    if request.method == "GET":
        info = request.args.get("info")
        #  Catalogue
        print()
        bin_file = me.get_tree_node(info)
        print(info)
        print(type(bin_file))
        # print(bin_file.read())

        return info

    elif request.method == "POST":
        #  Create a log file
        path = request.form["path"]
        name = request.form["name"]
        info = request.form.get("info")
        error = None

        if not path:
            error = "Path is required."

        if not info:
            return make_response({"status": "error", "message": "Argument information is required"}, 400)

        if error is not None:
            flash(error)

        try:
            me.create_log_file(path, name, info)
        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)

        return path + '/' + name + ':' + info

    return render_template("main_system/log_file.html")


@bp.route("/bufferfile", methods=["GET", "POST", "PUT"])
def bufferfile():
    me = MemorySystem()
    if request.method == "GET":
        #  Read binary file
        item = request.args.get("item")
        #  Catalogue
        print()
        return item

    elif request.method == "POST":
        #  Create some binaries files
        path = request.form["path"]
        name = request.form["name"]
        error = None

        if not path:
            error = "Path is required."

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)

        try:
            me.create_buffer(path, name)
            me.create_directory(path, name)

        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)

        print()
        return path + '/' + name
    if request.method == "PUT":
        #  Storing information to binary files
        path = request.form.get("path")
        item = request.form.get("item")

        if not path or not item:
            return make_response({"status": "error", "message": "Arguments path and information is required"}, 400)

        return item

    return render_template("main_system/buffer_file.html")

