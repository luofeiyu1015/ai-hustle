#!/bin/bash
# AI副业系统守护脚本 - 服务挂了自动重启 + 依赖自动安装
cd /workspace/ai_hustle
LOG=/tmp/flask_supervisor.log
PYTHON=/root/.pyenv/shims/python3

echo "[$(date)] 守护脚本启动" >> $LOG

while true; do
    # 检查 Flask 是否在监听 8000 端口
    if ! /usr/bin/curl -s -o /dev/null http://127.0.0.1:8000/ 2>/dev/null; then
        echo "[$(date)] 服务挂了，重新启动..." >> $LOG
        # 清理残留进程
        pkill -9 -f "python3.*app.py" 2>/dev/null
        sleep 1
        # --- 关键加固：每次启动前确保依赖存在 ---
        if ! $PYTHON -c "import flask" 2>/dev/null; then
            echo "[$(date)] 依赖缺失，安装 flask gunicorn requests..." >> $LOG
            $PYTHON -m pip install flask gunicorn requests --quiet 2>&1 >> $LOG
        fi
        # 启动
        nohup $PYTHON -u app.py > /tmp/flask.log 2>&1 &
        disown
        sleep 4
        if /usr/bin/curl -s -o /dev/null http://127.0.0.1:8000/ 2>/dev/null; then
            echo "[$(date)] ✅ 服务启动成功" >> $LOG
        else
            echo "[$(date)] ❌ 启动失败，检查日志" >> $LOG
            /usr/bin/tail -5 /tmp/flask.log >> $LOG
        fi
    fi
    sleep 5
done
