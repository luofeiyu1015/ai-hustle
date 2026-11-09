# -*- coding: utf-8 -*-
"""AI副业系统 - Flask 主应用"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, send_file
from datetime import datetime
import json
import io
import tarfile

from modules import database as db
from modules import product_engine as pe
from modules import copywriter as cw
from modules import analyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-hustle-2025-secret-key'

# ======== 初始化 ========
db.init_db()


# ======== 部署包下载（PythonAnywhere 一键部署）========
@app.route('/deploy.tar.gz')
def download_deploy():
    """返回完整项目部署包"""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w:gz') as tar:
        tar.add('app.py', arcname='ai_hustle/app.py')
        tar.add('wsgi.py', arcname='ai_hustle/wsgi.py')
        tar.add('requirements.txt', arcname='ai_hustle/requirements.txt')
        for root, dirs, files in os.walk('modules'):
            for f in files:
                tar.add(os.path.join(root, f), arcname=f'ai_hustle/{os.path.join(root, f)}')
        for root, dirs, files in os.walk('templates'):
            for f in files:
                tar.add(os.path.join(root, f), arcname=f'ai_hustle/{os.path.join(root, f)}')
        for root, dirs, files in os.walk('static'):
            for f in files:
                tar.add(os.path.join(root, f), arcname=f'ai_hustle/{os.path.join(root, f)}')
        tar.add('data', arcname='ai_hustle/data')
    buf.seek(0)
    return send_file(buf, mimetype='application/gzip', as_attachment=True, download_name='ai_hustle.tar.gz')

@app.route('/deploy')
def deploy_guide():
    """PythonAnywhere 一键部署说明页"""
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:-apple-system,sans-serif;background:#f4f6f8;padding:20px}pre{background:#1e1e2e;color:#cdd6f4;padding:16px;border-radius:8px;overflow-x:auto;white-space:pre-wrap}code{background:#eee;padding:2px 6px;border-radius:4px}.btn{display:inline-block;background:#4a90e2;color:#fff;padding:12px 24px;text-decoration:none;border-radius:8px;font-weight:bold;margin:8px 0}h1{color:#333}h2{color:#555;margin-top:30px}.step{background:#fff;padding:16px;border-radius:8px;margin:12px 0;box-shadow:0 2px 8px rgba(0,0,0,0.08)}</style></head><body>
<h1>🚀 AI副业系统 - PythonAnywhere 部署指南</h1>
<p style="background:#d4edda;color:#155724;padding:12px;border-radius:8px;margin:12px 0">✅ 用静态文件下载，瞬间完成！</p>
<div class="step"><h2>第1步：下载部署包（点下面这个链接）</h2>
<p><b>直接点这个文件：</b></p>
<p style="font-size:18px;text-align:center;margin:16px 0"><a href="/static/ai_hustle.tar.gz" style="color:#e74c3c;font-weight:bold;font-size:20px">📦 /static/ai_hustle.tar.gz</a></p>
<p style="color:#888">或者在 Safari 地址栏直接输入：</p>
<pre>http://localhost:8000/static/ai_hustle.tar.gz</pre>
<p style="color:#888">如果卡住，等10秒后刷新页面重试</p>
</div>
<div class="step"><h2>第2步：在 PythonAnywhere 上传 + 解压</h2>
<p>仪表板 → <code>浏览文件</code> → <code>上传</code> → 选刚才下载的文件</p>
<p>然后点 <code>$ Bash</code> → 复制粘贴：</p>
<pre>mkdir -p ~/ai_hustle
mv ~/ai_hustle.tar.gz ~/deploy.tar.gz 2>/dev/null
tar xzf ~/deploy.tar.gz -C ~/ai_hustle --strip-components=1
pip install flask -q
echo "✅ 部署成功！"</pre>
</div>
<div class="step"><h2>第3步：配置 Web App（公网访问）</h2>
<p>仪表板 → <code>Web</code> → <code>Add new web app</code> → <code>Flask</code> → <code>Manual configuration</code></p>
<p>Source code 填：</p>
<pre>/home/13307878293/ai_hustle</pre>
<p>然后 <code>Edit</code> WSGI 文件，清空后粘贴：</p>
<pre>import sys, os
sys.path.insert(0, '/home/13307878293/ai_hustle')
from wsgi import application</pre>
<p>保存 → 绿色 <code>Reload</code> → 搞定！🎊</p>
</div>
</body></html>'''


# ======== 首页仪表盘 ========
@app.route('/')
def index():
    stats = db.get_product_stats()
    summary = db.get_transaction_summary()
    products = db.get_all_products('active')[:6]
    lessons = db.get_lessons()[:3]
    today_tasks = analyzer.get_daily_tasks()
    reports = db.get_reports()[:3]
    
    # 今日报告
    today_report = None
    if reports and reports[0]['report_date'] == datetime.now().strftime('%Y-%m-%d'):
        today_report = reports[0]
    
    return render_template('index.html',
                         stats=stats, summary=summary,
                         products=products, lessons=lessons,
                         tasks=today_tasks, reports=reports,
                         today_report=today_report,
                         current_page='home')


# ======== 产品管理 ========
@app.route('/products')
def products_list():
    status = request.args.get('status', None)
    products = db.get_all_products(status)
    return render_template('products.html', products=products, 
                         status_filter=status, current_page='products')

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = db.get_product(pid)
    if not product:
        abort(404)
    copies = db.get_copies(pid)
    return render_template('product_detail.html', product=product, 
                         copies=copies, current_page='products')

@app.route('/product/new', methods=['GET', 'POST'])
def product_new():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', ''),
            'category': request.form.get('category', 'prompt_pack'),
            'price': float(request.form.get('price', 9.9) or 9.9),
            'description': request.form.get('description', ''),
            'content': request.form.get('content', ''),
            'cover_emoji': request.form.get('cover_emoji', '📦'),
            'tags': request.form.get('tags', ''),
            'platforms': request.form.get('platforms', '闲鱼,小红书'),
            'status': request.form.get('status', 'active'),
        }
        pid = db.save_product(data)
        return redirect(url_for('product_detail', pid=pid))
    
    return render_template('product_form.html', product=None, 
                         product_categories=pe.PRODUCT_CATEGORIES,
                         prompt_styles=pe.PROMPT_STYLE_OPTIONS,
                         current_page='products')

@app.route('/product/<int:pid>/edit', methods=['GET', 'POST'])
def product_edit(pid):
    product = db.get_product(pid)
    if not product:
        abort(404)
    
    if request.method == 'POST':
        data = {
            'id': pid,
            'name': request.form.get('name', ''),
            'category': request.form.get('category', 'prompt_pack'),
            'price': float(request.form.get('price', 9.9) or 9.9),
            'description': request.form.get('description', ''),
            'content': request.form.get('content', ''),
            'cover_emoji': request.form.get('cover_emoji', '📦'),
            'tags': request.form.get('tags', ''),
            'platforms': request.form.get('platforms', '闲鱼,小红书'),
            'status': request.form.get('status', 'active'),
        }
        db.save_product(data)
        return redirect(url_for('product_detail', pid=pid))
    
    return render_template('product_form.html', product=product,
                         product_categories=pe.PRODUCT_CATEGORIES,
                         prompt_styles=pe.PROMPT_STYLE_OPTIONS,
                         current_page='products')

@app.route('/product/<int:pid>/delete', methods=['POST'])
def product_delete(pid):
    db.delete_product(pid)
    return redirect(url_for('products_list'))

# ======== 自动生成产品 ========
@app.route('/api/generate_product', methods=['POST'])
def api_generate_product():
    data = request.get_json()
    category = data.get('category', 'prompt_pack')
    sub_option = data.get('sub_option')
    
    product = pe.auto_generate_product(category, sub_option)
    if product:
        # 自动创建为草稿
        pid = db.save_product(product)
        product['id'] = pid
        return jsonify({'success': True, 'product': product})
    return jsonify({'success': False, 'error': '生成失败'})

@app.route('/product/generate', methods=['GET', 'POST'])
def product_generate():
    if request.method == 'POST':
        category = request.form.get('category', 'prompt_pack')
        sub_option = request.form.get('sub_option')
        product = pe.auto_generate_product(category, sub_option)
        if product:
            pid = db.save_product(product)
            return redirect(url_for('product_detail', pid=pid))
    
    return render_template('product_generate.html',
                         product_categories=pe.PRODUCT_CATEGORIES,
                         prompt_styles=pe.PROMPT_STYLE_OPTIONS,
                         current_page='products')


# ======== 文案管理 ========
@app.route('/copies')
def copies_list():
    copies = db.get_copies()
    return render_template('copies.html', copies=copies, current_page='copies')

@app.route('/api/generate_copies/<int:pid>', methods=['POST'])
def api_generate_copies(pid):
    product = db.get_product(pid)
    if not product:
        return jsonify({'success': False, 'error': '产品不存在'}), 404
    
    copies = cw.generate_all_copies(product)
    for cp in copies:
        cp['product_id'] = pid
        db.save_copy(cp)
    
    return jsonify({'success': True, 'copies': copies})

@app.route('/copy/<int:cid>/delete', methods=['POST'])
def copy_delete(cid):
    db.delete_copy(cid)
    return redirect(url_for('copies_list'))


# ======== 财务账本 ========
@app.route('/finance')
def finance():
    transactions = db.get_transactions(30)
    summary = db.get_transaction_summary()
    products = db.get_all_products('active')
    predictions = analyzer.predict_revenue(30)
    return render_template('finance.html', transactions=transactions, 
                         summary=summary, products=products,
                         predictions=predictions, current_page='finance')

@app.route('/finance/add', methods=['POST'])
def finance_add():
    data = {
        'type': request.form.get('type', 'income'),
        'amount': float(request.form.get('amount', 0) or 0),
        'category': request.form.get('category', ''),
        'description': request.form.get('description', ''),
        'product_id': request.form.get('product_id') or None,
        'platform': request.form.get('platform', ''),
        'trans_date': request.form.get('trans_date') or datetime.now().isoformat(),
    }
    db.add_transaction(data)
    return redirect(url_for('finance'))

@app.route('/finance/delete/<int:tid>', methods=['POST'])
def finance_delete(tid):
    db.delete_transaction(tid)
    return redirect(url_for('finance'))


# ======== 市场分析 ========
@app.route('/market')
def market():
    keyword = request.args.get('keyword', '')
    opportunities = analyzer.analyze_market(keyword)
    pricing = analyzer.get_pricing_strategy()
    platforms = analyzer.PLATFORM_STRATEGIES
    return render_template('market.html', opportunities=opportunities,
                         pricing=pricing, platforms=platforms,
                         keyword=keyword, current_page='market')


# ======== 报告 ========
@app.route('/reports')
def reports():
    reports_list = db.get_reports()
    summary = db.get_transaction_summary()
    return render_template('reports.html', reports=reports_list,
                         summary=summary, current_page='reports')

@app.route('/api/generate_report', methods=['POST'])
def api_generate_report():
    report = analyzer.generate_daily_report()
    return jsonify({'success': True, 'report': report})

@app.route('/daily_report')
def daily_report():
    # 自动生成今日报告
    report = analyzer.generate_daily_report()
    text = analyzer.format_report_text(report)
    return render_template('daily_report.html', report=report, text=text,
                         current_page='reports')


# ======== 学习中心 ========
@app.route('/lessons')
def lessons_list():
    lessons = db.get_lessons()
    return render_template('lessons.html', lessons=lessons, current_page='lessons')

@app.route('/lessons/add', methods=['POST'])
def lessons_add():
    data = {
        'title': request.form.get('title', ''),
        'content': request.form.get('content', ''),
        'category': request.form.get('category', ''),
        'action': request.form.get('action', ''),
    }
    db.add_lesson(data)
    return redirect(url_for('lessons_list'))

@app.route('/lessons/delete/<int:lid>', methods=['POST'])
def lessons_delete(lid):
    db.delete_lesson(lid)
    return redirect(url_for('lessons_list'))


# ======== 工具：一键复制 ========
@app.route('/api/copy_text', methods=['POST'])
def api_copy_text():
    text = request.form.get('text', '')
    return jsonify({'success': True, 'text': text})


# ======== 错误处理 ========
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', code=404, message='页面没找到', current_page=''), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', code=500, message='服务器出问题了', current_page=''), 500


# ======== 启动 ========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"""
╔══════════════════════════════════════════════════╗
║       🚀 AI 副业系统已启动                        ║
║       访问地址: http://localhost:{port}            ║
║                                                    ║
║       功能模块：                                   ║
║       📦 产品自动生成 & 管理                       ║
║       ✍️ 文案自动生成                              ║
║       📊 市场分析                                  ║
║       💰 财务账本                                  ║
║       📈 每日报告                                  ║
║       📚 学习中心                                  ║
╚══════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=port, debug=False)
