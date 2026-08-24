#!/usr/bin/env python3
"""更新README中的API状态表格"""

import json
import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

# API配置 (名称, 支持IP查询, 分类, URL模板)
# 分类: 1=可查询本机IP和通过IP查询信息, 2=只可查询本机IP, 3=只可通过IP查询, 4=已失效
API_CONFIG = {
    # === 1. 可查询本机IP和通过IP查询信息 ===
    "ip-api.com": {
        "name": "ip-api.com",
        "supports_ip": True,
        "category": 1,
        "url": "http://ip-api.com/json/{ip}?lang=zh-CN",
    },
    "demo.ip-api.com": {
        "name": "demo.ip-api.com",
        "supports_ip": True,
        "category": 1,
        "url": "http://demo.ip-api.com/json/{ip}?fields=66842623&lang=zh-CN",
    },
    "pconline": {
        "name": "pconline",
        "supports_ip": True,
        "category": 1,
        "url": "https://whois.pconline.com.cn/ipJson.jsp?ip={ip}&json=true",
    },
    "ip.sb": {
        "name": "ip.sb",
        "supports_ip": True,
        "category": 1,
        "url": "https://api.ip.sb/geoip/{ip}",
    },
    "ip2location.io": {
        "name": "ip2location.io",
        "supports_ip": True,
        "category": 1,
        "url": "https://api.ip2location.io/?ip={ip}",
    },
    "realip.cc": {
        "name": "realip.cc",
        "supports_ip": True,
        "category": 1,
        "url": "https://realip.cc/?ip={ip}",
    },
    "ipapi.co": {
        "name": "ipapi.co",
        "supports_ip": True,
        "category": 1,
        "url": "https://ipapi.co/{ip}/json/",
    },
    "ipapi.is": {
        "name": "ipapi.is",
        "supports_ip": True,
        "category": 1,
        "url": "https://api.ipapi.is/?ip={ip}",
    },
    "db-ip.com": {
        "name": "db-ip.com",
        "supports_ip": True,
        "category": 1,
        "url": "https://api.db-ip.com/v2/free/{ip}",
    },
    "freeipapi.com": {
        "name": "freeipapi.com",
        "supports_ip": True,
        "category": 1,
        "url": "https://freeipapi.com/api/json/{ip}",
    },
    "ipwhois.app": {
        "name": "ipwhois.app",
        "supports_ip": True,
        "category": 1,
        "url": "https://ipwhois.app/json/{ip}?format=json",
    },
    "ip.nc.gy": {
        "name": "ip.nc.gy",
        "supports_ip": True,
        "category": 1,
        "url": "https://ip.nc.gy/json?ip={ip}",
    },
    "ipdata.info": {
        "name": "ipdata.info",
        "supports_ip": True,
        "category": 1,
        "url": "https://ipdata.info/json/{ip}",
    },
    "ipwtf.com": {
        "name": "ipwtf.com",
        "supports_ip": True,
        "category": 1,
        "url": "https://ipwtf.com/api/whois/{ip}",
    },
    "geojs.io": {
        "name": "geojs.io",
        "supports_ip": True,
        "category": 1,
        "url": "https://get.geojs.io/v1/ip/geo/{ip}.json",
    },
    "baidu.opendata": {
        "name": "baidu.opendata",
        "supports_ip": True,
        "category": 1,
        "url": "https://opendata.baidu.com/api.php?co=&resource_id=6006&oe=utf8&query={ip}",
    },
    # === 2. 只可查询本机IP ===
    "httpbin.org": {
        "name": "httpbin.org",
        "supports_ip": False,
        "category": 2,
        "url": "http://httpbin.org/ip",
    },
    "cdid.ctrip": {
        "name": "cdid.ctrip",
        "supports_ip": False,
        "category": 2,
        "url": "https://cdid.c-ctrip.com/model-poc2/h",
    },
    "qq.video": {
        "name": "qq.video",
        "supports_ip": False,
        "category": 2,
        "url": "https://vv.video.qq.com/checktime?otype=ojson",
    },
    "test.ipw.cn": {
        "name": "test.ipw.cn",
        "supports_ip": False,
        "category": 2,
        "url": "https://test.ipw.cn/api/ip/myip?json",
    },
    "api.ipify.org": {
        "name": "api.ipify.org",
        "supports_ip": False,
        "category": 2,
        "url": "https://api.ipify.org?format=json",
    },
    "my.ipinfo.app": {
        "name": "my.ipinfo.app",
        "supports_ip": False,
        "category": 2,
        "url": "https://ipv4.my.ipinfo.app/api/ipDetails.php",
    },
    "g3.letv": {
        "name": "g3.letv",
        "supports_ip": False,
        "category": 2,
        "url": "https://g3.letv.com/r?format=1",
    },
    "qq.inews": {
        "name": "qq.inews",
        "supports_ip": False,
        "category": 2,
        "url": "https://r.inews.qq.com/api/ip2city",
    },
    "myip.ipip.net": {
        "name": "myip.ipip.net",
        "supports_ip": False,
        "category": 2,
        "url": "https://myip.ipip.net/json",
    },
    "ifconfig.me": {
        "name": "ifconfig.me",
        "supports_ip": False,
        "category": 2,
        "url": "https://ifconfig.me/all.json",
    },
    "geolocation-db.com": {
        "name": "geolocation-db.com",
        "supports_ip": False,
        "category": 2,
        "url": "https://geolocation-db.com/json",
    },
    "api.myip.com": {
        "name": "api.myip.com",
        "supports_ip": False,
        "category": 2,
        "url": "https://api.myip.com",
    },
    "wtfismyip.com": {
        "name": "wtfismyip.com",
        "supports_ip": False,
        "category": 2,
        "url": "https://wtfismyip.com/json",
    },
    "ipbase.com": {
        "name": "ipbase.com",
        "supports_ip": False,
        "category": 2,
        "url": "https://api.ipbase.com/v1/json",
    },
    "ipquery.io": {
        "name": "ipquery.io",
        "supports_ip": False,
        "category": 2,
        "url": "https://api.ipquery.io/?format=json",
    },
    "cloudflare.trace": {
        "name": "cloudflare.trace",
        "supports_ip": False,
        "category": 2,
        "url": "https://1.1.1.1/cdn-cgi/trace",
    },
    "torproject": {
        "name": "torproject",
        "supports_ip": False,
        "category": 2,
        "url": "https://check.torproject.org/api/ip",
    },
    "bilibili": {
        "name": "bilibili",
        "supports_ip": False,
        "category": 2,
        "url": "https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo",
    },
    "news.qq": {
        "name": "news.qq",
        "supports_ip": False,
        "category": 2,
        "url": "https://i.news.qq.com/api/ip2city",
    },
    "gdt.qq": {
        "name": "gdt.qq",
        "supports_ip": False,
        "category": 2,
        "url": "https://ipv4.gdt.qq.com/get_client_ip",
    },
    "uapis.cn": {
        "name": "uapis.cn",
        "supports_ip": False,
        "category": 2,
        "url": "https://uapis.cn/api/v1/network/myip",
    },
    "cip.cc": {
        "name": "cip.cc",
        "supports_ip": True,
        "category": 2,
        "url": "http://www.cip.cc/{ip}",
    },
    # === 3. 只可通过IP查询 ===
    "ipinfo.io": {
        "name": "ipinfo.io",
        "supports_ip": True,
        "category": 3,
        "url": "https://ipinfo.io/widget/demo/{ip}",
    },
    "db-ip.demo": {
        "name": "db-ip.demo",
        "supports_ip": True,
        "category": 3,
        "url": "https://db-ip.com/demo/home.php?s={ip}",
    },
    "iqiyi.mesh": {
        "name": "iqiyi.mesh",
        "supports_ip": True,
        "category": 3,
        "url": "https://mesh.if.iqiyi.com/aid/ip/info?ip={ip}",
    },
    "ip9.com.cn": {
        "name": "ip9.com.cn",
        "supports_ip": True,
        "category": 3,
        "url": "https://ip9.com.cn/get?ip={ip}",
    },
    # === 4. 已失效的API ===
    "meitu.webapi": {
        "name": "meitu.webapi",
        "supports_ip": True,
        "category": 4,
        "url": "https://webapi-pc.meitu.com/common/ip_location?ip={ip}",
    },
    "ip.cn": {
        "name": "ip.cn",
        "supports_ip": True,
        "category": 4,
        "url": "https://www.ip.cn/api/index?ip={ip}&type=0",
    },
    "vore.top": {
        "name": "vore.top",
        "supports_ip": True,
        "category": 4,
        "url": "https://api.vore.top/api/IPdata?ip={ip}",
    },
    "qjqq.cn": {
        "name": "qjqq.cn",
        "supports_ip": True,
        "category": 4,
        "url": "https://api.qjqq.cn/api/Local?ip={ip}",
    },
    "csdn.searchplugin": {
        "name": "csdn.searchplugin",
        "supports_ip": True,
        "category": 4,
        "url": "https://searchplugin.csdn.net/api/v1/ip/get?ip={ip}",
    },
    "ip-api.io": {
        "name": "ip-api.io",
        "supports_ip": True,
        "category": 4,
        "url": "https://ip-api.io/json?ip={ip}",
    },
    "useragentinfo": {
        "name": "useragentinfo",
        "supports_ip": False,
        "category": 4,
        "url": "https://ip.useragentinfo.com/json",
    },
    "uomg.com": {
        "name": "uomg.com",
        "supports_ip": False,
        "category": 4,
        "url": "https://api.uomg.com/api/visitor.info?skey=1",
    },
    "baidu.qifu": {
        "name": "baidu.qifu",
        "supports_ip": False,
        "category": 4,
        "url": "https://qifu-api.baidubce.com/ip/local/geo/v1/district",
    },
    "ipapi.com": {
        "name": "ipapi.com",
        "supports_ip": True,
        "category": 4,
        "url": "https://ipapi.com/ip_api.php?ip={ip}",
    },
}


def get_api_status(api_name: str) -> dict:
    """获取API状态"""
    api_dir = REPOSITORY_ROOT / "output" / "by_api" / api_name
    if not api_dir.exists():
        return {
            "status": "unknown",
            "elapsed_ms": None,
            "count": 0,
            "success": 0,
            "failed": 0,
        }

    results = list(api_dir.glob("*.json"))
    if not results:
        return {
            "status": "unknown",
            "elapsed_ms": None,
            "count": 0,
            "success": 0,
            "failed": 0,
        }

    success_count = 0
    failed_count = 0
    total_elapsed = 0

    for result_file in results:
        try:
            with open(result_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("status") == "success":
                    success_count += 1
                    total_elapsed += data.get("elapsed_ms", 0)
                else:
                    failed_count += 1
        except Exception:
            failed_count += 1

    avg_elapsed = round(total_elapsed / success_count, 2) if success_count > 0 else None

    if failed_count == 0 and success_count > 0:
        status = "success"
    elif success_count == 0:
        status = "failed"
    else:
        status = "partial"

    return {
        "status": status,
        "elapsed_ms": avg_elapsed,
        "count": len(results),
        "success": success_count,
        "failed": failed_count,
    }


def get_status_icon(status: str) -> str:
    """获取状态图标"""
    icons = {"success": "✅", "failed": "❌", "partial": "⚠️", "unknown": "❓"}
    return icons.get(status, "❓")


def generate_readme_table() -> str:
    """生成README中的API状态表格"""
    from datetime import datetime, timezone, timedelta
    from urllib.parse import quote

    utc_time = datetime.now(timezone.utc)
    update_time_utc = utc_time.strftime("%Y-%m-%d %H:%M")
    update_time_cst = utc_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")

    test_ips = ["117.30.120.138", "1.1.1.1", "8.8.8.8", "223.5.5.5", "9.9.9.9"]
    test_ip = test_ips[0]
    test_ips_str = ", ".join(test_ips)

    # 定义分类顺序
    category_order = [1, 2, 3, 4]
    category_names = {
        1: "🔎 支持查询指定IP的API",
        2: "📍 仅查询本机IP的API",
        3: "🎯 仅支持查询指定IP的API",
        4: "⚠️ 已失效的API",
    }

    output_lines = []
    output_lines.append("## 📊 API状态监控\n")
    output_lines.append(f"> Updated at UTC+0: {update_time_utc}\n")
    output_lines.append(f"> 由 GitHub Actions 自动更新于 (UTC+8): {update_time_cst}\n")
    output_lines.append(f"> 测试IP: {test_ips_str}\n")

    # 按分类顺序生成表格
    for category in category_order:
        output_lines.append(f"\n### {category_names[category]}\n")
        output_lines.append("| 测试 | API | 状态 | 平均响应 | 成功率 | 详情 |")
        output_lines.append("|------|-----|------|---------|--------|------|")

        # 按test_apis.py中的顺序输出
        api_order = []
        for api_name, config in API_CONFIG.items():
            if config["category"] == category:
                api_order.append(api_name)

        for api_name in api_order:
            config = API_CONFIG[api_name]
            stat = get_api_status(api_name)
            icon = get_status_icon(stat["status"])
            elapsed = f"{stat['elapsed_ms']}ms" if stat["elapsed_ms"] else "-"
            success_rate = (
                f"{stat['success']}/{stat['count']}" if stat["count"] > 0 else "-"
            )
            url = config.get("url", "")
            if config["supports_ip"]:
                url = url.replace("{ip}", test_ip)
            badge_url = f"https://img.shields.io/website?url={quote(url, safe='')}&label={api_name}"
            shield_link = f"[![{api_name}]({badge_url})]({url})"
            detail_link = f"[📁 查看](output/by_api/{api_name}/)"
            output_lines.append(
                f"| {shield_link} | {api_name} | {icon} | {elapsed} | {success_rate} | {detail_link} |"
            )

    return "\n".join(output_lines)


def update_readme():
    """更新README文件"""
    readme_path = REPOSITORY_ROOT / "README.md"

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 查找 <!-- API_STATUS_START --> 和 <!-- API_STATUS_END --> 之间的内容
    pattern = r"<!-- API_STATUS_START -->.*?<!-- API_STATUS_END -->"
    new_table = generate_readme_table()
    placeholder = f"<!-- API_STATUS_START -->\n{new_table}\n<!-- API_STATUS_END -->"

    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, placeholder, content, flags=re.DOTALL)
    else:
        # 如果没有占位符，添加到文件末尾
        content += "\n\n" + placeholder

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md updated successfully!")


if __name__ == "__main__":
    update_readme()
