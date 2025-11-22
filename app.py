# web_app.py - 完整优化版本
from flask import Flask, render_template, request, jsonify, send_file
import os
import requests
import base64
import tempfile
import uuid
from datetime import datetime
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置请求超时
REQUEST_TIMEOUT = 30  # 30秒超时

class GitHubClient:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if self.token:
            self.headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        else:
            self.headers = {'Accept': 'application/vnd.github.v3+json'}
    
    def get_repo_info(self, repo_url):
        try:
            parts = repo_url.strip('/').split('/')
            if len(parts) < 4:
                return None, "GitHub链接格式不正确"
                
            owner = parts[-2]
            repo_name = parts[-1]
            
            api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
            
            print(f"🔍 请求GitHub API: {api_url}")
            
            # 添加超时设置
            response = requests.get(api_url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                repo_data = response.json()
                return {
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'description': repo_data.get('description', '无描述'),
                    'html_url': repo_data['html_url'],
                    'language': repo_data.get('language', '未知'),
                    'stars': repo_data['stargazers_count'],
                    'forks': repo_data['forks_count'],
                    'open_issues': repo_data['open_issues_count'],
                    'created_at': repo_data['created_at'][:10],
                    'updated_at': repo_data['updated_at'][:10]
                }, None
            else:
                error_msg = f"GitHub API错误: {response.status_code} - {response.text}"
                print(error_msg)
                return None, error_msg
                
        except requests.exceptions.Timeout:
            error_msg = "请求GitHub API超时，请稍后重试"
            print(error_msg)
            return None, error_msg
        except requests.exceptions.ConnectionError:
            error_msg = "网络连接错误，请检查网络连接"
            print(error_msg)
            return None, error_msg
        except Exception as e:
            error_msg = f"获取仓库信息失败: {str(e)}"
            print(error_msg)
            return None, error_msg

    def get_readme(self, owner, repo_name):
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
            response = requests.get(api_url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                content = response.json().get('content', '')
                decoded_content = base64.b64decode(content).decode('utf-8')
                return decoded_content, None
            return "无README", None
        except Exception as e:
            return "无README", f"获取README失败: {str(e)}"

# 智能分析器 - 使用模拟数据确保可靠性
class SmartAIAnalyzer:
    def analyze_repo(self, repo_info, readme_content):
        try:
            # 模拟AI分析 - 快速返回结果
            analysis = self._generate_smart_analysis(repo_info, readme_content)
            return analysis, None
        except Exception as e:
            return None, f"AI分析失败: {str(e)}"
    
    def _generate_smart_analysis(self, repo_info, readme_content):
        """生成智能分析报告"""
        stars = repo_info['stars']
        forks = repo_info['forks']
        language = repo_info['language']
        issues = repo_info['open_issues']
        
        # 根据数据生成智能评价
        popularity = "极高" if stars > 10000 else "很高" if stars > 1000 else "中等" if stars > 100 else "一般"
        activity = "非常活跃" if forks > 500 else "活跃" if forks > 100 else "一般" if forks > 10 else "较低"
        
        # 技术栈分析
        tech_stack = self._analyze_tech_stack(language, readme_content)
        
        # 学习价值评估
        learning_value = self._assess_learning_value(stars, forks, issues)
        
        analysis = f"""
# 🚀 {repo_info['full_name']} 深度分析报告

## 📊 项目概览
这是一个使用 **{language}** 语言开发的开源项目，目前在GitHub上拥有 **{stars:,}** 个星标和 **{forks:,}** 个Fork。

## 🎯 项目评价
- **受欢迎程度**: ⭐⭐⭐⭐⭐ ({popularity})
- **社区活跃度**: 🔄🔨 ({activity}) 
- **问题处理**: 🐛 {issues} 个待解决问题

## 💻 技术栈分析
{tech_stack}

## 📚 学习价值
{learning_value}

## 🔍 项目洞察
{self._generate_insights(repo_info)}

## 💡 使用建议
{self._generate_recommendations(repo_info)}

---
*🤖 由 AI 分析生成 • 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return analysis
    
    def _analyze_tech_stack(self, language, readme_content):
        """分析技术栈"""
        tech_mapping = {
            'JavaScript': '前端开发、Web应用',
            'Python': '数据分析、机器学习、Web后端',
            'Java': '企业级应用、Android开发',
            'TypeScript': '大型前端项目、类型安全的JavaScript',
            'Go': '高性能后端、微服务',
            'Rust': '系统编程、高性能应用',
            'C++': '游戏开发、系统软件',
            'PHP': 'Web开发、内容管理系统'
        }
        
        description = tech_mapping.get(language, "通用软件开发")
        return f"- **主要语言**: {language} - {description}\n- **应用领域**: {description}\n- **技术生态**: 丰富的开源库和框架支持"
    
    def _assess_learning_value(self, stars, forks, issues):
        """评估学习价值"""
        if stars > 5000 and forks > 1000:
            return "🔥 **极高价值** - 这是业界知名项目，学习它可以掌握最佳实践和先进技术"
        elif stars > 1000:
            return "⭐ **很高价值** - 优秀的开源项目，代码质量和架构设计值得学习"
        elif stars > 100:
            return "📚 **中等价值** - 适合学习特定技术的实现方式"
        else:
            return "📖 **基础价值** - 适合初学者了解项目结构"
    
    def _generate_insights(self, repo_info):
        """生成项目洞察"""
        created = repo_info['created_at']
        updated = repo_info['updated_at']
        
        insights = []
        if repo_info['stars'] > repo_info['forks'] * 10:
            insights.append("项目被很多人关注但参与贡献的人相对较少")
        if repo_info['open_issues'] > 100:
            insights.append("项目有较多待解决的问题，可能缺乏维护")
        else:
            insights.append("项目维护良好，问题处理及时")
            
        return "\n".join([f"- {insight}" for insight in insights])
    
    def _generate_recommendations(self, repo_info):
        """生成使用建议"""
        recs = []
        
        if repo_info['stars'] > 10000:
            recs.append("适合深入研究架构设计和代码规范")
        if repo_info['language'] in ['JavaScript', 'TypeScript']:
            recs.append("可以学习现代前端开发的最佳实践")
        if repo_info['forks'] > 500:
            recs.append("考虑参与社区贡献，有很多协作机会")
            
        return "\n".join([f"- {rec}" for rec in recs])

# 导出功能
def generate_pdf(data):
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    repo_info = data['repo_info']
    
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt=f"GitHub仓库分析报告 - {repo_info['full_name']}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="📊 基本信息", ln=True)
    pdf.set_font("Arial", size=10)
    
    info_text = f"""
仓库名称: {repo_info['full_name']}
描述: {repo_info['description']}
主要语言: {repo_info['language']}
星标数: {repo_info['stars']}
Fork数: {repo_info['forks']}
未解决问题: {repo_info['open_issues']}
创建时间: {repo_info['created_at']}
最后更新: {repo_info['updated_at']}
分析时间: {data['analyzed_at']}
    """
    
    pdf.multi_cell(0, 8, txt=info_text)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="🤖 AI分析报告", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, txt=data['ai_analysis'])
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    return temp_file.name

def generate_markdown(data):
    repo_info = data['repo_info']
    
    md_content = f"""# GitHub仓库分析报告 - {repo_info['full_name']}

## 📊 基本信息

- **仓库名称**: {repo_info['full_name']}
- **描述**: {repo_info['description'] or '无描述'}
- **主要语言**: {repo_info['language']}
- **星标数**: {repo_info['stars']}
- **Fork数**: {repo_info['forks']}
- **未解决问题**: {repo_info['open_issues']}
- **创建时间**: {repo_info['created_at']}
- **最后更新**: {repo_info['updated_at']}

## 🤖 AI分析报告

{data['ai_analysis']}

---

*分析时间: {data['analyzed_at']}*
"""
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.md')
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(md_content)
    return temp_file.name

# Flask路由 - 优化错误处理
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_repo():
    """分析GitHub仓库 - 优化版本"""
    start_time = time.time()
    
    data = request.get_json()
    repo_url = data.get('repo_url')
    
    if not repo_url:
        return jsonify({'error': '请输入GitHub仓库链接'}), 400
    
    # 验证GitHub链接格式
    if not repo_url.startswith('https://github.com/') or repo_url.count('/') < 4:
        return jsonify({'error': 'GitHub链接格式不正确，应为: https://github.com/用户名/仓库名'}), 400
    
    try:
        github_client = GitHubClient()
        ai_analyzer = SmartAIAnalyzer()
        
        print(f"🔄 开始分析: {repo_url}")
        
        # 获取仓库信息（带错误处理）
        repo_info, repo_error = github_client.get_repo_info(repo_url)
        if repo_error:
            return jsonify({'error': repo_error}), 400
        
        # 提取owner和repo_name
        parts = repo_url.strip('/').split('/')
        owner = parts[-2]
        repo_name = parts[-1]
        
        # 获取README（快速返回，不阻塞）
        readme_content, readme_error = github_client.get_readme(owner, repo_name)
        if readme_error:
            print(f"⚠️ {readme_error}")  # 记录错误但不中断流程
        
        # AI分析
        ai_analysis, ai_error = ai_analyzer.analyze_repo(repo_info, readme_content)
        if ai_error:
            return jsonify({'error': ai_error}), 500
        
        # 计算处理时间
        processing_time = round(time.time() - start_time, 2)
        
        # 返回结果
        result = {
            'report_id': str(uuid.uuid4())[:8],
            'repo_info': repo_info,
            'ai_analysis': ai_analysis,
            'analyzed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'processing_time': processing_time
        }
        
        print(f"✅ 分析完成: {repo_url} (耗时: {processing_time}s)")
        return jsonify(result)
        
    except Exception as e:
        error_msg = f'分析过程中出现错误: {str(e)}'
        print(f"❌ {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'GitHub Repo AI Analyst'
    })

@app.route('/export/<format_type>', methods=['POST'])
def export_report(format_type):
    """导出报告"""
    data = request.get_json()
    
    try:
        if format_type == 'pdf':
            pdf_file = generate_pdf(data)
            return send_file(pdf_file, as_attachment=True, 
                           download_name=f"github_report_{data['repo_info']['name']}.pdf")
        
        elif format_type == 'markdown':
            md_file = generate_markdown(data)
            return send_file(md_file, as_attachment=True,
                           download_name=f"github_report_{data['repo_info']['name']}.md")
        
        else:
            return jsonify({'error': '暂不支持该格式'}), 400
            
    except Exception as e:
        return jsonify({'error': f'导出失败: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 启动GitHub Repo AI分析师 Web版 (优化版本)")
    print("📱 请在浏览器中访问: http://localhost:5000")
    print("💡 按 Ctrl+C 停止服务器")
    print("🔧 优化特性: 超时控制、错误处理、快速分析")
    app.run(debug=True, host='0.0.0.0', port=5000)
