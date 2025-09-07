#!/usr/bin/env python3
"""
快速启动脚本 - MCP Everything Search Server

这个脚本帮助你：
1. 测试配置是否正确
2. 查找 Everything SDK DLL
3. 启动服务器
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """打印欢迎信息"""
    print("=" * 60)
    print("MCP Everything Search Server - 快速启动")
    print("=" * 60)
    print()

def check_python_version():
    """检查 Python 版本"""
    print("检查 Python 版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 版本过低: {version.major}.{version.minor}")
        print("   需要 Python 3.7 或更高版本")
        return False
    else:
        print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True

def check_dependencies():
    """检查依赖项"""
    print("\n检查依赖项...")
    try:
        import asyncio
        print("✅ asyncio 可用")
    except ImportError:
        print("❌ asyncio 不可用")
        return False
    
    try:
        import ctypes
        print("✅ ctypes 可用")
    except ImportError:
        print("❌ ctypes 不可用")
        return False
    
    return True

def find_everything_dll():
    """查找 Everything SDK DLL"""
    print("\n查找 Everything SDK DLL...")
    
    # 检查环境变量
    env_path = os.getenv('EVERYTHING_SDK_PATH')
    if env_path and os.path.exists(env_path):
        print(f"✅ 从环境变量找到: {env_path}")
        return env_path
    
    # 检查常见位置
    common_paths = [
        'C:\\Program Files\\Everything\\Everything64.dll',
        'C:\\Program Files (x86)\\Everything\\Everything64.dll',
        'D:\\dev\\tools\\Everything-SDK\\dll\\Everything64.dll',
        str(Path.cwd() / 'Everything64.dll'),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ 找到 DLL: {path}")
            return path
    
    # 使用 glob 搜索
    import glob
    search_patterns = [
        'C:\\Program Files\\Everything\\Everything*.dll',
        'C:\\Program Files (x86)\\Everything\\Everything*.dll',
        'D:\\*\\Everything-SDK\\dll\\Everything*.dll',
        'C:\\*\\Everything-SDK\\dll\\Everything*.dll'
    ]
    
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            print(f"✅ 通过搜索找到: {matches[0]}")
            return matches[0]
    
    print("❌ 未找到 Everything SDK DLL")
    return None

def suggest_solutions():
    """提供解决方案建议"""
    print("\n" + "=" * 60)
    print("解决方案建议:")
    print("=" * 60)
    
    print("\n1. 安装 Everything 软件（推荐）:")
    print("   - 访问: https://www.voidtools.com/")
    print("   - 下载并安装 Everything")
    print("   - DLL 将自动安装到: C:\\Program Files\\Everything\\")
    
    print("\n2. 设置环境变量:")
    print("   PowerShell:")
    print("   $env:EVERYTHING_SDK_PATH = 'C:\\path\\to\\Everything64.dll'")
    print("   命令提示符:")
    print("   set EVERYTHING_SDK_PATH=C:\\path\\to\\Everything64.dll")
    
    print("\n3. 下载 Everything SDK:")
    print("   - 访问: https://www.voidtools.com/support/everything/sdk/")
    print("   - 下载 SDK 并解压到项目目录")
    print("   - 将 Everything64.dll 放在项目根目录")
    
    print("\n4. 修改配置文件:")
    print("   - 编辑 config.py 文件")
    print("   - 在 DEFAULT_DLL_PATHS 中添加你的 DLL 路径")

def test_config():
    """测试配置"""
    print("\n测试配置...")
    try:
        from config import find_everything_dll
        dll_path = find_everything_dll()
        print(f"✅ 配置测试成功: {dll_path}")
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def start_server():
    """启动服务器"""
    print("\n启动 MCP 服务器...")
    try:
        # 切换到正确的目录
        server_dir = Path(__file__).parent / 'src' / 'mcp_server_everything_search'
        os.chdir(server_dir)
        
        # 启动服务器
        cmd = [sys.executable, '-m', 'mcp_server_everything_search']
        print(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 服务器启动成功")
        else:
            print(f"❌ 服务器启动失败:")
            print(f"   错误输出: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 启动服务器时出错: {e}")

def main():
    """主函数"""
    print_header()
    
    # 检查基本要求
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    # 查找 DLL
    dll_path = find_everything_dll()
    
    if not dll_path:
        suggest_solutions()
        return
    
    # 测试配置
    if not test_config():
        return
    
    # 询问是否启动服务器
    print(f"\n✅ 所有检查都通过了！")
    print(f"Everything SDK DLL 位置: {dll_path}")
    
    response = input("\n是否现在启动 MCP 服务器？(y/n): ").lower().strip()
    if response in ['y', 'yes', '是']:
        start_server()
    else:
        print("\n要手动启动服务器，请运行:")
        print("python -m mcp_server_everything_search")

if __name__ == '__main__':
    main()
