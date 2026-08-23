"""飞书文档集成客户端"""
import requests
import json
from utils import config

class FeishuClient:
    """飞书API客户端"""
    
    def __init__(self):
        self.app_id = config.feishu_app_id
        self.app_secret = config.feishu_app_secret
        self.doc_token = config.feishu_doc_token
        self.tenant_access_token = None
    
    def _get_tenant_access_token(self):
        """获取tenant_access_token"""
        if not self.app_id or not self.app_secret:
            print("飞书配置不完整，请在.env文件中配置FEISHU_APP_ID和FEISHU_APP_SECRET")
            return None
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get('code') == 0:
                self.tenant_access_token = result.get('tenant_access_token')
                return self.tenant_access_token
            else:
                print(f"获取token失败: {result.get('msg')}")
                return None
        except Exception as e:
            print(f"获取token异常: {e}")
            return None
    
    def read_document(self, doc_token=None):
        """
        读取飞书文档内容
        
        Args:
            doc_token: 文档token，如果为None则使用配置中的默认值
        
        Returns:
            文档内容（文本）
        """
        if not doc_token:
            doc_token = self.doc_token
        
        if not doc_token:
            print("未配置飞书文档token")
            return None
        
        # 获取access token
        if not self.tenant_access_token:
            self._get_tenant_access_token()
        
        if not self.tenant_access_token:
            return None
        
        # 读取文档内容
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/raw_content"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            result = response.json()
            
            if result.get('code') == 0:
                content = result.get('data', {}).get('content', '')
                return content
            else:
                print(f"读取文档失败: {result.get('msg')}")
                return None
        except Exception as e:
            print(f"读取文档异常: {e}")
            return None
    
    def parse_feedback(self, content):
        """
        解析反馈内容
        
        期望格式：
        第X章：问题描述
        
        Returns:
            反馈列表 [{'chapter': 1, 'feedback': '问题描述'}, ...]
        """
        if not content:
            return []
        
        feedbacks = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 尝试匹配 "第X章" 格式
            if '第' in line and '章' in line:
                try:
                    # 提取章节号
                    start = line.index('第') + 1
                    end = line.index('章')
                    chapter_str = line[start:end].strip()
                    
                    # 转换为数字
                    chapter_num = int(chapter_str)
                    
                    # 提取反馈内容（冒号或：后面的内容）
                    if '：' in line:
                        feedback_text = line.split('：', 1)[1].strip()
                    elif ':' in line:
                        feedback_text = line.split(':', 1)[1].strip()
                    else:
                        feedback_text = line
                    
                    feedbacks.append({
                        'chapter': chapter_num,
                        'feedback': feedback_text
                    })
                except (ValueError, IndexError):
                    continue
        
        return feedbacks


class FeedbackProcessor:
    """反馈处理器"""
    
    def __init__(self):
        self.feishu_client = FeishuClient()
    
    def process_feedbacks(self):
        """处理飞书文档中的反馈"""
        from agents import ContentGenerationAgent
        
        print("=" * 50)
        print("开始处理飞书文档反馈...")
        print("=" * 50)
        
        # 读取文档
        content = self.feishu_client.read_document()
        if not content:
            print("✗ 无法读取飞书文档")
            return
        
        # 解析反馈
        feedbacks = self.feishu_client.parse_feedback(content)
        if not feedbacks:
            print("未找到有效的反馈信息")
            return
        
        print(f"找到 {len(feedbacks)} 条反馈")
        
        # 处理每条反馈
        generation_agent = ContentGenerationAgent()
        for fb in feedbacks:
            chapter_num = fb['chapter']
            feedback_text = fb['feedback']
            
            print(f"\n处理第 {chapter_num} 章的反馈...")
            print(f"反馈内容: {feedback_text}")
            
            # 优化章节
            result = generation_agent.optimize_chapter(chapter_num, feedback_text)
            if result:
                print(f"✓ 第 {chapter_num} 章已优化")
            else:
                print(f"✗ 第 {chapter_num} 章优化失败")
        
        print("\n" + "=" * 50)
        print("反馈处理完成")
        print("=" * 50)

