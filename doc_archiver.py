#!/usr/bin/env python3
"""
文档归档工具 - 智能版
根据文档名自动识别类型并提取核心名称创建文件夹归档

识别模式：
  - 公司文件：XXX有限公司 / XXX集团 / XXX公司 → 提取公司名（保留括号）
  - 大学文件：XXX大学 / XXX学院 → 提取校名
  - 括号处理：仅去除文件描述性括号（如"（合同）"、"（模板）"），保留公司名中的括号
  - 常见后缀：合同、协议、证书、模板、推荐信、证明、申请表、批复、报告、附件...

用法:
  python3 doc_archiver.py <目录路径>        # 交互模式
  python3 doc_archiver.py <目录路径> --auto  # 自动模式
  python3 doc_archiver.py <目录路径> --dry   # 预览模式
"""

import os
import sys
import shutil
import argparse
import re
from pathlib import Path
from datetime import datetime

# 支持的文件扩展名
DEFAULT_EXTS = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
                '.txt', '.md', '.csv', '.zip', '.rar']

# 公司名称后缀关键词
COMPANY_KEYWORDS = [
    '有限公司', '有限责任公司', '股份有限公司', '集团有限公司',
    '集团', '公司', '工厂', '企业',
    '事务所', '律所', '商行', '合作社',
    '分公司', '子公司', '办事处',
]

# 大学/学院后缀关键词
UNIVERSITY_KEYWORDS = [
    '大学', '学院', '职校', '职院',
    '高中', '中学', '小学', '学校',
    '研究院', '研究所', '实验室',
    '党校', '团校', '军校',
]

# 文件描述性后缀（这些不是名称的一部分）
DESC_KEYWORDS = [
    '合同', '协议', '合约', '契约', '保密协议', '补充协议',
    '证书', '证明', '证明材料', '资质', '执照', '许可证',
    '模板', '范本', '样本', '格式', '样式', '示例',
    '推荐信', '申请表', '申请书', '申请表格', '报名表', '登记表',
    '履历表', '简历', '求职信', '自荐信',
    '批复', '复函', '函', '通知', '公告', '通告', '决定', '决议',
    '报告', '请示', '汇报', '总结', '汇报材料',
    '附件', '附录', '清单', '目录', '索引',
    '材料', '补充材料', '变更材料', '审核材料',
    '身份证', '护照', '户口本', '证件', '复印件', '扫描件',
    '原件', '复印件', '电子版', '打印版',
    '原件与复印件', '加盖公章', '签字版',
    '委托书', '授权书', '承诺书', '说明书',
    '计划书', '方案', '策划书', '草案', '初稿', '终稿', '定稿',
    '会议纪要', '纪要', '备忘录',
    '介绍信', '推荐函', '公函',
    '中标通知书', '成交通知书', '入围通知',
    '验收报告', '检测报告', '审计报告', '评估报告', '可行性报告',
    '报价单', '预算表', '结算单', '对账单',
    '发票', '收据', '凭证', '票据',
    '业绩', '业绩表', '财务报表', '报表',
    '章程', '制度', '规定', '办法', '细则', '守则',
    '公告', '声明', '启事',
    '任务书', '责任书', '承诺书', '保证书',
    '备案', '归档', '存档', '资料',
    '照片', '图片', '截图', '扫描件',
    '电子档', 'word版', 'pdf版', 'doc版', 'xls版',
]

# 描述性括号内容（这些括号里的内容是描述，不是名称的一部分）
DESC_PAREN_PATTERNS = [
    # 文件状态类
    r'（\s*合同\s*）', r'（\s*协议\s*）', r'（\s*模板\s*）', r'（\s*范本\s*）',
    r'（\s*暂定\s*）', r'（\s*草稿\s*）', r'（\s*初稿\s*）', r'（\s*终稿\s*）',
    r'（\s*定稿\s*）', r'（\s*正式\s*）', r'（\s*电子版\s*）', r'（\s*打印版\s*）',
    r'（\s*原件\s*）', r'（\s*复印件\s*）', r'（\s*扫描件\s*）',
    r'（\s*盖章\s*）', r'（\s*签字\s*）', r'（\s*加盖公章\s*）',
    r'（\s*已签\s*）', r'（\s*未签\s*）', r'（\s*签章\s*）',
    # 接收/发送状态
    r'（\s*已接收\s*）', r'（\s*已发\s*）', r'（\s*待发\s*）', r'（\s*以接收\s*）',
    r'（\s*收\s*）', r'（\s*发\s*）',
    # 版本/批次
    r'（\s*v\d+\s*）', r'（\s*version\s*\d+\s*）', r'（\s*第\d+版\s*）',
    r'（\s*202\d{1,2}年\s*）', r'（\s*20\d{2}\.\d{1,2}\.\d{1,2}\s*）',
    # 其他描述
    r'（\s*参考\s*）', r'（\s*备用\s*）', r'（\s*存档\s*）', r'（\s*归档\s*）',
    r'（\s*最新\s*）', r'（\s*旧版\s*）', r'（\s*新版\s*）',
]

# 编译正则
DESC_PAREN_RE = re.compile('|'.join(DESC_PAREN_PATTERNS), re.IGNORECASE)

def remove_desc_paren(content: str) -> str:
    """去除描述性括号，保留公司名中的括号"""
    # 先去除描述性括号
    result = DESC_PAREN_RE.sub('', content)
    return result.strip()

def extract_core_name(filename: str) -> str:
    """
    从文件名提取核心名称
    策略：
      - 去掉扩展名
      - 去掉描述性括号（如"（以接收）"、"（合同）"）
      - 找到公司名/大学名作为截止点
      - 去掉描述性后缀（合同、协议、证明等）
    """
    # 去掉扩展名
    name = filename
    for ext in DEFAULT_EXTS:
        if name.lower().endswith(ext):
            name = name[:-len(ext)]
            break

    original = name

    # 去掉描述性括号（保留公司名中的括号）
    name = remove_desc_paren(name)

    # 1. 尝试提取公司名称（保留括号）
    company_match = None
    for kw in COMPANY_KEYWORDS:
        if kw in name:
            idx = name.index(kw)
            core = name[:idx + len(kw)]
            # 去掉后面的描述性后缀
            for desc in DESC_KEYWORDS:
                if core.endswith(desc):
                    core = core[:-len(desc)]
                    break
            # 清理尾部不成对的括号（如多余的"）"）
            core = core.strip()
            # 只去掉末尾不成对的闭合括号
            while core:
                if core[-1] == '）' and core.count('（') < core.count('）'):
                    core = core[:-1]
                elif core[-1] == ')' and core.count('(') < core.count(')'):
                    core = core[:-1]
                elif core[-1] in '）（）【】()':
                    core = core[:-1]
                else:
                    break
            if len(core) >= 2:
                company_match = core
                break
        if company_match:
            break

    if company_match:
        return company_match

    # 2. 尝试提取大学名称
    for kw in UNIVERSITY_KEYWORDS:
        if kw in name:
            idx = name.index(kw)
            core = name[:idx + len(kw)]
            for desc in DESC_KEYWORDS:
                if core.endswith(desc):
                    core = core[:-len(desc)]
                    break
            core = core.strip()
            while core:
                if core[-1] == '）' and core.count('（') < core.count('）'):
                    core = core[:-1]
                elif core[-1] == ')' and core.count('(') < core.count(')'):
                    core = core[:-1]
                elif core[-1] in '）（）【】()':
                    core = core[:-1]
                else:
                    break
            if len(core) >= 2:
                return core

    # 3. 去掉描述性后缀，保留剩余部分
    result = name
    for desc in DESC_KEYWORDS:
        if result.endswith(desc):
            result = result[:-len(desc)]
            break

    result = result.strip()
    while result and result[-1] in '（）【】()':
        result = result[:-1].strip()

    if len(result) < 2:
        return original.strip()

    return result

def scan_directory(directory: Path, exts):
    """扫描目录下的所有支持的文件"""
    files = []
    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() in exts:
            files.append(item)
    return sorted(files, key=lambda x: x.name)

def preview_actions(files, base_dir):
    """预览将要执行的操作"""
    sep = '=' * 60
    print(f"\n{sep}")
    print(f"📁 文档归档预览 - {base_dir}")
    print(f"{sep}\n")

    for i, f in enumerate(files, 1):
        core = extract_core_name(f.name)
        print(f"  {i:2d}. {f.name}")
        print(f"      ⬇  →  ./{core}/")
        print()

    folder_count = len(set(extract_core_name(f.name) for f in files))
    print(f"共找到 {len(files)} 个文件，将创建 {folder_count} 个文件夹\n")

def auto_archive(files, base_dir, dry_mode=False):
    """自动归档"""
    success = []
    skipped = []
    errors = []

    for f in files:
        core = extract_core_name(f.name)
        target_dir = base_dir / core

        try:
            if target_dir.exists() and list(target_dir.iterdir()):
                timestamp = datetime.now().strftime("%H%M%S")
                target_dir = base_dir / f"{core}_{timestamp}"

            if dry_mode:
                print(f"  [预览] 将创建: ./{core}/ 并移动 {f.name}")
            else:
                target_dir.mkdir(exist_ok=True)
                target_path = target_dir / f.name
                shutil.move(str(f), str(target_path))
                print(f"  ✅ {f.name}")
                print(f"      → ./{target_dir.name}/")
                success.append((f.name, target_dir.name))
        except Exception as e:
            print(f"  ❌ 错误: {f.name} - {e}")
            errors.append((f.name, str(e)))

    return success, skipped, errors

def interactive_mode(files, base_dir):
    """交互模式"""
    sep = '=' * 60
    print(f"\n{sep}")
    print(f"📁 文档归档 - {base_dir}")
    print(f"{sep}\n")
    print(f"找到 {len(files)} 个文件:\n")

    for i, f in enumerate(files, 1):
        core = extract_core_name(f.name)
        print(f"  {i:2d}. {f.name}")
        print(f"      → ./{core}/")
    print()

    print("操作选项:")
    print("  [a] 全部归档")
    print("  [s] 全部跳过")
    print("  [p] 预览（不执行）")
    print("  [q] 退出")
    print()

    choice = input("请选择操作 [a/s/p/q]: ").strip().lower()

    if choice == 'a':
        return auto_archive(files, base_dir, dry_mode=False)
    elif choice == 's':
        return [], files, []
    elif choice == 'p':
        preview_actions(files, base_dir)
        return [], [], []
    else:
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description='根据文档名智能识别公司/大学名称并归档（保留括号）',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('directory', nargs='?', default='.',
                        help='要扫描的目录路径（默认当前目录）')
    parser.add_argument('--auto', action='store_true',
                        help='自动模式：直接归档，不询问')
    parser.add_argument('--dry', action='store_true',
                        help='预览模式：只显示将要执行的操作，不实际移动文件')
    parser.add_argument('--ext', nargs='+', default=DEFAULT_EXTS,
                        help='指定文件扩展名')

    args = parser.parse_args()
    directory = Path(args.directory).expanduser().resolve()
    exts = set(args.ext)

    if not directory.exists():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)
    if not directory.is_dir():
        print(f"❌ 不是有效的目录: {directory}")
        sys.exit(1)

    files = scan_directory(directory, exts)

    if not files:
        print(f"📂 在 {directory} 中未找到支持的文档文件")
        sys.exit(0)

    print(f"📂 在 {directory} 中找到 {len(files)} 个文件\n")

    # 显示识别结果预览
    print("📋 识别结果预览：")
    for f in files:
        core = extract_core_name(f.name)
        print(f"  {f.name}")
        print(f"    → {core}")
    print()

    if args.dry:
        preview_actions(files, directory)
        success, skipped, errors = [], [], []
    elif args.auto:
        success, skipped, errors = auto_archive(files, directory, dry_mode=False)
    else:
        success, skipped, errors = interactive_mode(files, directory)

    if success or errors:
        sep = '=' * 60
        print(f"\n{sep}")
        print(f"📊 汇总")
        print(f"{sep}")
        print(f"  ✅ 成功: {len(success)}")
        print(f"  ⏭️  跳过: {len(skipped)}")
        print(f"  ❌ 失败: {len(errors)}")

if __name__ == '__main__':
    main()
