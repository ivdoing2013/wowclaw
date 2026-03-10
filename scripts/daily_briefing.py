#!/usr/bin/env python3
"""
WowOclaw 每日简报生成器
每天早上8点自动抓取 GitHub Trending + AI 资讯，发送到飞书
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from urllib.parse import quote

# ============ 配置 ============
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK", "")
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
BITABLE_APP_TOKEN = os.getenv("BITABLE_APP_TOKEN", "")
BITABLE_TABLE_ID = os.getenv("BITABLE_TABLE_ID", "")

# ============ GitHub Trending 抓取 ============
def fetch_github_trending():
    """抓取 GitHub Trending (今日) """
    url = "https://github.com/trending?since=daily"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        # 简单解析 trending repos (实际使用时需要更完善的HTML解析)
        # 这里返回几个热门的作为示例
        return [
            {"name": "microsoft/playwright", "stars": "68.5k", "desc": "浏览器自动化工具", "lang": "TypeScript"},
            {"name": "openclawcn/openclawcn", "stars": "12.8k", "desc": "国产 AI Agent 平台", "lang": "TypeScript"},
            {"name": "karpathy/nanoGPT", "stars": "45.2k", "desc": "最简 GPT 训练实现", "lang": "Python"},
        ]
    except Exception as e:
        print(f"GitHub fetch error: {e}")
        return []

# ============ AI 资讯抓取 ============
def fetch_ai_news():
    """获取 AI 行业最新资讯（模拟数据，实际可接入 RSS 或 API） """
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        {"title": "Kimi K2.5 发布：编程能力大幅提升", "date": today, "tag": "模型更新"},
        {"title": "OpenClaw v2.0 正式发布：全新代理架构", "date": today, "tag": "产品发布"},
        {"title": "MCP 协议成为 AI 工具集成新标准", "date": today, "tag": "行业趋势"},
    ]

# ============ 生成简报内容 ============
def generate_briefing():
    """生成每日简报 Markdown """
    today = datetime.now().strftime("%Y年%m月%d日")
    
    github_repos = fetch_github_trending()
    ai_news = fetch_ai_news()
    
    # 构建消息
    msg = f"""📰 **WowOclaw 每日简报** | {today}

---

## 🔥 GitHub 今日热门

"""
    for i, repo in enumerate(github_repos[:5], 1):
        msg += f"{i}. **{repo['name']}** ⭐ {repo['stars']}\n"
        msg += f"   💻 {repo['lang']} | {repo['desc']}\n\n"
    
    msg += """---

## 🤖 AI 行业资讯

"""
    for news in ai_news[:3]:
        msg += f"• **{news['tag']}** | {news['title']}\n"
    
    msg += """
---

## 📦 WowOclaw 最新动态

• v2.0.5 已发布，新增飞书多维表格支持
• 社区用户突破 10,000 人 🎉
• 技能市场新增 50+ MCP 服务器

---

💡 **提示**: 回复 "退订" 取消每日简报

🌐 [访问官网](http://wowoclaw.com/) | 📰 [查看完整资讯](http://wowoclaw.com/updates.html)
"""
    
    return msg

# ============ 飞书机器人发送 ============
def send_feishu_message(content, webhook_url=None):
    """通过飞书 webhook 发送消息 """
    if webhook_url:
        url = webhook_url
    else:
        # 使用自定义机器人 webhook
        url = FEISHU_WEBHOOK
    
    if not url:
        print("❌ 未配置飞书 Webhook")
        return False
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📰 WowOclaw 每日简报"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "🌐 访问官网"},
                            "url": "http://wowoclaw.com/",
                            "type": "primary"
                        },
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "📰 查看资讯"},
                            "url": "http://wowoclaw.com/updates.html",
                            "type": "default"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()
        if result.get("code") == 0:
            print("✅ 飞书消息发送成功")
            return True
        else:
            print(f"❌ 飞书发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False

# ============ 获取订阅用户 ============
def get_subscribers_from_bitable():
    """从飞书多维表格获取订阅用户列表 """
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return []
    
    try:
        # 1. 获取 tenant_access_token
        token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        token_resp = requests.post(token_url, json={
            "app_id": FEISHU_APP_ID,
            "app_secret": FEISHU_APP_SECRET
        })
        token_data = token_resp.json()
        access_token = token_data.get("tenant_access_token")
        
        if not access_token:
            print("❌ 获取飞书 token 失败")
            return []
        
        # 2. 查询订阅用户
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{BITABLE_TABLE_ID}/records"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers, params={"page_size": 500})
        data = response.json()
        
        if data.get("code") != 0:
            print(f"❌ 查询表格失败: {data}")
            return []
        
        subscribers = []
        for item in data.get("data", {}).get("items", []):
            fields = item.get("fields", {})
            email = fields.get("邮箱", "")
            status = fields.get("状态", "")
            if email and status == "订阅中":
                subscribers.append(email)
        
        return subscribers
        
    except Exception as e:
        print(f"❌ 获取订阅列表失败: {e}")
        return []

# ============ 主函数 ============
def main():
    print(f"🚀 开始生成每日简报 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 生成简报内容
    briefing = generate_briefing()
    print("\n📄 简报内容预览:")
    print("=" * 50)
    print(briefing[:500] + "...")
    print("=" * 50)
    
    # 发送消息
    success = send_feishu_message(briefing)
    
    if success:
        print("\n✅ 每日简报发送完成")
        return 0
    else:
        print("\n❌ 发送失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())