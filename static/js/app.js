// AI副业助手 - 前端交互脚本

// Toast 提示
function showToast(message, duration = 2000) {
    // 移除已有的toast
    var existing = document.querySelector('.toast');
    if (existing) existing.remove();
    
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(function() { toast.remove(); }, 300);
    }, duration);
}

// 复制文本
function copyText(btn, text) {
    if (!text) {
        showToast('没有可复制的内容');
        return;
    }
    
    // 尝试使用 Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('✅ 已复制到剪贴板');
            if (btn && btn.textContent.indexOf('已复制') === -1) {
                var originalText = btn.textContent;
                btn.textContent = '✅ 已复制';
                setTimeout(function() { btn.textContent = originalText; }, 1500);
            }
        }).catch(function() {
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

// 降级复制方法
function fallbackCopy(text) {
    try {
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('✅ 已复制到剪贴板');
    } catch (e) {
        showToast('❌ 复制失败，请手动选择复制');
    }
}

// 表单确认
document.addEventListener('submit', function(e) {
    var form = e.target;
    if (form.dataset.confirm && !confirm(form.dataset.confirm)) {
        e.preventDefault();
    }
});

// 数字输入格式化
document.addEventListener('input', function(e) {
    if (e.target.type === 'number' && e.target.value < 0) {
        e.target.value = 0;
    }
});

// 防止双击按钮
document.addEventListener('click', function(e) {
    var btn = e.target.closest('.btn-block, button[type="submit"]');
    if (btn && !btn.disabled) {
        btn.addEventListener('click', function() {
            btn.disabled = true;
            setTimeout(function() { btn.disabled = false; }, 1500);
        }, { once: true });
    }
});

// 图片懒加载（预留）
document.addEventListener('DOMContentLoaded', function() {
    // 自动保存表单到 localStorage 作为草稿
    var forms = document.querySelectorAll('form[data-autosave]');
    forms.forEach(function(form) {
        var key = 'ai_hustle_draft_' + (form.id || form.action);
        var saved = localStorage.getItem(key);
        if (saved) {
            try {
                var data = JSON.parse(saved);
                Object.keys(data).forEach(function(name) {
                    var input = form.querySelector('[name="' + name + '"]');
                    if (input && !input.value) {
                        input.value = data[name];
                    }
                });
            } catch(e) {}
        }
        
        form.addEventListener('input', function() {
            var data = {};
            form.querySelectorAll('input, textarea, select').forEach(function(input) {
                if (input.name && input.type !== 'hidden') {
                    data[input.name] = input.value;
                }
            });
            localStorage.setItem(key, JSON.stringify(data));
        });
        
        form.addEventListener('submit', function() {
            localStorage.removeItem(key);
        });
    });
});

// 快捷返回顶部
var scrollTimer;
window.addEventListener('scroll', function() {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function() {
        var existing = document.getElementById('backToTop');
        if (window.scrollY > 300) {
            if (!existing) {
                var btn = document.createElement('button');
                btn.id = 'backToTop';
                btn.innerHTML = '↑';
                btn.style.cssText = 'position:fixed;bottom:90px;right:20px;width:44px;height:44px;border-radius:50%;background:var(--primary);color:white;font-size:20px;box-shadow:var(--shadow-lg);z-index:150;border:none;transition:all 0.2s;';
                btn.onclick = function() { window.scrollTo({top:0, behavior:'smooth'}); };
                document.body.appendChild(btn);
            }
        } else if (existing) {
            existing.remove();
        }
    }, 100);
});
