// static/js/script.js - 完整优化版本
console.log("✅ script.js 文件已加载！");

document.addEventListener('DOMContentLoaded', function() {
    console.log("🚀 DOM 加载完成，开始初始化...");
    
    const repoUrlInput = document.getElementById('repoUrl');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const loadingStatus = document.getElementById('loadingStatus');

    console.log("📝 找到页面元素:", {
        repoUrlInput: !!repoUrlInput,
        analyzeBtn: !!analyzeBtn,
        loadingDiv: !!loadingDiv,
        resultDiv: !!resultDiv,
        loadingStatus: !!loadingStatus
    });

    // 超时设置（30秒）
    const REQUEST_TIMEOUT = 30000;
    let currentRequestController = null;

    // 输入动画
    if (repoUrlInput) {
        repoUrlInput.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });

        repoUrlInput.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    }

    // 绑定分析按钮事件
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeRepository);
        console.log("✅ 分析按钮事件绑定成功");
    } else {
        console.error("❌ 找不到分析按钮");
    }

    // 回车键支持
    if (repoUrlInput) {
        repoUrlInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') analyzeRepository();
        });
    }

    async function analyzeRepository() {
        console.log("🔄 开始分析流程...");
        
        const repoUrl = repoUrlInput ? repoUrlInput.value.trim() : '';
        
        console.log("📋 输入的URL:", repoUrl);
        
        if (!repoUrl) {
            showNotification('请输入GitHub仓库链接', 'error');
            return;
        }

        if (!repoUrl.startsWith('https://github.com/') || repoUrl.split('/').length < 5) {
            showNotification('GitHub链接格式不正确，应为: https://github.com/用户名/仓库名', 'error');
            return;
        }

        // 取消之前的请求（如果存在）
        if (currentRequestController) {
            currentRequestController.abort();
        }

        // 创建新的AbortController用于超时控制
        currentRequestController = new AbortController();
        const timeoutId = setTimeout(() => {
            if (currentRequestController) {
                currentRequestController.abort();
            }
        }, REQUEST_TIMEOUT);

        // 显示加载动画
        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 分析中...';
        }
        
        if (loadingDiv) {
            loadingDiv.classList.remove('hidden');
        }
        
        if (resultDiv) {
            resultDiv.classList.add('hidden');
        }

        // 更新加载状态信息
        updateLoadingStatus('正在连接GitHub API...');

        try {
            console.log("📡 发送请求到服务器:", repoUrl);
            
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ repo_url: repoUrl }),
                signal: currentRequestController.signal
            });

            clearTimeout(timeoutId);

            console.log("📨 服务器响应状态:", response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `服务器错误: ${response.status}`);
            }

            const data = await response.json();
            console.log("✅ 收到服务器响应数据");

            // 显示结果
            displayResult(data);
            showNotification(`分析完成！耗时 ${data.processing_time || '未知'} 秒`, 'success');
            
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                console.log("⏰ 请求超时");
                showNotification('请求超时，请检查网络连接或稍后重试', 'error');
            } else {
                console.error('分析错误:', error);
                showNotification('分析失败: ' + error.message, 'error');
            }
        } finally {
            if (analyzeBtn) {
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = '<i class="fas fa-search"></i> 开始智能分析';
            }
            
            if (loadingDiv) {
                loadingDiv.classList.add('hidden');
            }
            
            currentRequestController = null;
        }
    }

    function updateLoadingStatus(message) {
        console.log("📊 更新加载状态:", message);
        if (loadingStatus) {
            loadingStatus.textContent = message;
        }
    }

    function displayResult(data) {
        console.log("🎨 开始显示分析结果");
        
        const { repo_info, ai_analysis, analyzed_at, processing_time } = data;
        
        const resultHTML = `
            <div class="repo-header">
                <h2>
                    <i class="fas fa-cube"></i>
                    ${repo_info.full_name}
                </h2>
                <p class="repo-description">${repo_info.description || '这个项目没有描述信息'}</p>
                
                <div class="repo-stats">
                    <div class="stat-item">
                        <span class="stat-number">${repo_info.stars.toLocaleString()}</span>
                        <span class="stat-label">
                            <i class="fas fa-star"></i>
                            星标
                        </span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${repo_info.forks.toLocaleString()}</span>
                        <span class="stat-label">
                            <i class="fas fa-code-branch"></i>
                            Fork
                        </span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${repo_info.open_issues.toLocaleString()}</span>
                        <span class="stat-label">
                            <i class="fas fa-bug"></i>
                            问题
                        </span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${repo_info.language}</span>
                        <span class="stat-label">
                            <i class="fas fa-code"></i>
                            语言
                        </span>
                    </div>
                </div>
                
                <div class="repo-meta">
                    <span><i class="fas fa-calendar-plus"></i> 创建: ${repo_info.created_at}</span>
                    <span><i class="fas fa-sync-alt"></i> 更新: ${repo_info.updated_at}</span>
                    <span><i class="fas fa-clock"></i> 分析: ${analyzed_at}</span>
                    ${processing_time ? `<span><i class="fas fa-rocket"></i> 耗时: ${processing_time}s</span>` : ''}
                </div>
            </div>

            <div class="analysis-section">
                <h3>
                    <i class="fas fa-robot"></i>
                    AI深度分析报告
                </h3>
                <div class="analysis-content">${ai_analysis}</div>
            </div>

            <div class="export-buttons">
                <button class="export-btn btn-pdf" onclick="exportReport('pdf')">
                    <i class="fas fa-file-pdf"></i>
                    导出PDF报告
                </button>
                <button class="export-btn btn-word" onclick="exportReport('word')">
                    <i class="fas fa-file-word"></i>
                    导出Word文档
                </button>
                <button class="export-btn btn-md" onclick="exportReport('markdown')">
                    <i class="fas fa-file-code"></i>
                    导出Markdown
                </button>
            </div>
        `;

        if (resultDiv) {
            resultDiv.innerHTML = resultHTML;
            resultDiv.classList.remove('hidden');
        }
        
        // 保存数据供导出使用
        window.currentReportData = data;
        
        // 平滑滚动到结果
        if (resultDiv) {
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        console.log("✅ 分析结果显示完成");
    }

    // 通知函数
    function showNotification(message, type = 'info') {
        console.log("🔔 显示通知:", message, type);
        
        // 移除现有通知
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        });

        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            ${message}
        `;
        
        // 添加样式
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
            max-width: 400px;
            font-weight: 500;
        `;
        
        document.body.appendChild(notification);
        
        // 自动移除
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in forwards';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    // 导出功能
    window.exportReport = async function(format) {
        console.log("📤 导出报告:", format);
        
        if (!window.currentReportData) {
            showNotification('没有可导出的数据', 'error');
            return;
        }

        try {
            showNotification(`正在生成${format.toUpperCase()}报告...`, 'info');
            
            const response = await fetch(`/export/${format}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(window.currentReportData)
            });

            if (!response.ok) {
                throw new Error('导出失败');
            }

            // 创建下载
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `github_analysis_${window.currentReportData.repo_info.name}.${format === 'word' ? 'docx' : format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('导出成功！', 'success');
            
        } catch (error) {
            console.error('导出错误:', error);
            showNotification('导出失败: ' + error.message, 'error');
        }
    };

    // 添加取消分析功能
    window.cancelAnalysis = function() {
        console.log("❌ 取消分析");
        
        if (currentRequestController) {
            currentRequestController.abort();
            showNotification('已取消分析', 'info');
        }
    };

    console.log("🎉 所有事件监听器绑定完成！");
});

// 添加全局错误处理
window.addEventListener('error', function(e) {
    console.error('🚨 全局错误:', e.error);
    console.error('🚨 错误位置:', e.filename, e.lineno, e.colno);
});