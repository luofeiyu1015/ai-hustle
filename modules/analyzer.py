# -*- coding: utf-8 -*-
"""市场分析 & 每日报告模块"""
import random
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/workspace/ai_hustle')
from modules import database as db

# ======= 热门选品建议池 =======
HOT_NICHES = [
    {'niche': 'AI头像/Prompt', 'platform': '小红书+闲鱼', 'reason': '女生用户多，喜欢头像；客单价10-20元', 'score': 95},
    {'niche': '简历模板', 'platform': '闲鱼', 'reason': '求职季刚需，可分应届生/职场人', 'score': 85},
    {'niche': 'PPT模板（创业BP）', 'platform': '闲鱼+淘宝', 'reason': '创业者需要，客单价30-50元', 'score': 80},
    {'niche': 'AI赚钱/副业电子书', 'platform': '小红书', 'reason': '付费意愿强，客单价可做高', 'score': 88},
    {'niche': 'AI绘画教程', 'platform': '小红书', 'reason': '从入门到进阶，可做成系列', 'score': 90},
    {'niche': '小红书素材包', 'platform': '闲鱼', 'reason': '博主刚需，封面/字体/免抠素材', 'score': 78},
    {'niche': '公众号排版模板', 'platform': '闲鱼', 'reason': '公众号作者需要', 'score': 72},
    {'niche': 'AI情侣头像', 'platform': '小红书', 'reason': '刚需+社交分享属性', 'score': 82},
    {'niche': 'AI表情包/贴纸', 'platform': '闲鱼', 'reason': '低价引流，带动高客单价产品', 'score': 65},
    {'niche': '婚礼/纪念日PPT', 'platform': '淘宝', 'reason': '垂直细分，竞争小', 'score': 70},
]

PRICING_STRATEGIES = [
    {'name': '引流款+利润款', 'desc': '9.9元低价品引流 + 39.9元利润款赚钱 + 99元旗舰款形象',
     'products': '1个6.6元表情包 + 3个9.9-19.9元Prompt/Template + 1个39.9元电子书'},
    {'name': '爆款单品', 'desc': '集中打造1-2个爆款单品，价格9.9-29.9元',
     'products': '集中精力做2-3个精品产品，打磨好文案和封面'},
    {'name': '组合套餐', 'desc': '打包多个产品成套餐，提高客单价',
     'products': 'Prompt包 + 模板 + 电子书 = 49.9元 组合套餐'},
]

PLATFORM_STRATEGIES = {
    '闲鱼': {
        'daily_actions': ['上新1-2个产品', '擦亮所有产品', '回复所有消息(15分钟内)', '逛同类产品评论区', '每天发1条动态'],
        'tips': '• 产品标题要带关键词\n• 首图用好看的封面图\n• 文案里要写清楚"秒发""永久使用"\n• 客户消息一定要快回！\n• 定期降价/领券活动增加曝光',
    },
    '小红书': {
        'daily_actions': ['发1-2条笔记', '回复所有评论和私信', '逛同领域内容点赞评论', '主页保持统一风格', '关注10个同行'],
        'tips': '• 笔记开头要有钩子（救命！姐妹们！）\n• 正文要真诚，像和朋友分享\n• 结尾引导点赞收藏关注\n• 私信话术要专业热情\n• 图片至少3-5张，要有对比图/效果图',
    },
    '淘宝': {
        'daily_actions': ['客服在线8小时+', '优化标题关键词', '参加平台活动', '维护好评率', '直通车测款'],
        'tips': '• 主图点击率最重要\n• 详情页要打信任牌\n• 新品有流量扶持\n• 销量起来后开直通车',
    },
}


def analyze_market(keyword=None):
    """分析市场机会"""
    results = []
    
    # 基于数据库中的市场数据
    market_data = db.get_market_data(keyword)
    
    for md in market_data:
        results.append({
            'keyword': md['keyword'],
            'platform': md['platform'],
            'hot_score': md['hot_score'],
            'competition': md['competition'],
            'avg_price': md['avg_price'],
            'suggestion': md['suggestion'],
            'opportunity_score': md['hot_score'] * (10 - md['competition']) / 10,
        })
    
    # 基于热门选品池补充建议
    for niche in HOT_NICHES:
        if keyword and keyword not in niche['niche']:
            continue
        results.append({
            'keyword': niche['niche'],
            'platform': niche['platform'],
            'hot_score': niche['score'],
            'competition': random.randint(3, 8),
            'avg_price': round(random.uniform(9.9, 49.9), 1),
            'suggestion': niche['reason'],
            'opportunity_score': niche['score'] * random.uniform(0.4, 0.8),
        })
    
    # 按机会分数排序
    results.sort(key=lambda x: x['opportunity_score'], reverse=True)
    return results


def get_pricing_strategy():
    """获取定价策略建议"""
    return PRICING_STRATEGIES


def get_platform_strategy(platform):
    """获取平台运营策略"""
    return PLATFORM_STRATEGIES.get(platform, {})


def get_daily_tasks():
    """获取今日任务清单"""
    tasks = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 产品相关
    active_products = db.get_all_products('active')
    tasks.append({
        'type': 'product',
        'title': '检查产品状态',
        'desc': f'当前有 {len(active_products)} 个在售产品',
        'priority': 'high',
        'done': False,
    })
    
    # 新增产品建议
    if len(active_products) < 5:
        tasks.append({
            'type': 'new_product',
            'title': '建议新增产品',
            'desc': '在售产品少于5个，建议今天新增1-2个产品',
            'priority': 'medium',
            'done': False,
        })
    
    # 平台运营
    for platform in ['闲鱼', '小红书']:
        strategy = PLATFORM_STRATEGIES.get(platform, {})
        for action in strategy.get('daily_actions', [])[:2]:
            tasks.append({
                'type': 'marketing',
                'title': f'[{platform}] {action}',
                'desc': f'{platform}平台每日任务',
                'priority': 'medium',
                'done': False,
            })
    
    return tasks


def generate_daily_report():
    """生成今日报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 查询今日交易
    today_transactions = db.get_transactions(1)
    today_income = sum(t['amount'] for t in today_transactions if t['type'] == 'income')
    today_cost = sum(t['amount'] for t in today_transactions if t['type'] == 'expense')
    today_sales = sum(1 for t in today_transactions if t['type'] == 'income')
    
    # 查询总览
    summary = db.get_transaction_summary()
    
    # 热销产品
    products = db.get_all_products()
    hot_product = max(products, key=lambda p: p.get('sales_count', 0)) if products else None
    
    # 失败经验
    lessons = db.get_lessons()
    today_lesson = random.choice(lessons) if lessons else None
    
    # 明日计划
    tomorrow_plan_items = []
    if today_income < 50:
        tomorrow_plan_items.append('提升产品吸引力，考虑降价促销或加赠品')
    if len(products) < 5:
        tomorrow_plan_items.append('新增1-2个产品上架')
    if today_income > 0 and today_sales >= 3:
        tomorrow_plan_items.append('复制成功产品的模式，多上类似款')
    if not tomorrow_plan_items:
        tomorrow_plan_items.append('保持日常运营节奏，擦亮产品+回复消息')
    
    # 生成报告
    report = {
        'report_date': today,
        'revenue': round(today_income, 2),
        'cost': round(today_cost, 2),
        'net_profit': round(today_income - today_cost, 2),
        'sales_count': today_sales,
        'top_product': hot_product['name'] if hot_product else '暂无销售数据',
        'lessons_learned': today_lesson['title'] if today_lesson else '持续学习，不断优化',
        'tomorrow_plan': '；'.join(tomorrow_plan_items),
        'summary_total': summary,
    }
    
    # 保存报告
    db.save_report(report)
    
    return report


def format_report_text(report):
    """格式化报告为可读文本"""
    return f"""📊 AI副业每日报告 - {report['report_date']}
{'='*40}

💰 今日收入：{report['revenue']} 元
💸 今日支出：{report['cost']} 元
📈 今日净利润：{report['net_profit']} 元
🛒 今日销量：{report['sales_count']} 单

🔥 累计总收入：{report['summary_total'].get('total_income', 0)} 元
📉 累计净利润：{report['summary_total'].get('net_profit', 0)} 元
📦 热销产品：{report['top_product']}

{'='*40}

💡 今日经验：
{report['lessons_learned']}

📋 明日计划：
{report['tomorrow_plan']}

{'='*40}
保持节奏，坚持就是胜利！💪"""


# ======= 财务预测 =======
def predict_revenue(days=30):
    """基于历史数据预测收入"""
    summary = db.get_transaction_summary()
    total_income = summary.get('total_income', 0)
    total_sales = summary.get('sales_count', 0)
    
    if total_sales == 0:
        # 没有历史数据时给一个保守但有希望的预测
        daily_income_expected = random.uniform(10, 50)
    else:
        avg_transaction = total_income / total_sales
        # 假设每天1-5单
        daily_income_expected = avg_transaction * random.uniform(1, 3)
    
    predicted = round(daily_income_expected * days, 2)
    
    return {
        'period': f'{days}天',
        'predicted_daily_income': round(daily_income_expected, 2),
        'predicted_total': predicted,
        'confidence': 'medium' if total_sales > 5 else 'low',
        'note': '实际收入取决于产品质量、运营执行和市场竞争'
    }


if __name__ == '__main__':
    db.init_db()
    print("=== 市场分析 ===")
    opportunities = analyze_market()
    for o in opportunities[:5]:
        print(f"  [{o['keyword']}] 机会分:{o['opportunity_score']:.1f} 热:{o['hot_score']} 竞:{o['competition']} 价:{o['avg_price']}")
    
    print("\n=== 每日任务 ===")
    for t in get_daily_tasks():
        print(f"  [{t['priority']}] {t['title']}")
    
    print("\n=== 每日报告 ===")
    report = generate_daily_report()
    print(format_report_text(report))
    
    print("\n=== 收入预测(30天) ===")
    print(predict_revenue(30))
