# -*- coding: utf-8 -*-
"""文案生成器 - 自动生成商品标题、描述、推广内容"""
import random
from datetime import datetime

# ======= 平台特定模板 =======
PLATFORM_TEMPLATES = {
    '闲鱼': {
        'title_formats': [
            '{emoji} {name} 全新整理 | {highlight}',
            '{emoji} 急出！{name} 手慢无',
            '{emoji} {name} | 买一送三超值套餐',
            '{emoji} 9.9{name} 良心整理 直接上手',
        ],
        'closing_hooks': [
            '💰 一杯奶茶钱，值回票价！',
            '⏰ 手慢无，卖完下架！',
            '📦 下单秒发百度网盘链接！',
            '🎁 今日下单额外赠送XX！',
            '💯 不满意全额退款，放心拍！',
            '🌟 已经有1000+人在看啦！',
            '🔥 今日特价，错过等一年！',
        ],
    },
    '小红书': {
        'title_formats': [
            '{emoji} 救命！{name}真的太香了！{highlight}',
            '{emoji} 姐妹们！{name}分享给你们！',
            '{emoji} {name} | 干货分享，建议收藏',
            '{emoji} 用了{name}之后，我{benefit}',
            '{emoji} 普通人也能用{name}赚钱？',
        ],
        'closing_hooks': [
            '❤️ 觉得有用的话点赞收藏关注哦~',
            '💬 有问题评论区问我！',
            '✨ 想要的宝子私我！',
            '🌟 关注我，每天分享一个赚钱小技巧！',
            '💪 一起加油搞钱！',
        ],
    },
    '淘宝': {
        'title_formats': [
            '{emoji} {name} {highlight} | 官方正品 终身免费更新',
            '{emoji} 2025全新版 {name} | {highlight}',
        ],
        'closing_hooks': [
            '✅ 7天无理由退款',
            '✅ VIP专属客户支持',
            '✅ 购买后永久免费更新',
        ],
    },
    '朋友圈': {
        'title_formats': [
            '🔥 {name} | {highlight}',
        ],
        'closing_hooks': [
            '🔗 有需要的朋友直接私聊我！',
            '💬 朋友圈专属价，私聊获取！',
        ],
    },
}

# ======= 标签库 =======
TAG_LIBRARY = {
    'prompt': ['AI绘画', 'Prompt', 'Midjourney', 'Stable Diffusion', 'AI教程', 
               'AI头像', 'AI壁纸', '二次元', '治愈系', '每日分享', '干货'],
    'template': ['简历模板', 'PPT模板', 'Word模板', '求职', 'WPS', 'PPT', 
                 '职场', '创业', '融资BP', '设计素材'],
    'ebook': ['AI副业', '副业', '赚钱', '电子书', 'AI教程', '自由职业', 
              '搞钱', 'AI工具', '干货', '学习资料'],
}

# ======= 小红书爆款公式 =======
XHS_OPENERS = [
    "姐妹们！！！我终于找到了{product}！！！😭",
    "救命🆘 不会还有人不知道{product}吧！",
    "普通人用{product}真的能赚钱！我试试！",
    "{product}yyds！！用过的都说好！",
    "宝子们！这个{product}我不允许还有人没试过！",
    "全网最全{product}整理！建议收藏！",
]

XHS_STORY_STARTS = [
    "之前我也是小白一个，什么都不会...",
    "花了整整一个月整理，踩了无数坑...",
    "自从发现了{product}，我的效率直接翻倍！",
    "说实话一开始我也不信，直到我自己试了之后...",
]


def generate_listing_copy(product, platform='闲鱼'):
    """生成商品上架文案"""
    tmpl = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES['闲鱼'])
    
    name = product.get('name', '产品')
    desc = product.get('description', '')
    content = product.get('content', '')
    emoji = product.get('cover_emoji', '📦')
    price = product.get('price', 9.9)
    tags = product.get('tags', '')
    
    # 生成标题
    highlight = random.choice(['超值', '干货满满', '新手友好', '长期更新', '限量发售', '亲测有效'])
    title_format = random.choice(tmpl['title_formats'])
    title = title_format.replace('{emoji}', emoji).replace('{name}', name).replace('{highlight}', highlight)
    
    # 生成正文
    body_parts = []
    body_parts.append(f"【{name}】")
    body_parts.append("")
    if desc:
        body_parts.append(desc)
        body_parts.append("")
    if content:
        body_parts.append(content)
        body_parts.append("")
    
    # 价格信息
    if platform == '闲鱼':
        body_parts.append(f"💰 价格：{price}元（一杯奶茶钱）")
        body_parts.append("")
        body_parts.append("📦 购买方式：")
        body_parts.append("1. 直接拍下付款")
        body_parts.append("2. 我会发送百度网盘下载链接")
        body_parts.append("3. 有任何问题随时问我")
        body_parts.append("")
        body_parts.append("⚠️ 注意事项：")
        body_parts.append("• 虚拟商品，售出不退")
        body_parts.append("• 请勿二次转售")
        body_parts.append("• 仅供个人学习使用")
    elif platform == '小红书':
        body_parts.append(f"💰 价格：{price}元（私信购买）")
        body_parts.append("")
        body_parts.append("📌 想入手的宝子直接私我！")
        body_parts.append("评论区留言我也会回复的~")
    
    body_parts.append("")
    body_parts.append(random.choice(tmpl['closing_hooks']))
    
    body = '\n'.join(body_parts)
    
    # 生成标签
    tag_list = [t.strip() for t in tags.split(',') if t.strip()]
    if platform == '小红书':
        hashtags = ' '.join([f'#{t}' for t in tag_list[:8]])
    elif platform == '闲鱼':
        hashtags = ' '.join([f'#{t}' for t in tag_list[:5]])
    else:
        hashtags = ''
    
    return {
        'title': title,
        'body': body,
        'tags': hashtags,
        'platform': platform,
        'type': 'listing',
    }


def generate_xhs_post(product):
    """生成小红书笔记（种草式）"""
    name = product.get('name', '产品')
    emoji = product.get('cover_emoji', '✨')
    price = product.get('price', 9.9)
    tags = product.get('tags', '')
    category = product.get('category', '')
    
    opener = random.choice(XHS_OPENERS).replace('{product}', name)
    story_start = random.choice(XHS_STORY_STARTS).replace('{product}', name)
    
    tips_pool = {
        'prompt_pack': [
            '里面的Prompt都经过精心调试的！直接能用！',
            '还有负面Prompt大全，这个真的太实用了！',
            '配合Midjourney用，效果绝了！',
            '新手也能生成大师级作品！',
        ],
        'template': [
            '模板质量真的很高，不是那种粗糙货！',
            '下载就能用，Word/WPS直接打开！',
            '还有使用教程，新手也不怕！',
            '买了这个我简历直接过了初筛！',
        ],
        'ebook': [
            '内容超详细，从0到1都讲明白了！',
            '好几个赚钱方向亲测可行！',
            '工具清单直接抄作业就行！',
            '看完立刻有方向感了！',
        ],
        'sticker': [
            '太可爱了！聊天必备！',
            'AI生成的质量真的高！',
        ],
    }
    
    tips = tips_pool.get(category, tips_pool['prompt_pack'])
    selected_tips = random.sample(tips, min(3, len(tips)))
    
    hashtags = ' '.join([f'#{t.strip()}' for t in tags.split(',') if t.strip()][:10])
    extra_tags = '#AI #搞钱 #副业 #干货分享 #自学 #效率工具 #宝藏分享'
    
    body = f"""{emoji} {opener}

{story_start}

今天给大家分享一下我用{name}的真实感受：

{chr(10).join(f"✅ {t}" for t in selected_tips)}

💰 价格才{price}元，一杯奶茶钱！
📦 购买后秒发下载链接！

真的强烈推荐！特别适合：
• 想搞副业但没方向的宝子
• 想学AI但不知道怎么入门的新手
• 想买点AI工具试试水的朋友

{"".join(random.choice(PLATFORM_TEMPLATES['小红书']['closing_hooks']))}

{hashtags} {extra_tags}"""

    return {
        'title': f"{emoji} {name}真的太香了！💯",
        'body': body,
        'tags': hashtags + ' ' + extra_tags,
        'platform': '小红书',
        'type': 'xhs_note',
    }


def generate_wechat_friends_post(product):
    """生成朋友圈推广文案"""
    name = product.get('name', '产品')
    emoji = product.get('cover_emoji', '✨')
    price = product.get('price', 9.9)
    desc = product.get('description', '')
    
    templates = [
        f"""【{name}】🔥

{desc}

💰 只要{price}元！
📦 下单秒发！
⚠️ 朋友圈专属福利，私信立减1元！

（扫码/截图私聊我）""",
        f"""今天推荐一个好东西 👇

{emoji} {name}
{desc}

原价很贵，现在只要{price}块钱 🎉
有需要的朋友直接私聊我就行！""",
        f"""💡 好东西自己会说话

{emoji} {name}
已经有好几个朋友买了都说好 ✅

只要{price}元，有需要找我 👋""",
    ]
    
    return {
        'title': f'{emoji} 好物分享',
        'body': random.choice(templates),
        'tags': '',
        'platform': '朋友圈',
        'type': 'wechat',
    }


def generate_qq_group_copy(product):
    """生成群推广文案"""
    name = product.get('name', '产品')
    emoji = product.get('cover_emoji', '✨')
    price = product.get('price', 9.9)
    desc = product.get('description', '')
    
    templates = [
        f"""【{emoji} 好物推荐】

{name}
{desc}

💰 {price}元 带走！
📦 直接发网盘链接

有需要的私我~""",
    ]
    
    return {
        'title': '好物推荐',
        'body': random.choice(templates),
        'tags': '',
        'platform': '群聊',
        'type': 'group',
    }


def generate_all_copies(product):
    """为产品生成全平台文案"""
    copies = []
    platforms = product.get('platforms', '闲鱼,小红书').split(',')
    
    if '闲鱼' in platforms:
        copies.append(generate_listing_copy(product, '闲鱼'))
    if '小红书' in platforms:
        copies.append(generate_listing_copy(product, '小红书'))
        copies.append(generate_xhs_post(product))
    if '淘宝' in platforms:
        copies.append(generate_listing_copy(product, '淘宝'))
    
    # 额外生成朋友圈和群聊
    copies.append(generate_wechat_friends_post(product))
    copies.append(generate_qq_group_copy(product))
    
    return copies


# ======= 自动生成促销/节日文案 =======
HOLIDAY_TEMPLATES = {
    '双十一': ['双11大促！全场8折！错过再等一年！', '双11狂欢节，买二送一！'],
    '618': ['618年中大促，历史最低价！', '618狂欢，下单立减！'],
    '春节': ['春节特惠，不打烊！365天无休发货！', '新年新气象，新年新技能！'],
    '毕业季': ['毕业季福利！简历模板买一送一！', '应届生专属优惠，限时7折！'],
    '开学季': ['开学装备更新！AI工具助你学业有成！', '新学期，新技能！'],
}


def generate_promo_copy(product, holiday=None):
    """生成促销文案"""
    name = product.get('name', '')
    emoji = product.get('cover_emoji', '🎉')
    
    if holiday and holiday in HOLIDAY_TEMPLATES:
        hook = random.choice(HOLIDAY_TEMPLATES[holiday])
    else:
        hooks = [
            '限时特惠', '今日特价', '新客专享', '买二送一', '限量发售',
            '最后50份', '原价99现价9.9', '清仓大甩卖',
        ]
        hook = random.choice(hooks)
    
    return f"""{emoji} {hook}！

【{name}】

📌 产品优势不变
📌 价格全网最低
📌 库存有限，先到先得

💬 有需要直接拍下或私信我！"""


if __name__ == '__main__':
    # 测试
    test_product = {
        'name': 'AI绘画Prompt包·治愈系 50组',
        'description': '50组精心调试的Prompt，适用于Midjourney',
        'content': '详细内容...',
        'cover_emoji': '🎨',
        'price': 9.9,
        'tags': 'AI绘画,Prompt,Midjourney,治愈系',
        'platforms': '闲鱼,小红书',
        'category': 'prompt_pack',
    }
    
    copies = generate_all_copies(test_product)
    for c in copies:
        print(f"\n===== [{c['platform']}] {c['type']} =====")
        print(f"标题: {c['title']}")
        print(f"正文(前100字): {c['body'][:100]}...")
