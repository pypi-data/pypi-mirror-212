# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：record.py
import os


class Context:
    pass


def record_result(outcome, result_path=None):
    report = outcome.get_result()
    if report.when == "call":  # 过滤 前置，和后置，只保留运行中的状态

        if report.outcome != "passed":
            record_str = f"""
用例：{report.nodeid}
参与的数据为：{getattr(Context, "log_str", "无")}
异常原因：{report.longreprtext}
{"=" * 80}\n"""
            if result_path:
                abspath = os.path.abspath(result_path)
                with open(abspath, "a", encoding="utf-8") as f:
                    f.write(record_str)
            else:
                print(record_str)


def record_result_log(*args, **kwargs):
    log_str = f"""
    元组：{args}
    字典：{kwargs}
    """
    log_str = log_str.replace("元组：()", "").replace("字典：{}", "").replace("字典：", "").replace("元组：", "")
    setattr(Context, "log_str", log_str)
