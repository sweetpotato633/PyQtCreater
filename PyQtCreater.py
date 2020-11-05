import os
from pathlib import Path
from expand_file import get_file_path, execute_cmd, copyfile_with_dir
import shutil


def get_ui_rsc_file(mfile_list):
    ui_list = []
    rsc_list = []
    for m_file in mfile_list:
        if m_file.find(".ui") != -1:
            ui_list.append(m_file)
        elif m_file.find(".qrc") != -1:
            rsc_list.append(m_file)
    return ui_list, rsc_list


def create_ui_file(ui_list):
    cmd_list = []
    cmd_str = "pyuic5 -o"

    t_ui = ui_list[0]
    root_name = t_ui.split(os.sep)[0]
    cmd_list.append(root_name)
    for m_ui in ui_list:
        sub_dir = m_ui.split(os.sep)[:-1]
        sub_dir = os.sep.join(sub_dir)
        tcmd = "cd " + sub_dir
        cmd_list.append(tcmd)
        new_dir = m_ui.replace(".ui", ".py")
        tcmd = cmd_str + " " + new_dir + " " + m_ui
        cmd_list.append(tcmd)
        print("开始处理：" + m_ui)
    res = execute_cmd(cmd_list,need_print=False)
    print(res)

    try:
        for m_ui in ui_list:
            new_dir = m_ui.replace(app_dir + os.sep, "")
            new_dir = new_dir.replace(".ui", ".py")
            m_ui = m_ui.replace(".ui", ".py")
            copyfile_with_dir(m_ui, new_dir)
    except:
        print("\n" + m_ui + "处理错误，退出\n")


def create_rsc_file(rsc_list):
    cmd_list = []
    cmd_str = "pyrcc5"
    new_rsc_list = []
    for m_rsc in rsc_list:
        sub_dir = m_rsc.split(os.sep)[:-1]
        sub_dir = os.sep.join(sub_dir)
        tcmd = "cd " + sub_dir
        cmd_list.append(tcmd)
        new_dir_list = m_rsc.split(os.sep)
        new_name_list = new_dir_list[-1].split(".")
        new_name_list[-2] += "_rc"
        new_name_list[-1] = "py"
        new_dir_list[-1] = ".".join(new_name_list)
        new_dir = os.sep.join(new_dir_list)
        new_rsc_list.append(new_dir)
        tcmd = cmd_str + " " + m_rsc + " -o " + new_dir
        cmd_list.append(tcmd)
        print("开始处理：" + m_rsc)
    res = execute_cmd(cmd_list,need_print=False)
    print(res)

    try:
        for new_rsc in new_rsc_list:
            new_dir = new_rsc.replace(app_dir + os.sep, "")
            copyfile_with_dir(new_rsc, new_dir)
    except:
        print("\n" + m_rsc + "处理错误，退出\n")


app_dir = "QtApp"
if __name__ == "__main__":
    abdir = os.path.abspath(os.path.dirname(__file__))

    abdir = abdir + os.sep + app_dir

    print(abdir)
    mdir = Path(abdir)
    if not mdir.exists():
        print("请在根目录下创建" + app_dir + "文件夹，并把Qt原来的工程拷贝到这个目录下面。\n")
        input()
        exit(0)
    print("检测到" + app_dir + "目录，开始处理该目录下的QT工程文件...\n")
    file_list = []
    dir_list = []
    root_path = abdir

    get_file_path(root_path, file_list, dir_list)

    ui_list, rsc_list = get_ui_rsc_file(file_list)

    create_ui_file(ui_list)
    create_rsc_file(rsc_list)
    print("\n处理完毕，按任意键退出...\n")
    input()
