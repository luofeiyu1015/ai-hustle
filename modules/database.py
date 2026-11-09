# -*- coding: utf-8 -*-
"""数据库管理模块 - SQLite"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ai_hustle.db')

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    
    # 产品表
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL DEFAULT 9.9,
        description TEXT,
        content TEXT,
        cover_emoji TEXT DEFAULT '📦',
        tags TEXT,
        platforms TEXT,
        status TEXT DEFAULT 'draft',
        sales_count INTEGER DEFAULT 0,
        revenue REAL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 文案表
    c.execute('''CREATE TABLE IF NOT EXISTS copies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        title TEXT,
        body TEXT,
        tags TEXT,
        platform TEXT,
        type TEXT DEFAULT 'listing',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )''')
    
    # 收支记录表
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        description TEXT,
        product_id INTEGER,
        platform TEXT,
        trans_date TEXT DEFAULT CURRENT_TIMESTAMP,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 失败经验表
    c.execute('''CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        category TEXT,
        action TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 市场分析表
    c.execute('''CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        platform TEXT,
        hot_score INTEGER,
        competition INTEGER,
        avg_price REAL,
        suggestion TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 每日报告表
    c.execute('''CREATE TABLE IF NOT EXISTS daily_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date TEXT NOT NULL,
        revenue REAL DEFAULT 0,
        cost REAL DEFAULT 0,
        net_profit REAL DEFAULT 0,
        sales_count INTEGER DEFAULT 0,
        top_product TEXT,
        lessons_learned TEXT,
        tomorrow_plan TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(report_date)
    )''')
    
    conn.commit()
    
    # 插入初始数据
    _seed_initial_data(c)
    conn.commit()
    conn.close()

def _seed_initial_data(c):
    """插入初始种子数据"""
    # 检查是否已有产品
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        now = datetime.now().isoformat()
        # 预置几款初始产品模板
        products = [
            ('AI绘画Prompt包·治愈系插画50组', 'prompt_pack', 9.9, 
             '50组精心调试的治愈系AI绘画Prompt，适用于Midjourney/Stable Diffusion，包含风格、光线、构图完整描述',
             '✨ 包含内容：\n1. 治愈系插画风格Prompt 20组\n2. 动漫风格Prompt 15组\n3. 水彩风格Prompt 10组\n4. 附赠负面Prompt大全\n\n📌 适用于：Midjourney / Stable Diffusion / 文心一格\n📌 购买后可永久使用\n📌 支持二次创作商业授权',
             '🎨', 'AI绘画,Prompt,Midjourney,Stable Diffusion,治愈系,插画',
             '闲鱼,小红书', 'active', 0, 0, now, now),
            ('AI头像Prompt包·高级感头像30组', 'prompt_pack', 12.9,
             '30组AI头像Prompt，从写实到动漫，一键生成高级感个人头像',
             '✨ 包含内容：\n1. 写实人像Prompt 10组\n2. 动漫头像Prompt 10组\n3. 3D卡通头像Prompt 10组\n4. 附赠高清放大技巧\n\n📌 适用于：Midjourney / Stable Diffusion / DALL-E\n📌 可用于个人社交账号',
             '👤', 'AI头像,Prompt,头像制作,Midjourney',
             '闲鱼,小红书', 'active', 0, 0, now, now),
            ('简历模板·高端商务风2025版', 'template', 19.9,
             '100+套2025年最新简历模板，Word格式可编辑，含求职技巧电子书',
             '✨ 包含内容：\n1. 简约风简历模板 30套\n2. 高端商务风简历模板 30套\n3. 创意设计风简历模板 20套\n4. 应届生专属模板 20套\n5. 《简历撰写黄金法则》电子书\n\n📌 格式：Word / WPS 可直接编辑\n📌 购买后永久免费更新',
             '📄', '简历模板,Word模板,求职,简历制作',
             '闲鱼,淘宝', 'active', 0, 0, now, now),
            ('PPT模板合集·创业融资专用', 'template', 29.9,
             '50套商业PPT模板，覆盖创业融资、产品发布、年度总结等场景',
             '✨ 包含内容：\n1. 创业融资BP模板 15套\n2. 产品发布会模板 10套\n3. 年度总结模板 15套\n4. 通用商务模板 10套\n\n📌 格式：PPT/WPS 可直接编辑\n📌 含使用教程视频',
             '📊', 'PPT模板,创业,融资,商业计划书',
             '闲鱼,淘宝', 'active', 0, 0, now, now),
            ('AI副业赚钱手册·2025版', 'ebook', 39.9,
             '全面介绍2025年普通人用AI赚钱的10种实操方法，含具体步骤和工具',
             '✨ 包含内容：\n10个AI副业方向深度拆解：\n1. AI数字产品销售\n2. AI自媒体带货\n3. AI接单服务\n4. AI课程制作\n5. AI社群运营\n...等等\n\n每个方向都有：\n✅ 具体操作步骤\n✅ 推荐工具清单\n✅ 避坑指南\n✅ 真实案例分析',
             '📕', 'AI副业,赚钱,电子书,AI教程',
             '闲鱼,小红书', 'active', 0, 0, now, now),
        ]
        c.executemany('''INSERT INTO products (name, category, price, description, content, cover_emoji, tags, platforms, status, sales_count, revenue, created_at, updated_at)
                      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', products)
    
    # 检查市场数据
    c.execute("SELECT COUNT(*) FROM market_data")
    if c.fetchone()[0] == 0:
        market_data = [
            ('AI Prompt', '闲鱼', 95, 7, 9.9, '市场热度极高，竞争中等，建议做细分领域'),
            ('AI头像', '小红书', 90, 6, 12.9, '女生用户多，客单价可做高，建议加滤镜/风格细分'),
            ('简历模板', '闲鱼', 85, 5, 19.9, '求职季特别火，可做应届生/职场人细分'),
            ('PPT模板', '淘宝', 80, 8, 29.9, '竞争较大但需求稳定，建议做垂直领域'),
            ('AI电子书', '小红书', 88, 4, 39.9, '蓝海市场，可做AI赚钱/AI工具主题'),
            ('表情包素材', '闲鱼', 75, 3, 6.6, '超低价引流，可搭配其他产品打包'),
            ('AI绘画教程', '小红书', 92, 5, 49.9, '付费意愿强，可做录播课+社群'),
            ('公众号排版模板', '闲鱼', 70, 4, 15.9, '公众号作者刚需，可做行业细分'),
        ]
        c.executemany('''INSERT INTO market_data (keyword, platform, hot_score, competition, avg_price, suggestion)
                      VALUES (?,?,?,?,?,?)''', market_data)
    
    # 检查失败经验
    c.execute("SELECT COUNT(*) FROM lessons")
    if c.fetchone()[0] == 0:
        lessons = [
            ('不要什么都卖', '同时上架太多品类会让店铺显得杂乱，降低信任感', '选品', '聚焦1-2个垂直领域深耕'),
            ('低价引流但要有利润款', '只卖低价品赚不到钱，需要高中低价位组合', '定价', '引流款9.9 + 利润款39.9 + 形象款99'),
            ('要做差异化', '直接搬运别人的产品卖不动，要加自己的价值', '产品', '原始产品+额外赠品+使用教程'),
            ('及时回复客户', '闲鱼消息超过1小时不回，客户就跑了', '服务', '开启消息推送，设定15分钟内回复'),
            ('坚持上架新品', '每周至少上1-2个新品，增加曝光机会', '运营', '固定每周三上新'),
        ]
        c.executemany('''INSERT INTO lessons (title, content, category, action) VALUES (?,?,?,?)''', lessons)

# ====== 查询函数 ======
def get_all_products(status=None):
    conn = get_conn()
    if status:
        rows = conn.execute("SELECT * FROM products WHERE status=? ORDER BY id DESC", (status,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_product(pid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def save_product(data):
    conn = get_conn()
    now = datetime.now().isoformat()
    if data.get('id'):
        conn.execute('''UPDATE products SET name=?, category=?, price=?, description=?, content=?, cover_emoji=?, tags=?, platforms=?, status=?, updated_at=? WHERE id=?''',
                    (data.get('name',''), data.get('category',''), data.get('price',9.9), 
                     data.get('description',''), data.get('content',''), data.get('cover_emoji','📦'),
                     data.get('tags',''), data.get('platforms',''), data.get('status','active'), now, data['id']))
        pid = data['id']
    else:
        cur = conn.execute('''INSERT INTO products (name, category, price, description, content, cover_emoji, tags, platforms, status, created_at, updated_at)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                          (data.get('name',''), data.get('category',''), data.get('price',9.9),
                           data.get('description',''), data.get('content',''), data.get('cover_emoji','📦'),
                           data.get('tags',''), data.get('platforms',''), data.get('status','active'), now, now))
        pid = cur.lastrowid
    conn.commit()
    conn.close()
    return pid

def delete_product(pid):
    conn = get_conn()
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.execute("DELETE FROM copies WHERE product_id=?", (pid,))
    conn.commit()
    conn.close()

def get_copies(product_id=None):
    conn = get_conn()
    if product_id:
        rows = conn.execute("SELECT * FROM copies WHERE product_id=? ORDER BY id DESC", (product_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM copies ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_copy(data):
    conn = get_conn()
    conn.execute('''INSERT INTO copies (product_id, title, body, tags, platform, type)
                  VALUES (?,?,?,?,?,?)''',
                (data.get('product_id'), data.get('title',''), data.get('body',''),
                 data.get('tags',''), data.get('platform','闲鱼'), data.get('type','listing')))
    conn.commit()
    conn.close()

def delete_copy(cid):
    conn = get_conn()
    conn.execute("DELETE FROM copies WHERE id=?", (cid,))
    conn.commit()
    conn.close()

def get_transactions(days=30):
    conn = get_conn()
    rows = conn.execute('''SELECT * FROM transactions WHERE date(trans_date) >= date('now', ?) 
                          ORDER BY trans_date DESC''', (f'-{days} days',)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_transaction_summary():
    conn = get_conn()
    row = conn.execute('''SELECT 
        COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as total_income,
        COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as total_cost,
        COALESCE(COUNT(CASE WHEN type='income' THEN 1 END), 0) as sales_count
        FROM transactions''').fetchone()
    conn.close()
    d = dict(row) if row else {}
    d['net_profit'] = (d.get('total_income') or 0) - (d.get('total_cost') or 0)
    return d

def add_transaction(data):
    conn = get_conn()
    conn.execute('''INSERT INTO transactions (type, amount, category, description, product_id, platform, trans_date)
                  VALUES (?,?,?,?,?,?,?)''',
                (data.get('type','income'), data.get('amount',0), data.get('category',''),
                 data.get('description',''), data.get('product_id'), data.get('platform',''),
                 data.get('trans_date') or datetime.now().isoformat()))
    # 同步更新产品销量和收入
    if data.get('type') == 'income' and data.get('product_id'):
        conn.execute('''UPDATE products SET sales_count = sales_count + 1, revenue = revenue + ?, 
                       updated_at=? WHERE id=?''',
                    (data.get('amount',0), datetime.now().isoformat(), data['product_id']))
    conn.commit()
    conn.close()

def delete_transaction(tid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM transactions WHERE id=?", (tid,)).fetchone()
    if row and row['type'] == 'income' and row['product_id']:
        conn.execute('''UPDATE products SET sales_count = sales_count - 1, revenue = revenue - ? WHERE id=?''',
                    (row['amount'], row['product_id']))
    conn.execute("DELETE FROM transactions WHERE id=?", (tid,))
    conn.commit()
    conn.close()

def get_lessons():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM lessons ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_lesson(data):
    conn = get_conn()
    conn.execute('''INSERT INTO lessons (title, content, category, action) VALUES (?,?,?,?)''',
                (data.get('title',''), data.get('content',''), data.get('category',''), data.get('action','')))
    conn.commit()
    conn.close()

def delete_lesson(lid):
    conn = get_conn()
    conn.execute("DELETE FROM lessons WHERE id=?", (lid,))
    conn.commit()
    conn.close()

def get_market_data(keyword=None):
    conn = get_conn()
    if keyword:
        rows = conn.execute("SELECT * FROM market_data WHERE keyword LIKE ?", (f'%{keyword}%',)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM market_data ORDER BY hot_score DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_market_data(data):
    conn = get_conn()
    conn.execute('''INSERT INTO market_data (keyword, platform, hot_score, competition, avg_price, suggestion)
                  VALUES (?,?,?,?,?,?)''',
                (data.get('keyword',''), data.get('platform',''), data.get('hot_score',50),
                 data.get('competition',5), data.get('avg_price',9.9), data.get('suggestion','')))
    conn.commit()
    conn.close()

def get_reports():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM daily_reports ORDER BY report_date DESC LIMIT 30").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_report(data):
    conn = get_conn()
    conn.execute('''INSERT OR REPLACE INTO daily_reports 
                  (report_date, revenue, cost, net_profit, sales_count, top_product, lessons_learned, tomorrow_plan)
                  VALUES (?,?,?,?,?,?,?,?)''',
                (data.get('report_date',''), data.get('revenue',0), data.get('cost',0),
                 data.get('net_profit',0), data.get('sales_count',0), data.get('top_product',''),
                 data.get('lessons_learned',''), data.get('tomorrow_plan','')))
    conn.commit()
    conn.close()

# 产品统计
def get_product_stats():
    conn = get_conn()
    row = conn.execute('''SELECT 
        COUNT(*) as total,
        COUNT(CASE WHEN status='active' THEN 1 END) as active,
        COALESCE(SUM(sales_count),0) as total_sales,
        COALESCE(SUM(revenue),0) as total_revenue
        FROM products''').fetchone()
    conn.close()
    return dict(row) if row else {}

if __name__ == '__main__':
    init_db()
    print("数据库初始化成功！")
    print(f"产品数: {len(get_all_products())}")
    print(f"市场数据: {len(get_market_data())}")
    print(f"失败经验: {len(get_lessons())}")
