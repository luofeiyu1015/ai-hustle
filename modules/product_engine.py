# -*- coding: utf-8 -*-
"""产品生成引擎 - 自动生成各类数字产品内容"""
import random
import json
from datetime import datetime

# ======= Prompt 包生成数据 =======
PROMPT_STYLES = {
    '治愈系_插画': {
        'tags': ['治愈', '温暖', '柔和', '梦境', '童话'],
        'subjects': ['森林小屋', '海边落日', '星空下的猫', '雨后街道', '咖啡馆', '花丛中的少女', 
                    '山顶云海', '冬日暖阳', '秋日枫叶', '春日樱花'],
        'modifiers': ['soft lighting', 'pastel colors', 'warm tones', 'dreamy atmosphere', 
                     'gentle brush strokes', 'highly detailed', '8k resolution', 'masterpiece']
    },
    '动漫风_头像': {
        'tags': ['二次元', '日系', '萌系', '高冷', '酷'],
        'subjects': ['少女', '少年', '猫娘', '兔耳娘', '机械少女', '古风美人', '西装少年', 
                    '校服少女', '天使', '恶魔'],
        'modifiers': ['anime style', 'studio ghibli', 'makoto shinkai', 'detailed eyes',
                     'vibrant colors', 'cel shading', 'full body', 'portrait']
    },
    '写实_人像': {
        'tags': ['真实', '写真', '高级感', '时尚', '电影感'],
        'subjects': ['商务人士', '时尚模特', '文艺青年', '运动达人', '美食博主',
                    '摄影师', '画家', '音乐家', '程序员', '创业者'],
        'modifiers': ['photorealistic', 'cinematic lighting', '8k uhd', 'kodak portra 400',
                     'golden hour', 'shallow depth of field', 'professional photography', 'sony a7r iv']
    },
    '3D_卡通': {
        'tags': ['3D', 'Q版', '可爱', '萌', '立体'],
        'subjects': ['小怪兽', '独角兽', '太空人', '小熊', '兔兔', '小龙',
                    '小精灵', '机器人', '魔法少女', '超级英雄Q版'],
        'modifiers': ['3d render', 'pixar style', 'soft shadows', 'subsurface scattering',
                     'round shapes', 'pastel palette', 'studio lighting', 'octane render']
    },
    '国风_古风': {
        'tags': ['国风', '古风', '汉服', '东方', '仙气'],
        'subjects': ['汉服美人', '侠客', '书生', '仙子', '将军',
                    '花间饮酒', '月下抚琴', '竹林对弈', '登高望远', '江上独钓'],
        'modifiers': ['chinese traditional painting', 'ink wash', 'song dynasty aesthetic',
                     'silk texture', 'moonlight', 'cherry blossoms', 'bamboo grove', 'mountains']
    },
    '赛博朋克': {
        'tags': ['未来', '科幻', '霓虹灯', '酷炫', '机械'],
        'subjects': ['赛博城市', '机甲战士', '未来赛车', '虚拟少女', '机械臂',
                    '飞行汽车', '黑客', '义体改造人', '太空站', '量子计算机'],
        'modifiers': ['cyberpunk style', 'neon lights', 'rainy city', 'blade runner aesthetic',
                     'futuristic technology', 'holographic displays', 'chrome materials', 'octane render']
    },
    '自然_风景': {
        'tags': ['风景', '自然', '壮丽', '秘境', '壁纸'],
        'subjects': ['极光', '大峡谷', '马尔代夫海滩', '富士山', '张家界',
                    '冰岛瀑布', '撒哈拉沙漠', '北极冰川', '热带雨林', '梯田'],
        'modifiers': ['landscape photography', 'national geographic', 'wide angle', 'stunning vista',
                     'golden hour', 'long exposure', 'panoramic', 'ultra hd wallpaper']
    },
    '表情包': {
        'tags': ['搞笑', '可爱', '打工人', '职场', '聊天'],
        'subjects': ['打工人日常', '摸鱼', '加班', '开会', '老板画饼',
                    '发工资', '收快递', '奶茶续命', '周末躺平', '周一上班'],
        'modifiers': ['meme style', 'simple background', 'expressive face', 'comic sans',
                     'bold text', 'cute character', 'minimalist', 'viral meme format']
    },
}

# ======= 简历模板文案 =======
RESUME_CONTENT_TEMPLATES = {
    '应届生': {
        'summary_points': ['性格开朗，学习能力强', '在校期间GPA 3.8/4.0，专业排名前5%', 
                          '有过2-3段相关实习经历', '熟练使用Office/PS/Python等工具'],
        'sections': ['个人信息', '求职意向', '教育背景', '实习经历', '项目经历', '校园活动', '技能证书'],
    },
    '职场人': {
        'summary_points': ['3年以上相关工作经验', '独立负责过核心项目', 
                          '带领5-10人小团队', '有完整的项目交付案例'],
        'sections': ['个人信息', '个人评价', '工作经历', '项目经验', '管理经验', '专业技能', '教育背景'],
    },
    '设计类': {
        'summary_points': ['视觉/交互设计经验丰富', '作品集30+上线项目', 
                          '熟悉Figma/Sketch/PS/AI', '有品牌设计全链路经验'],
        'sections': ['个人信息', '个人优势', '工作经历', '设计作品集', '项目详情', '专业技能'],
    },
    '技术类': {
        'summary_points': ['熟练掌握主力编程语言', '有高并发系统开发经验', 
                          '熟悉微服务/云原生架构', '代码review和技术分享习惯'],
        'sections': ['个人信息', '技术栈概览', '工作经历', '核心项目', '开源贡献', '教育背景'],
    },
}

# ======= PPT模板分类 =======
PPT_CATEGORIES = [
    ('创业融资BP', '适合向投资人展示项目，包含市场、产品、团队、财务预测'),
    ('产品发布会', '新产品/新功能发布，酷炫动效+清晰卖点展示'),
    ('年度/季度总结', '工作汇报用，数据可视化+成果展示'),
    ('商业计划书', '完整的商业方案，包含市场分析、竞争、运营策略'),
    ('培训课件', '内部培训/公开课用，结构清晰+互动设计'),
    ('述职报告', '年度/季度述职，成果+反思+规划'),
    ('路演演讲', '短时间抓住注意力的演讲PPT，简洁有力'),
    ('教育课件', '老师教学用，知识点清晰+配图丰富'),
    ('营销方案', '市场活动策划，包含目标、策略、执行、预算'),
    ('项目提案', '向客户展示方案，专业美观+逻辑清晰'),
]

# ======= AI电子书目录模板 =======
EBOOK_OUTLINES = {
    'AI副业赚钱': [
        '前言：为什么2025是普通人用AI翻身的最佳时机',
        '第一章：AI副业的底层逻辑',
        '第二章：准备工作（账号/工具/心态）',
        '第三章：方向一：AI数字产品销售',
        '第四章：方向二：AI自媒体内容生产',
        '第五章：方向三：AI接单服务',
        '第六章：方向四：AI课程/知识付费',
        '第七章：方向五：AI社群运营',
        '第八章：方向六：AI电商选品',
        '第九章：方向七：AI本地生活服务',
        '第十章：方向八：AI企业服务',
        '第十一章：方向九：AI投资/交易辅助',
        '第十二章：方向十：AI工具二次开发',
        '第十三章：避坑指南（常见失败原因）',
        '第十四章：案例分析（真实月入过万的案例）',
        '第十五章：从0到1的30天执行计划',
        '结语：AI时代，不努力才是最大的风险',
        '附录：AI工具清单',
        '附录：常用Prompt模板',
    ],
}


def generate_prompt_pack(style_key='治愈系_插画', count=20):
    """生成 Prompt 包"""
    style = PROMPT_STYLES.get(style_key, PROMPT_STYLES['治愈系_插画'])
    prompts = []
    for i in range(count):
        subject = random.choice(style['subjects'])
        mod_count = random.randint(3, 6)
        mods = random.sample(style['modifiers'], min(mod_count, len(style['modifiers'])))
        cn_tags = random.sample(style['tags'], 2)
        # 构建 prompt
        if random.random() > 0.5:
            # 英文prompt
            prompt = f"{subject}, {', '.join(mods)}"
        else:
            # 中英混合
            en_mods = mods[:3]
            prompt = f"{subject}, {', '.join(cn_tags)}, {', '.join(en_mods)}"
        prompts.append({
            'id': i + 1,
            'prompt': prompt,
            'tags': cn_tags if random.random() > 0.3 else style['tags'][:3],
            'subject': subject
        })
    
    # 生成负面prompt
    negative_prompts = generate_negative_prompts()
    
    return {
        'style': style_key,
        'style_tags': style['tags'],
        'prompts': prompts,
        'negative_prompts': negative_prompts,
        'tips': [
            '建议配合 --ar 16:9 或 --ar 3:4 调整画幅',
            '高清放大可用 --upbeta 或 --up2x',
            '同一Prompt多跑几次，挑选最满意的',
            '可在Prompt基础上微调形容词获得不同效果',
        ],
        'generated_at': datetime.now().isoformat()
    }

def generate_negative_prompts():
    """生成负面Prompt合集"""
    return {
        '通用': ['low quality', 'blurry', 'distorted', 'ugly', 'bad anatomy', 
                'extra limbs', 'watermark', 'text', 'logo', 'cropped'],
        '人像': ['deformed hands', 'extra fingers', 'mutated', 'poorly drawn face',
                'facial asymmetry', 'double body', 'cloned face'],
        '风景': ['oversaturated', 'underexposed', 'noise', 'grain', 'compression artifacts'],
    }

def generate_resume_template_desc(target='应届生'):
    """生成简历模板产品描述"""
    tmpl = RESUME_CONTENT_TEMPLATES.get(target, RESUME_CONTENT_TEMPLATES['应届生'])
    
    desc = f"""📄 高端简历模板合集 · {target}专属版

✨ 产品亮点：
• 100+套精美简历模板，简约/商务/创意三大风格
• Word格式，下载即用，支持自定义修改
• 每套模板都有内容填充指导
• 附赠《简历撰写黄金法则》电子书（5000字）
• 附赠"简历关键词库"（1000+行业关键词）
• 免费更新，后续新增模板自动获得

📌 适用场景：
{chr(10).join(f'  ✅ {s}' for s in tmpl['summary_points'])}

📌 模板结构：
{chr(10).join(f'  • {s}' for s in tmpl['sections'])}

📌 使用方法：
1. 购买后收到百度网盘链接
2. 下载后用Word/WPS打开
3. 替换为自己的信息即可

📌 额外赠品：
• 面试技巧电子书
• 自我介绍模板（30秒/1分钟/3分钟版）
• 薪资谈判指南

⚠️ 注意：本模板仅用于求职，禁止商业转售"""
    
    return desc

def generate_ppt_template_desc(category_idx=0):
    """生成PPT模板产品描述"""
    name, desc = PPT_CATEGORIES[category_idx % len(PPT_CATEGORIES)]
    
    full_desc = f"""📊 {name}PPT模板合集

💡 模板简介：{desc}

✨ 产品亮点：
• 50+套专业设计模板，覆盖各种场景
• PPT/WPS原生格式，直接编辑
• 16:9宽屏 + 4:3标准 双版本
• 内置图表/图标库，配色统一
• 每套含30-50页常用页面
• 附赠使用教程视频
• 终身免费更新

📌 模板清单：
• 封面页 5款
• 目录页 5款  
• 章节页 5款
• 内容页（图文）15款
• 数据图表页 10款
• 对比/流程页 5款
• 结尾页 5款

📌 使用方法：
1. 购买后收到下载链接
2. 解压后选择喜欢的模板
3. 替换文字/图片即可快速完成

📌 额外赠品：
• 1000+商务图标包
• 50张免抠元素素材
• PPT动画效果教程"""
    
    return full_desc

def generate_ebook_outline(topic='AI副业赚钱'):
    """生成电子书大纲"""
    outline = EBOOK_OUTLINES.get(topic, EBOOK_OUTLINES['AI副业赚钱'])
    
    content = f"""📕 《{topic}实操手册》

{'='*40}

{f'{chr(10).join(f"{i+1}. {ch}" for i, ch in enumerate(outline))}'}

{'='*40}

📌 电子书特色：
• 实战导向，每个方向都有具体操作步骤
• 包含真实案例和数据
• 附带工具清单和Prompt模板
• 可复制执行，不需要编程基础
• 持续更新，购买后永久免费获得新版本

📌 适合谁：
• 想增加副业收入的上班族
• 想做自由职业的年轻人
• 刚毕业找不到满意工作的大学生
• 想抓住AI浪潮的创业者
• 任何想通过AI改变收入结构的人

📌 购买后：
1. 自动发送百度网盘下载链接
2. 同时发送邮箱备份
3. 加入读者社群（可选）"""
    
    return content

def generate_emoji_set(count=20, theme='打工人'):
    """生成表情包/头像emoji文案"""
    themes = {
        '打工人': ['摸鱼中', '打工魂', '搬砖使我快乐', '又是元气满满的一天', '我爱工作',
                  '发工资啦', '老板又画饼', '周末快来', '不想加班', '奶茶续命',
                  '开会中勿扰', '甲方又改需求', '周一我好困', '加班狗', '带薪拉屎'],
        '可爱猫咪': ['喵喵', '撸我', '主子驾到', '猫粮呢', '摸摸头',
                    '本喵困了', '我不是胖', '别拍了', '铲屎官呢', '小鱼干呢'],
        '干饭人': ['干饭', '好饿', '再来一碗', '我请客', 'AA吧',
                  '吃什么', '好饱', '夜宵走起', '吃饱了才有力气', '减脂中…破防了'],
    }
    phrases = themes.get(theme, themes['打工人'])
    result = []
    for i in range(min(count, len(phrases))):
        result.append({'id': i+1, 'phrase': phrases[i], 'hint': f'一只{theme}说"'+phrases[i]+'"'})
    return {'theme': theme, 'stickers': result}


# ====== 主生成器接口 ======
PRODUCT_CATEGORIES = {
    'prompt_pack': {'name': 'AI Prompt包', 'icon': '🎨', 'generator': 'prompt_pack'},
    'template': {'name': '模板（简历/PPT）', 'icon': '📄', 'generator': 'template'},
    'ebook': {'name': 'AI电子书', 'icon': '📕', 'generator': 'ebook'},
    'sticker': {'name': '表情包素材', 'icon': '😀', 'generator': 'sticker'},
}

PROMPT_STYLE_OPTIONS = list(PROMPT_STYLES.keys())


def auto_generate_product(category='prompt_pack', sub_option=None):
    """自动生成产品"""
    if category == 'prompt_pack':
        style = sub_option or random.choice(PROMPT_STYLE_OPTIONS)
        pack = generate_prompt_pack(style)
        style_cn = style.replace('_', ' ')
        return {
            'name': f'AI绘画Prompt包·{style_cn} 50组',
            'category': 'prompt_pack',
            'price': 9.9,
            'description': f'50组精心调试的AI绘画Prompt，适用于Midjourney/Stable Diffusion，{style_cn}风格',
            'content': f"""✨ 包含内容：
1. {style_cn}风格Prompt 50组
2. 通用负面Prompt大全
3. 人像专用负面Prompt
4. 风景画专用负面Prompt
5. 使用技巧4条

📌 适用工具：Midjourney / Stable Diffusion / 文心一格 / DALL-E
📌 购买后永久使用
📌 支持商业创作授权

🔥 试看（3组）：
{f'{chr(10).join(f"  {i+1}. {p["prompt"]}" for i, p in enumerate(pack["prompts"][:3]))}'}

📋 完整50组Prompt + 负面Prompt + 使用技巧，购买后立即发送百度网盘链接！""",
            'cover_emoji': '🎨',
            'tags': f'AI绘画,Prompt,Midjourney,Stable Diffusion,{style_cn}',
            'platforms': '闲鱼,小红书',
            'generated_data': json.dumps(pack, ensure_ascii=False),
        }
    
    elif category == 'template':
        if sub_option == 'resume' or sub_option is None:
            targets = list(RESUME_CONTENT_TEMPLATES.keys())
            target = random.choice(targets)
            return {
                'name': f'简历模板·{target}专属版 100套',
                'category': 'template',
                'price': 19.9,
                'description': f'100+套{target}简历模板，Word格式，附赠简历电子书',
                'content': generate_resume_template_desc(target),
                'cover_emoji': '📄',
                'tags': f'简历模板,Word模板,求职,{target}简历',
                'platforms': '闲鱼,淘宝',
            }
        else:
            idx = random.randint(0, len(PPT_CATEGORIES)-1)
            name_cn, _ = PPT_CATEGORIES[idx]
            return {
                'name': f'PPT模板·{name_cn} 50套',
                'category': 'template',
                'price': 29.9,
                'description': f'50套{name_cn}PPT模板，专业设计，直接编辑',
                'content': generate_ppt_template_desc(idx),
                'cover_emoji': '📊',
                'tags': f'PPT模板,{name_cn},WPS',
                'platforms': '闲鱼,淘宝',
            }
    
    elif category == 'ebook':
        outline = generate_ebook_outline('AI副业赚钱')
        return {
            'name': 'AI副业赚钱手册·2025实操版',
            'category': 'ebook',
            'price': 39.9,
            'description': '普通人用AI赚钱的10种方法，含具体步骤和真实案例',
            'content': outline,
            'cover_emoji': '📕',
            'tags': 'AI副业,赚钱,电子书,AI教程,副业',
            'platforms': '闲鱼,小红书',
        }
    
    elif category == 'sticker':
        themes = list(generate_emoji_set(1, '打工人').keys()) if False else ['打工人', '可爱猫咪', '干饭人']
        theme = sub_option or random.choice(themes)
        stickers = generate_emoji_set(20, theme)
        return {
            'name': f'AI表情包素材包·{theme} 20张',
            'category': 'sticker',
            'price': 6.6,
            'description': f'20张{theme}主题AI表情包，可直接用于聊天/社交',
            'content': f"""😀 {theme}主题AI表情包 20张

✨ 包含内容：
{f'{chr(10).join(f"  {s["id"]}. {s["phrase"]}" for s in stickers["stickers"])}'}

📌 格式：PNG高清透明背景
📌 用途：微信/QQ/小红书/微博聊天使用
📌 可自由修改添加文字

🔥 低价引流款，搭配其他产品购买更优惠！""",
            'cover_emoji': '😀',
            'tags': f'表情包,{theme},AI绘画,社交素材',
            'platforms': '闲鱼',
            'generated_data': json.dumps(stickers, ensure_ascii=False),
        }
    
    return None


if __name__ == '__main__':
    # 测试
    print("=== Prompt包生成 ===")
    pack = generate_prompt_pack('治愈系_插画', 5)
    for p in pack['prompts']:
        print(f"  {p['id']}. {p['prompt']}")
    
    print("\n=== 自动生成产品 ===")
    product = auto_generate_product('prompt_pack')
    print(f"  名称: {product['name']}")
    print(f"  价格: {product['price']}")
    print(f"  描述: {product['description'][:50]}...")
