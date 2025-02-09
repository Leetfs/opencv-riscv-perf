import json
import os

def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_reports(rv_file, rvv_file, group_name):
    """
    对比 RV 和 RVV 的性能数据，计算性能提升率，并返回对比结果。

    参数:
        rv_file (str): RV 测试报告 JSON 文件路径
        rvv_file (str): RVV 测试报告 JSON 文件路径
        group_name (str): 测试集所属分组，如 'opencv_perf_core' 或 'opencv_perf_imgproc'

    返回:
        dict: 对比后的测试集结果，包括各个测试项的详细数据
    """
    rv_data = load_json(rv_file)
    rvv_data = load_json(rvv_file)

    # 读取 RV 和 RVV 的测试数据（按测试集分类）
    rv_testsuites = {ts["name"]: ts for ts in rv_data["testsuites"]}
    rvv_testsuites = {ts["name"]: ts for ts in rvv_data["testsuites"]}

    comparison_results = []
    for suite_name, rv_testsuite in rv_testsuites.items():
        if suite_name in rvv_testsuites:
            rvv_testsuite = rvv_testsuites[suite_name]

            suite_comparison = {
                "name": suite_name,
                "group": group_name,  # 标记当前测试集所属分组
                "tests": []
            }

            # 解析 RV 和 RVV 测试项
            rv_tests = {test["name"]: test for test in rv_testsuite["testsuite"]}
            rvv_tests = {test["name"]: test for test in rvv_testsuite["testsuite"]}

            total_speedup = 0  # 记录总性能提升
            count = 0  # 统计有效对比项数量

            for test_name, rv_test in rv_tests.items():
                if test_name in rvv_tests:
                    rvv_test = rvv_tests[test_name]

                    # **时间解析**
                    rv_time = float(rv_test["time"].replace("s", ""))
                    rvv_time = float(rvv_test["time"].replace("s", ""))

                    # **RV 和 RVV CPU 统计数据**
                    rv_stddev = int(rv_test["stddev"])
                    rvv_stddev = int(rvv_test["stddev"])
                    rv_mean = int(rv_test["mean"])
                    rvv_mean = int(rvv_test["mean"])
                    rv_median = int(rv_test["median"])
                    rvv_median = int(rvv_test["median"])

                    # **性能提升计算**
                    # RVV 加速时，应保证 speedup 计算出的值为正数
                    if rv_time > 0:
                        speedup = ((rv_time - rvv_time) / rv_time) * 100
                    else:
                        speedup = 0  # 避免除零错误

                    total_speedup += speedup
                    count += 1

                    # 记录测试项对比结果
                    suite_comparison["tests"].append({
                        "name": test_name,
                        "rv_time": rv_time,
                        "rvv_time": rvv_time,
                        "speedup": speedup,
                        "rv_stddev": rv_stddev,
                        "rvv_stddev": rvv_stddev,
                        "rv_mean": rv_mean,
                        "rvv_mean": rvv_mean,
                        "rv_median": rv_median,
                        "rvv_median": rvv_median
                    })

            # 计算该测试集的平均性能提升
            suite_comparison["avg_speedup"] = (total_speedup / count) if count > 0 else 0
            comparison_results.append(suite_comparison)

    return comparison_results

def generate_html(comparisons, output_path="../test_report.html"):
    """
    生成 HTML 格式的性能对比报告

    参数:
        comparisons (list): 所有测试集的对比结果
        output_path (str): 生成的 HTML 文件路径
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenCV RISC-V Vector 性能测试报告</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { text-align: center; }
            h2 { margin-top: 20px; border-bottom: 2px solid #333; padding-bottom: 5px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { border: 1px solid black; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            .faster { background-color: #c8e6c9; } /* 绿色 - 提升 */
            .slower { background-color: #ffcdd2; } /* 红色 - 退步 */
            .neutral { background-color: #eeeeee; } /* 灰色 - 无变化 */
        </style>
    </head>
    <body>
        <h1>OpenCV RISC-V Vector 性能测试报告</h1>
        <p>采样次数: 50</p>
    """

    # **按组排序，确保测试集按类别正确显示**
    comparisons.sort(key=lambda x: x["group"])

    last_group = None  # 追踪当前分组，避免重复插入标题
    for suite in comparisons:
        if suite["group"] != last_group:
            html_content += f"<h2>{suite['group']}</h2>"
            last_group = suite["group"]

        html_content += f"<h3>{suite['name']}（平均提升: {suite['avg_speedup']:.2f}%）</h3>"
        html_content += """
        <table>
            <tr>
                <th>测试用例</th>
                <th>RV 时间 (s)</th>
                <th>RVV 时间 (s)</th>
                <th>RV 标准差</th>
                <th>RVV 标准差</th>
                <th>RV 平均</th>
                <th>RVV 平均</th>
                <th>RV 中位数</th>
                <th>RVV 中位数</th>
                <th>提升 (%)</th>
            </tr>
        """

        for test in suite["tests"]:
            color_class = "faster" if test["speedup"] > 0 else "slower" if test["speedup"] < 0 else "neutral"
            html_content += f"""
            <tr class="{color_class}">
                <td>{test['name']}</td>
                <td>{test['rv_time']:.3f}</td>
                <td>{test['rvv_time']:.3f}</td>
                <td>{test['rv_stddev']}</td>
                <td>{test['rvv_stddev']}</td>
                <td>{test['rv_mean']}</td>
                <td>{test['rvv_mean']}</td>
                <td>{test['rv_median']}</td>
                <td>{test['rvv_median']}</td>
                <td>{test['speedup']:.2f}%</td>
            </tr>
            """

        html_content += "</table>"

    html_content += "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 报告已生成: {output_path}")

def generate_comparison_report():
    """
    生成完整的 OpenCV 性能对比报告
    """
    test_report_pairs = [
        ("../core/RV_core_test_report.json", "../core/RVV_core_test_report.json", "opencv_perf_core"),
        ("../imgproc/RV_imgproc_test_report.json", "../imgproc/RVV_imgproc_test_report.json", "opencv_perf_imgproc"),
    ]

    # test_report_pairs = [
    #     ("./output_sample/RV_core_Abs_test_report.json", "./output_sample/RVV_core_Abs_test_report.json", "opencv_perf_core"),
    #     ("./output_sample/RV_imgproc_Bilateral_test_report.json", "./output_sample/RVV_imgproc_Bilateral_test_report.json", "opencv_perf_imgproc"),
    # ]

    all_comparisons = []
    for rv_file, rvv_file, group in test_report_pairs:
        if os.path.exists(rv_file) and os.path.exists(rvv_file):
            all_comparisons.extend(compare_reports(rv_file, rvv_file, group))

    generate_html(all_comparisons)

if __name__ == "__main__":
    generate_comparison_report()
