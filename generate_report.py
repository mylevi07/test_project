import json
import os
from datetime import datetime

def parse_allure_results(results_dir):
    """解析 allure-results 目录，生成测试摘要"""
    summary = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0, "cases": []}

    if not os.path.exists(results_dir):
        print(f"目录 {results_dir} 不存在")
        return summary

    for filename in os.listdir(results_dir):
        if not filename.endswith("-result.json"):
            continue
        filepath = os.path.join(results_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        case_info = {
            "name": data.get("name", "Unknown"),
            "status": data.get("status", "unknown"),
            "duration": data.get("time", {}).get("duration", 0) / 1000,  # 转为秒
        }

        summary["cases"].append(case_info)
        status = case_info["status"]
        if status in summary:
            summary[status] += 1
        summary["total"] += 1

    return summary

def print_report(summary):
    """打印报告到控制台"""
    print("\n" + "=" * 50)
    print("       Allure 测试报告摘要")
    print("=" * 50)
    print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  总计用例: {summary['total']}")
    print(f"  ✅ 通过: {summary['passed']}")
    print(f"  ❌ 失败: {summary['failed']}")
    print(f"  ⚠️  异常: {summary['broken']}")
    print(f"  ⏭️  跳过: {summary['skipped']}")
    print("-" * 50)

    for case in summary["cases"]:
        icon = "✅" if case["status"] == "passed" else "❌"
        print(f"  {icon} {case['name']} ({case['duration']:.2f}s)")

    print("=" * 50 + "\n")

if __name__ == "__main__":
    results = parse_allure_results("./allure-results")
    print_report(results)