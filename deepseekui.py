import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import os


class FormulaConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math2Lean4 Pro")
        self.root.geometry("1000x800")

        # API配置
        self.API_URL = "https://api.deepseek.com/v1/chat/completions"
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

        # 创建界面
        self.create_widgets()
        self.setup_style()

    def setup_style(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, font=('Arial', 10))
        style.configure("Red.TLabel", foreground="red")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="Entering math formulas")
        input_frame.pack(fill=tk.X, pady=10)

        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 12))
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # 元数据输入
        self.meta_frame = ttk.Frame(main_frame)
        self.meta_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.meta_frame, text="Theoretical name:").pack(side=tk.LEFT)
        self.theory_name = ttk.Entry(self.meta_frame, width=40)
        self.theory_name.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.meta_frame, text="type:").pack(side=tk.LEFT, padx=10)
        self.type_combo = ttk.Combobox(
            self.meta_frame,
            values=["theory", "def", "lemma", "formula"],
            state="readonly",
            width=12
        )
        self.type_combo.current(0)
        self.type_combo.pack(side=tk.LEFT)

        # 转换按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(
            btn_frame,
            text="Convert and save",
            command=self.convert_and_save
        ).pack(side=tk.LEFT, padx=5)

        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="Lean4 output")
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=20,
            wrap=tk.WORD,
            font=('Consolas', 11),
            state='disabled'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_bar = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=5)

    def convert_and_save(self):
        try:
            formula = self.input_text.get("1.0", tk.END).strip()
            if not formula:
                raise ValueError("Entering math formulas")

            lean_code = self._call_deepseek_api(formula)
            self._display_output(lean_code)
            self._save_results(lean_code)
            self.status_bar.config(text="Conversion saved successfully", foreground="green")

        except Exception as e:
            self._handle_error(e)

    def _call_deepseek_api(self, formula):
        headers = {
            "Authorization": f"Bearer {self.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-reasoner",
            "messages": [
                {
                    "role": "system",
                    "content": "生成Lean4代码，包含变量声明和证明骨架，不要解释"
                },
                {
                    "role": "user",
                    "content": formula
                }
            ],
            "temperature": 0.1
        }

        response = requests.post(self.API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _display_output(self, content):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, content)
        self.output_text.config(state='disabled')

    def _save_results(self, content):
        from theory2json import TheoryExporter

        # 获取用户输入或自动生成
        theory_name = self.theory_name.get().strip()
        lean_type = self.type_combo.get()

        # 保存原始文本
        txt_path = self._save_text(content)

        # 保存JSON
        exporter = TheoryExporter()
        json_path = exporter.export(
            theory_name=theory_name or "未命名理论",
            lean_type=lean_type,
            content=content
        )

        # 更新状态
        self.status_bar.config(
            text=f"保存路径: TXT - {txt_path} | JSON - {json_path}"
        )

    def _save_text(self, content):
        os.makedirs("outputs", exist_ok=True)
        txt_path = os.path.join("outputs", "lean_output.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(content)
        return txt_path

    def _handle_error(self, error):
        error_msg = f"错误: {str(error)}"
        self.status_bar.config(text=error_msg, foreground="red")
        messagebox.showerror("Operation failed", error_msg)
