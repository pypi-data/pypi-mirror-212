# encoding: UTF-8
import os, fnmatch, shutil


def one(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def read_file_list(filepath, filename, errlog=None):
    fullfilename = os.path.join(filepath, filename)
    try:
        file1 = open(fullfilename, "r")
    except Exception as e:
        if errlog:
            errlog("Error al abrir el fichero %s" % fullfilename)
        return []
    txt = [line.strip() for line in file1]
    file1.close()
    txt2 = [line for line in txt if len(line) and not line.startswith("#")]
    return txt2


def find_files(basedir, glob_pattern="*", abort_on_match=False):
    ignored_files = [
        "*~",
        ".*",
        "*.bak",
        "*.bakup",
        "*.tar.gz",
        "*.tar.bz2",
        "*.BASE.*",
        "*.LOCAL.*",
        "*.REMOTE.*",
        "*.*.rej",
        "*.*.orig",
    ]
    retfiles = []

    for root, dirs, files in os.walk(basedir):
        baseroot = os.path.relpath(root, basedir)
        for pattern in ignored_files:
            delfiles = fnmatch.filter(files, pattern)
            for f in delfiles:
                files.remove(f)
            deldirs = fnmatch.filter(dirs, pattern)
            for f in deldirs:
                dirs.remove(f)
        pass_files = [
            os.path.join(baseroot, filename) for filename in fnmatch.filter(files, glob_pattern)
        ]
        if pass_files and abort_on_match:
            dirs[:] = []
        retfiles += pass_files
    return retfiles


def get_max_mtime(path, filename):
    ignored_files = [
        "*~",
        ".*",
        "*.bak",
        "*.bakup",
        "*.tar.gz",
        "*.tar.bz2",
        "*.BASE.*",
        "*.LOCAL.*",
        "*.REMOTE.*",
        "*.*.rej",
        "*.*.orig",
    ]

    basedir = os.path.join(path, os.path.dirname(filename))
    max_mtime = 0
    for root, dirs, files in os.walk(basedir):
        for pattern in ignored_files:
            delfiles = fnmatch.filter(files, pattern)
            for f in delfiles:
                files.remove(f)
            deldirs = fnmatch.filter(dirs, pattern)
            for f in deldirs:
                dirs.remove(f)
        for filename in files:
            filepath = os.path.join(root, filename)
            file_stat = os.stat(filepath)
            if file_stat.st_mtime > max_mtime:
                max_mtime = file_stat.st_mtime
    return max_mtime


def check_folder_clean(iface, feature, folder):
    from enebootools.assembler import kobjects

    feature_object = kobjects.FeatureObject.find(feature)

    src_path = os.path.join(feature_object.fullpath, "build", "src")
    base_path = os.path.join(feature_object.fullpath, "build", "base")
    final_path = os.path.join(feature_object.fullpath, "build", "final")
    patch_path = os.path.join(feature_object.fullpath, "patches", feature)

    diferencias = calcula_diferencias_folders(final_path, src_path)

    if diferencias:
        print(
            "\n** ATENCIÓN **\n\n\nEn la carpeta %s de la extensión %s existen cambios que no existen"
            % (folder, feature)
            + " en la carpeta final.Si usó previamente el comando save-fullpatch esto puede ser normal.\n\nCambios:"
        )
        print(
            "\n".join(
                [
                    "\t- %s -> %s"
                    % (
                        diferencia[1],
                        diferencia[0],
                    )
                    for diferencia in diferencias
                ]
            )
        )

        while True:
            print(
                "\n¿Desea continuar regenerando la carpeta(s/n)?",
                end="",
            )
            result = input().lower()
            if result in ("s,n,y"):
                if result in ("n"):
                    return False
                break
            print("Respuesta invalida.")

    if folder == "src":
        if os.path.exists(src_path):
            iface.info("Borrando %s" % src_path)
            shutil.rmtree(src_path)
        if os.path.exists(base_path):
            iface.info("Borrando %s" % base_path)
            shutil.rmtree(base_path)
        if os.path.exists(final_path):
            iface.info("Borrando %s" % final_path)
            shutil.rmtree(final_path)

    return True


def calcula_diferencias_folders(final_path, src_path):
    ignored_files = [
        "*~",
        ".*",
        "*.bak",
        "*.bakup",
        "*.tar.gz",
        "*.tar.bz2",
        "*.BASE.*",
        "*.LOCAL.*",
        "*.REMOTE.*",
        "*.*.rej",
        "*.*.orig",
    ]
    final_path_files = set([])

    for root, dirs, files in os.walk(final_path):
        baseroot = os.path.relpath(root, final_path)
        for pattern in ignored_files:
            delfiles = fnmatch.filter(files, pattern)
            for f in delfiles:
                files.remove(f)
            deldirs = fnmatch.filter(dirs, pattern)
            for f in deldirs:
                dirs.remove(f)

        for filename in files:
            final_path_files.add(os.path.join(baseroot, filename))

    src_path_files = set([])

    for root, dirs, files in os.walk(src_path):
        baseroot = os.path.relpath(root, src_path)
        for pattern in ignored_files:
            delfiles = fnmatch.filter(files, pattern)
            for f in delfiles:
                files.remove(f)
            deldirs = fnmatch.filter(dirs, pattern)
            for f in deldirs:
                dirs.remove(f)

        for filename in files:
            src_path_files.add(os.path.join(baseroot, filename))

    added_files = src_path_files - final_path_files
    deleted_files = final_path_files - src_path_files
    common_files = src_path_files & final_path_files
    modified_files = []

    for common_file in common_files:
        src_file = os.path.join(src_path, common_file)
        final_file = os.path.join(final_path, common_file)
        src_time = os.path.getmtime(src_file) if os.path.exists(src_file) else 0
        final_time = os.path.getmtime(final_file) if os.path.exists(final_file) else 0
        if src_time and final_time and src_time > final_time:
            modified_files.append(common_file)
            continue

    if final_path and src_path:
        file_actions = []
        file_actions += [(f, "add") for f in added_files]
        file_actions += [(f, "modified") for f in modified_files]
        file_actions += [(f, "delete") for f in deleted_files]

    return file_actions
