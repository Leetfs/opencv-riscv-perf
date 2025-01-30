import json
import os

def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_reports(rv_file, rvv_file):
    """对比 RV 和 RVV 性能"""
    rv_data = load_json(rv_file)
    rvv_data = load_json(rvv_file)

    rv_testsuites = {ts["name"]: ts for ts in rv_data["testsuites"]}
    rvv_testsuites = {ts["name"]: ts for ts in rvv_data["testsuites"]}

    comparison_results = []
    for suite_name, rv_testsuite in rv_testsuites.items():
        if suite_name in rvv_testsuites:
            rvv_testsuite = rvv_testsuites[suite_name]

            suite_comparison = {
                "name": suite_name,
                "tests": []
            }

            rv_tests = {test["name"]: test for test in rv_testsuite["testsuite"]}
            rvv_tests = {test["name"]: test for test in rvv_testsuite["testsuite"]}

            total_speedup = 0
            count = 0

            for test_name, rv_test in rv_tests.items():
                if test_name in rvv_tests:
                    rvv_test = rvv_tests[test_name]

                    # **解析时间**
                    rv_time = float(rv_test["time"].replace("s", ""))
                    rvv_time = float(rvv_test["time"].replace("s", ""))

                    # **正确的提升计算方式**
                    speedup = ((rv_time - rvv_time) / rvv_time) * 100 if rvv_time > 0 else 0

                    # **解析额外信息**
                    rv_samples = int(rv_test["samples"])
                    rvv_samples = int(rvv_test["samples"])
                    rv_mean = float(rv_test["mean"])
                    rvv_mean = float(rvv_test["mean"])
                    rv_median = float(rv_test["median"])
                    rvv_median = float(rvv_test["median"])

                    total_speedup += speedup
                    count += 1

                    suite_comparison["tests"].append({
                        "name": test_name,
                        "rv_time": rv_time,
                        "rvv_time": rvv_time,
                        "speedup": speedup,
                        "rv_samples": rv_samples,
                        "rvv_samples": rvv_samples,
                        "rv_mean": rv_mean,
                        "rvv_mean": rvv_mean,
                        "rv_median": rv_median,
                        "rvv_median": rvv_median
                    })

            # **计算该测试集的整体平均提升**
            suite_comparison["avg_speedup"] = (total_speedup / count) if count > 0 else 0
            comparison_results.append(suite_comparison)

    return comparison_results

def generate_html(comparisons, output_path="test_report.html"):
    """生成 HTML 报告"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenCV RISC-V Vector 性能对比报告</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid black; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            .faster { background-color: #c8e6c9; } /* 绿色 - 提升 */
            .slower { background-color: #ffcdd2; } /* 红色 - 退步 */
            .neutral { background-color: #eeeeee; } /* 灰色 - 无变化 */
        </style>
    </head>
    <body>
        <h1>OpenCV RISC-V Vector 性能对比报告</h1>
    """

    for suite in comparisons:
        html_content += f"<h2>{suite['name']}（平均提升: {suite['avg_speedup']:.2f}%）</h2>"
        html_content += """
        <table>
            <tr>
                <th>测试用例</th>
                <th>RV 时间 (s)</th>
                <th>RVV 时间 (s)</th>
                <th>RV 采样</th>
                <th>RVV 采样</th>
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
                <td>{test['rv_samples']}</td>
                <td>{test['rvv_samples']}</td>
                <td>{test['rv_mean']:.0f}</td>
                <td>{test['rvv_mean']:.0f}</td>
                <td>{test['rv_median']:.0f}</td>
                <td>{test['rvv_median']:.0f}</td>
                <td>{test['speedup']:.2f}%</td>
            </tr>
            """

        html_content += "</table>"

    html_content += "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 报告已生成: {output_path}")

def generate_comparison_report():
    """生成最终对比报告"""
    test_report_pairs = [
        ("./output/RV_core_Abs_test_report.json", "./output/RVV_core_Abs_test_report.json"),
        ("./output/RV_core_Mul_test_report.json", "./output/RVV_core_Mul_test_report.json"),
        ("./output/RV_imgproc_Bilateral_test_report.json", "./output/RVV_imgproc_Bilateral_test_report.json"),
        ("./output/RV_imgproc_Resize_test_report.json", "./output/RVV_imgproc_Resize_test_report.json"),
    ]

    all_comparisons = []
    for rv_file, rvv_file in test_report_pairs:
        if os.path.exists(rv_file) and os.path.exists(rvv_file):
            all_comparisons.extend(compare_reports(rv_file, rvv_file))
        else:
            print(f"❌ 找不到文件: {rv_file} 或 {rvv_file}")

    generate_html(all_comparisons)

if __name__ == "__main__":
    generate_comparison_report()
