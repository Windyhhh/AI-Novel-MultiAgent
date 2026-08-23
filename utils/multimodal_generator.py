"""
Multimodal Generator - 多模态内容生成器
支持文本、图像、音频等多媒体小说创作
"""

import json
import os
import base64
from typing import Dict, List, Any, Optional
from utils.llm_client import LLMClient
from utils.logger import get_logger

logger = get_logger(__name__)


class MultimodalGenerator:
    """多模态内容生成器，支持文本+图像+音频的综合创作"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.supported_modes = ['text', 'image_description', 'audio_description', 'scene_visualization']
        self.style_presets = {
            'realistic': '写实风格，注重细节描写',
            'fantasy': '奇幻风格，富有想象力',
            'noir': '黑色电影风格，氛围感强烈',
            'romantic': '浪漫风格，情感细腻',
            'thriller': '悬疑惊悚风格，紧张感强烈'
        }
    
    def generate_multimodal_chapter(self, chapter_plan: Dict[str, Any], 
                                   multimodal_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        生成多模态章节内容
        
        Args:
            chapter_plan: 章节计划
            multimodal_config: 多模态配置
            
        Returns:
            包含文本、图像描述、音频描述等的多模态内容
        """
        try:
            config = multimodal_config or {}
            
            # 生成主要文本内容
            text_content = self._generate_text_content(chapter_plan, config)
            
            result = {
                'text_content': text_content,
                'chapter_number': chapter_plan.get('chapter_number'),
                'title': chapter_plan.get('chapter_title', ''),
                'word_count': len(text_content),
                'multimodal_elements': {}
            }
            
            # 生成图像描述（如果需要）
            if config.get('include_images', False):
                image_descriptions = self._generate_image_descriptions(text_content, config)
                result['multimodal_elements']['images'] = image_descriptions
            
            # 生成音频描述（如果需要）
            if config.get('include_audio', False):
                audio_descriptions = self._generate_audio_descriptions(text_content, config)
                result['multimodal_elements']['audio'] = audio_descriptions
            
            # 生成场景可视化（如果需要）
            if config.get('include_visualization', False):
                scene_visualizations = self._generate_scene_visualizations(text_content, config)
                result['multimodal_elements']['visualizations'] = scene_visualizations
            
            # 生成阅读体验增强元素
            if config.get('include_experience_enhancement', True):
                experience_elements = self._generate_experience_elements(text_content, config)
                result['multimodal_elements']['experience'] = experience_elements
            
            return result
            
        except Exception as e:
            logger.error(f"多模态章节生成失败: {e}")
            return {
                'text_content': '',
                'error': str(e),
                'multimodal_elements': {}
            }
    
    def _generate_text_content(self, chapter_plan: Dict[str, Any], config: Dict[str, Any]) -> str:
        """生成文本内容"""
        style = config.get('style', 'realistic')
        target_length = config.get('target_length', 3000)
        
        text_prompt = f"""
请根据以下章节计划生成小说内容：

【章节信息】
章节号：{chapter_plan.get('chapter_number')}
章节标题：{chapter_plan.get('chapter_title', '')}
主要情节：{json.dumps(chapter_plan.get('main_plot_points', []), ensure_ascii=False)}
角色发展：{json.dumps(chapter_plan.get('character_development', []), ensure_ascii=False)}

【创作要求】
1. 风格：{self.style_presets.get(style, style)}
2. 目标字数：{target_length}字
3. 适合多媒体呈现：内容要有画面感，便于后续生成图像和音频描述
4. 场景描写丰富：包含详细的环境、人物、动作描述
5. 情感表达充分：便于后续音频情感表达

请生成章节内容：
"""
        
        return self.llm_client.generate(text_prompt).strip()
    
    def _generate_image_descriptions(self, text_content: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成图像描述"""
        image_style = config.get('image_style', 'illustration')
        max_images = config.get('max_images', 3)
        
        image_prompt = f"""
请为以下小说内容生成{max_images}个关键场景的图像描述：

【小说内容】
{text_content}

【要求】
1. 选择最具视觉冲击力的{max_images}个场景
2. 每个场景提供详细的图像描述，包括：
   - 场景环境（时间、地点、氛围）
   - 人物外观和姿态
   - 画面构图和色调
   - 艺术风格：{image_style}
3. 描述要适合AI绘画工具生成

请按以下JSON格式输出：
```json
[
  {{
    "scene_name": "场景名称",
    "position_in_text": "在文中的大概位置",
    "image_description": "详细的图像描述",
    "style_tags": ["风格标签1", "风格标签2"],
    "mood": "画面情感基调"
  }}
]
```
"""
        
        try:
            response = self.llm_client.generate(image_prompt)
            json_match = json.loads(response.split('```json')[1].split('```')[0])
            return json_match if isinstance(json_match, list) else []
        except Exception as e:
            logger.error(f"图像描述生成失败: {e}")
            return []
    
    def _generate_audio_descriptions(self, text_content: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """生成音频描述"""
        audio_elements = config.get('audio_elements', ['background_music', 'sound_effects', 'voice_tone'])
        
        audio_prompt = f"""
请为以下小说内容生成音频描述：

【小说内容】
{text_content}

【音频元素要求】
{', '.join(audio_elements)}

请按以下JSON格式输出：
```json
{{
  "background_music": {{
    "style": "音乐风格",
    "mood": "情感基调",
    "tempo": "节奏",
    "description": "具体描述"
  }},
  "sound_effects": [
    {{
      "position": "在文中位置",
      "effect": "音效类型", 
      "description": "音效描述"
    }}
  ],
  "voice_guidance": {{
    "narrator_tone": "叙述者音调",
    "character_voices": {{
      "角色名": "声音特点"
    }},
    "reading_pace": "阅读节奏建议"
  }},
  "ambient_sounds": [
    {{
      "environment": "环境音",
      "description": "环境音描述"
    }}
  ]
}}
```
"""
        
        try:
            response = self.llm_client.generate(audio_prompt)
            json_match = json.loads(response.split('```json')[1].split('```')[0])
            return json_match if isinstance(json_match, dict) else {}
        except Exception as e:
            logger.error(f"音频描述生成失败: {e}")
            return {}
    
    def _generate_scene_visualizations(self, text_content: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成场景可视化描述"""
        viz_type = config.get('visualization_type', '3d_scene')
        
        viz_prompt = f"""
请为以下小说内容生成场景可视化描述，用于3D场景或VR体验：

【小说内容】
{text_content}

【可视化要求】
1. 类型：{viz_type}
2. 包含空间布局、物体位置、光照效果
3. 适合虚拟现实或3D渲染

请按以下JSON格式输出：
```json
[
  {{
    "scene_id": "场景标识",
    "scene_name": "场景名称",
    "spatial_layout": {{
      "environment": "环境类型",
      "dimensions": "空间规模",
      "key_objects": ["关键物体1", "关键物体2"],
      "layout_description": "布局描述"
    }},
    "lighting": {{
      "type": "光照类型",
      "intensity": "强度",
      "color_temperature": "色温",
      "description": "光照描述"
    }},
    "camera_angles": [
      {{
        "angle": "机位角度",
        "description": "视角描述"
      }}
    ],
    "interactive_elements": ["可互动元素1", "可互动元素2"]
  }}
]
```
"""
        
        try:
            response = self.llm_client.generate(viz_prompt)
            json_match = json.loads(response.split('```json')[1].split('```')[0])
            return json_match if isinstance(json_match, list) else []
        except Exception as e:
            logger.error(f"场景可视化生成失败: {e}")
            return []
    
    def _generate_experience_elements(self, text_content: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """生成阅读体验增强元素"""
        experience_prompt = f"""
请为以下小说内容生成阅读体验增强元素：

【小说内容】
{text_content}

请按以下JSON格式输出：
```json
{{
  "reading_rhythm": {{
    "fast_paced_sections": ["快节奏段落位置"],
    "slow_paced_sections": ["慢节奏段落位置"],
    "pause_points": ["适合暂停的位置"],
    "climax_points": ["高潮点位置"]
  }},
  "emotional_markers": [
    {{
      "position": "位置",
      "emotion": "情感类型",
      "intensity": "强度(1-10)",
      "description": "情感描述"
    }}
  ],
  "immersion_tips": [
    {{
      "type": "沉浸技巧类型",
      "description": "技巧描述",
      "application": "应用方式"
    }}
  ],
  "interactive_suggestions": [
    {{
      "type": "互动类型",
      "description": "互动描述",
      "trigger_point": "触发点"
    }}
  ]
}}
```
"""
        
        try:
            response = self.llm_client.generate(experience_prompt)
            json_match = json.loads(response.split('```json')[1].split('```')[0])
            return json_match if isinstance(json_match, dict) else {}
        except Exception as e:
            logger.error(f"体验元素生成失败: {e}")
            return {}
    
    def create_multimedia_package(self, chapters: List[Dict[str, Any]], 
                                 package_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """创建多媒体小说包"""
        config = package_config or {}
        
        multimedia_package = {
            'title': config.get('novel_title', '未命名小说'),
            'description': config.get('novel_description', ''),
            'chapters': [],
            'global_assets': {
                'character_profiles': [],
                'location_gallery': [],
                'soundtrack_playlist': [],
                'style_guide': {}
            },
            'package_info': {
                'total_chapters': len(chapters),
                'creation_date': config.get('creation_date', ''),
                'multimodal_elements_count': 0
            }
        }
        
        total_multimodal_elements = 0
        
        for chapter in chapters:
            multimodal_chapter = self.generate_multimodal_chapter(chapter, config)
            multimedia_package['chapters'].append(multimodal_chapter)
            
            # 统计多媒体元素
            if 'multimodal_elements' in multimodal_chapter:
                for element_type, elements in multimodal_chapter['multimodal_elements'].items():
                    if isinstance(elements, list):
                        total_multimodal_elements += len(elements)
                    elif isinstance(elements, dict):
                        total_multimodal_elements += len(elements)
        
        multimedia_package['package_info']['multimodal_elements_count'] = total_multimodal_elements
        
        # 生成全局资产
        multimedia_package['global_assets'] = self._generate_global_assets(chapters, config)
        
        return multimedia_package
    
    def _generate_global_assets(self, chapters: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
        """生成全局多媒体资产"""
        # 提取所有章节的文本内容
        all_text = "\n\n".join([ch.get('content', ch.get('text_content', '')) for ch in chapters])
        
        assets_prompt = f"""
请基于以下完整小说内容，生成全局多媒体资产：

【小说内容概要】
{all_text[:2000]}...  # 取前2000字符作为概要

请按以下JSON格式输出：
```json
{{
  "character_profiles": [
    {{
      "name": "角色名",
      "description": "外貌描述",
      "personality": "性格特点",
      "voice_characteristics": "声音特点",
      "visual_style": "视觉风格"
    }}
  ],
  "location_gallery": [
    {{
      "name": "地点名",
      "description": "地点描述",
      "atmosphere": "氛围",
      "visual_elements": "视觉元素",
      "audio_elements": "音频元素"
    }}
  ],
  "soundtrack_playlist": [
    {{
      "title": "音乐标题",
      "style": "音乐风格",
      "usage": "使用场景",
      "mood": "情绪基调"
    }}
  ],
  "style_guide": {{
    "visual_style": "整体视觉风格",
    "color_palette": ["颜色1", "颜色2", "颜色3"],
    "typography": "字体风格",
    "ui_elements": "界面元素风格"
  }}
}}
```
"""
        
        try:
            response = self.llm_client.generate(assets_prompt)
            json_match = json.loads(response.split('```json')[1].split('```')[0])
            return json_match if isinstance(json_match, dict) else {}
        except Exception as e:
            logger.error(f"全局资产生成失败: {e}")
            return {}
    
    def export_to_format(self, multimedia_package: Dict[str, Any], format_type: str) -> Dict[str, Any]:
        """导出多媒体包为指定格式"""
        formats = {
            'epub_enhanced': self._export_to_epub_enhanced,
            'interactive_web': self._export_to_interactive_web,
            'audiobook_script': self._export_to_audiobook_script,
            'vr_experience': self._export_to_vr_experience
        }
        
        if format_type not in formats:
            return {'error': f'不支持的格式类型: {format_type}'}
        
        try:
            return formats[format_type](multimedia_package)
        except Exception as e:
            logger.error(f"导出格式{format_type}失败: {e}")
            return {'error': str(e)}
    
    def _export_to_epub_enhanced(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """导出为增强型EPUB"""
        # 这里可以集成EPUB生成库
        return {
            'format': 'epub_enhanced',
            'structure': {
                'metadata': package.get('package_info', {}),
                'chapters': [
                    {
                        'title': ch.get('title', ''),
                        'text': ch.get('text_content', ''),
                        'images': ch.get('multimodal_elements', {}).get('images', []),
                        'audio_cues': ch.get('multimodal_elements', {}).get('audio', {})
                    }
                    for ch in package.get('chapters', [])
                ],
                'assets': package.get('global_assets', {})
            }
        }
    
    def _export_to_interactive_web(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """导出为交互式Web应用"""
        return {
            'format': 'interactive_web',
            'components': {
                'reader_interface': 'HTML/CSS/JS界面代码',
                'chapter_data': package.get('chapters', []),
                'media_assets': package.get('global_assets', {}),
                'interaction_scripts': '交互脚本代码'
            }
        }
    
    def _export_to_audiobook_script(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """导出为有声书脚本"""
        audiobook_script = []
        
        for chapter in package.get('chapters', []):
            script_item = {
                'chapter_number': chapter.get('chapter_number'),
                'title': chapter.get('title', ''),
                'narration_text': chapter.get('text_content', ''),
                'voice_guidance': chapter.get('multimodal_elements', {}).get('audio', {}).get('voice_guidance', {}),
                'background_music': chapter.get('multimodal_elements', {}).get('audio', {}).get('background_music', {}),
                'sound_effects': chapter.get('multimodal_elements', {}).get('audio', {}).get('sound_effects', [])
            }
            audiobook_script.append(script_item)
        
        return {
            'format': 'audiobook_script',
            'script': audiobook_script,
            'production_notes': {
                'total_chapters': len(audiobook_script),
                'estimated_duration': len(package.get('chapters', [])) * 15,  # 假设每章15分钟
                'voice_cast': package.get('global_assets', {}).get('character_profiles', [])
            }
        }
    
    def _export_to_vr_experience(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """导出为VR体验"""
        vr_scenes = []
        
        for chapter in package.get('chapters', []):
            visualizations = chapter.get('multimodal_elements', {}).get('visualizations', [])
            for viz in visualizations:
                vr_scene = {
                    'scene_id': viz.get('scene_id'),
                    'chapter_reference': chapter.get('chapter_number'),
                    'spatial_data': viz.get('spatial_layout', {}),
                    'lighting_config': viz.get('lighting', {}),
                    'interactive_elements': viz.get('interactive_elements', []),
                    'audio_environment': chapter.get('multimodal_elements', {}).get('audio', {})
                }
                vr_scenes.append(vr_scene)
        
        return {
            'format': 'vr_experience',
            'scenes': vr_scenes,
            'navigation': {
                'scene_transitions': '场景转换逻辑',
                'user_interactions': '用户交互设置'
            },
            'assets_required': package.get('global_assets', {})
        }


class MultimodalAnalyzer:
    """多模态内容分析器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def analyze_multimedia_effectiveness(self, multimedia_package: Dict[str, Any]) -> Dict[str, Any]:
        """分析多媒体效果"""
        analysis_prompt = f"""
请分析以下多媒体小说包的效果：

【包信息】
章节数：{multimedia_package.get('package_info', {}).get('total_chapters', 0)}
多媒体元素数：{multimedia_package.get('package_info', {}).get('multimodal_elements_count', 0)}

【分析维度】
1. 多媒体元素与文本的匹配度
2. 沉浸感提升效果
3. 用户体验优化程度
4. 技术实现可行性
5. 商业价值潜力

请按以下JSON格式输出分析结果：
```json
{{
  "effectiveness_scores": {{
    "text_media_alignment": 分数,
    "immersion_enhancement": 分数,
    "user_experience": 分数,
    "technical_feasibility": 分数,
    "commercial_potential": 分数
  }},
  "strengths": ["优势1", "优势2"],
  "improvement_areas": ["改进点1", "改进点2"],
  "recommendations": ["建议1", "建议2"]
}}
```
"""
        
        try:
            response = self.llm_client.generate(analysis_prompt)
            json_match = json.loads(response.split('```json')[1].split('```')[0])
            return json_match if isinstance(json_match, dict) else {}
        except Exception as e:
            logger.error(f"多媒体效果分析失败: {e}")
            return {}
