import json
import re
import unicodedata
import os
from pathlib import Path
from datetime import datetime


class TheoryExporter:
    def __init__(self, output_dir="theory_db"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, theory_name, lean_type, content):
        # 验证输入
        if not content.strip():
            raise ValueError("内容不能为空")

        # 清理名称
        safe_name = self.sanitize_name(theory_name)

        # 构建数据结构
        data = {
            "metadata": {
                "name": theory_name,
                "type": lean_type,
                "created_at": datetime.now().isoformat(),
                "safe_name": safe_name
            },
            "content": content
        }

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{safe_name}_{timestamp}.json"
        filepath = self.output_dir / filename

        # 路径长度验证
        if len(str(filepath)) > 255:
            raise ValueError("文件路径过长，请缩短名称")

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def sanitize_name(self, raw_name):
        """强化名称清理"""
        # 处理空值
        if not raw_name.strip():
            return "unnamed"

        # Unicode规范化
        name = unicodedata.normalize('NFKD', raw_name)
        # 移除特殊字符
        name = re.sub(r'[^\w\s_\-]', '', name)
        # 替换空格
        name = re.sub(r'\s+', '_', name)
        # 截断长度
        return name[:100].strip('_')

    @staticmethod
    def validate_type(lean_type):
        valid_types = ["theory", "def", "lemma", "formula"]
        if lean_type not in valid_types:
            raise ValueError(f"无效类型，可选值：{valid_types}")
