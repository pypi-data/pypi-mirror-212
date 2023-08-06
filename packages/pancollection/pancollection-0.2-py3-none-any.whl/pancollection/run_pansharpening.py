# GPL License
# Copyright (C) UESTC
# All Rights Reserved 
#
# @Time    : 2022/4/25 0:17
# @Author  : Xiao Wu
# @reference:

def run_demo():
    from pancollection.configs.configs import TaskDispatcher
    from udl.AutoDL.trainer import main
    from pancollection.common.builder import build_model, getDataSession

    cfg = TaskDispatcher.new(task='pansharpening', mode='entrypoint', arch='FusionNet')
    print(TaskDispatcher._task.keys())
    main(cfg, build_model, getDataSession)

if __name__ == '__main__':
    run_demo()