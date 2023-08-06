# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：record.py
import os, time
from requests import request


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


def record_send_text(terminalreporter, key):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    headers = {"Content-Type": "application/json"}

    time_ = time.strftime("%Y-%m-%d %H:%M:%S")
    skipped = terminalreporter.stats.get("skipped", [])
    passed = terminalreporter.stats.get("passed", [])
    failed = terminalreporter.stats.get("failed", [])

    failed_content = list()
    failed_log = list()
    for i in failed:
        case_name = i.location[-1]
        long_log = str(i.longrepr)
        log_file = time_ + " " + case_name + "_error.log"
        failed_content.append(case_name)
        with open(log_file, "w") as f:
            f.write(long_log)

        upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
        upload_headers = {
            "Content-Type": "multipart/form-data",
            "Content-Length": "220"
        }

        upload_file = open(log_file, "rb")

        r = request(url=upload_url, files={"filename": upload_file}, headers=upload_headers, method="post")
        failed_log.append(r.json()["media_id"])

    failed_count = len(failed)
    passed_count = len(passed)
    skipped_count = len(skipped)

    result_count = failed_count + passed_count + skipped_count

    if failed_count > 0:
        content = {
            "content": f"""{time_}\n实时api监控反馈;请相关同事注意。\n
                     >总计运行用例数：<font color=\"info\">{result_count}</font>
                     >异常用例数：<font color=\"warning\">{failed_count}</font>
                     >正常用例数：<font color=\"info\">{passed_count}</font>
                     >跳过用例数：<font color=\"comment\">{skipped_count}</font>
                     >失败的用例为：<font color=\"warning\">{failed_content}</font>
                     """
        }
        data = {
            "msgtype": "markdown",
            "markdown": content
        }

        request(url=url, json=data, headers=headers, method="post")
        for i in failed_log:
            failed_data = {
                "msgtype": "file",
                "file": {
                    "media_id": i
                }
            }
            request(url=url, json=failed_data, headers=headers, method="post")
    else:
        content = {
            "content": f"""{time_}\n实时[{time_}]api监控反馈;请相关同事注意。\n
                     >总计运行用例数：<font color=\"info\">{result_count}</font>
                     >异常用例数：<font color=\"warning\">{failed_count}</font>
                     >正常用例数：<font color=\"info\">{passed_count}</font>
                     >跳过用例数：<font color=\"comment\">{skipped_count}</font>"""
        }

        data = {
            "msgtype": "markdown",
            "markdown": content
        }

        request(url=url, json=data, headers=headers, method="post")
