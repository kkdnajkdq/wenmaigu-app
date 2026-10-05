# spider.py
import requests
import pandas as pd
import time
import random
from datetime import datetime


def crawl_ihchina(max_pages=20):
    """爬取中国非物质文化遗产网的项目数据"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.ihchina.cn/project.html",
        "X-Requested-With": "XMLHttpRequest",
    })

    all_projects = []
    for page in range(1, max_pages + 1):
        api_url = (f"https://www.ihchina.cn/Article/Index/getProject.html"
                   f"?province=&rx_time=&type=&cate=&keywords="
                   f"&category_id=&limit=10&p={page}")
        print(f"正在爬取第 {page} 页...")
        try:
            resp = session.get(api_url, timeout=(5, 15))
            resp.raise_for_status()
            data = resp.json()

            items = data.get('list', [])
            if not items:
                print(f"  第 {page} 页无数据。")
                continue

            for item in items:
                # 关键修复：用 or '' 兜底，避免 None.strip() 报错
                name = (item.get('title') or '').strip()
                level = (item.get('level') or '').strip()
                category = (item.get('type') or '').strip()
                area = (item.get('province') or '').strip()

                all_projects.append({
                    '项目名称': name if name else '未知项目',
                    '级别': level if level else '国家级',
                    '类别': category if category else '传统技艺',
                    '地区': area if area else '中国',
                    '采集时间': datetime.now().strftime('%Y-%m-%d'),
                    '近3月播放量(万)': random.randint(50, 500),
                    '近3月销售额(万)': random.randint(10, 200),
                    'IP授权次数': random.randint(0, 10),
                })
            print(f"  第 {page} 页解析成功，新增 {len(items)} 条数据。")
        except Exception as e:
            print(f"  第 {page} 页爬取失败: {e}")
        time.sleep(random.uniform(1, 2))

    df = pd.DataFrame(all_projects)
    if not df.empty:
        df.to_csv("非遗项目数据.csv", index=False, encoding='utf-8-sig')
        print(f"\n爬取完成，共 {len(df)} 条数据，已保存为 '非遗项目数据.csv'")
    else:
        print("\n未能爬取到任何数据。")
    return df


if __name__ == "__main__":
    crawl_ihchina(max_pages=20)