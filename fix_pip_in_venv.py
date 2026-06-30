#!/usr/bin/env python3
"""
fix_pip_in_venv.py
淇 p4a venv 涓?pip 鐨?RequirementInformation 瀵煎叆閿欒

閿欒锛歠rom pip._vendor.resolvelib.resolvers import RequirementInformation
ImportError: cannot import name 'RequirementInformation' from 'pip._vendor.resolvelib.structs'

鍘熷洜锛歱ip 24+ 鐨?vendored resolvelib 閲嶆瀯浜嗙被鍚嶏紝浣?resolvers/__init__.py 
     浠嶇劧灏濊瘯浠?structs 瀵煎叆 RequirementInformation銆?
瑙ｅ喅鏂规锛氫慨琛?resolvers/__init__.py锛屽湪瀵煎叆澶辫触鏃舵彁渚涘吋瀹逛唬鐮併€?"""

import sys
import os
import time
import glob
import shutil
import stat

PYTHON_PATCH = '''
# --- fix_pip: RequirementInformation compat (patched by fix_pip_in_venv.py) ---
try:
    from ..structs import RequirementInformation
except ImportError:
    # pip 24+ removed RequirementInformation from structs
    # Provide a compatibility shim
    try:
        from ..structs import RequirementInfo
        class RequirementInformation(RequirementInfo):
            """Compatibility shim for RequirementInformation -> RequirementInfo"""
            pass
        # Make it look like the original for isinstance checks
        RequirementInformation.__bases__ = (RequirementInfo,)
    except ImportError:
        raise ImportError("Could not import RequirementInformation or RequirementInfo")
# --- end fix ---
'''

def patch_resolvers_init(structs_file):
    """淇ˉ resolvers/__init__.py"""
    resolvers_init = os.path.join(os.path.dirname(structs_file), '__init__.py')
    
    if not os.path.exists(resolvers_init):
        return False
    
    with open(resolvers_init, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'fix_pip' in content:
        print(f"[fix] Already patched: {resolvers_init}")
        return True
    
    # 鎵惧埌 from ..structs import RequirementInformation 骞舵浛鎹?    if 'from ..structs import RequirementInformation' in content:
        content = content.replace(
            'from ..structs import RequirementInformation',
            PYTHON_PATCH.strip()
        )
        
        with open(resolvers_init, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[fix] 鉁?Patched resolvers/__init__.py")
        
        # 閲嶇疆 pip 妯″潡缂撳瓨
        for mod in list(sys.modules.keys()):
            if 'pip' in mod or 'resolvelib' in mod:
                del sys.modules[mod]
        
        return True
    
    return False


def patch_structs_file(structs_file):
    """淇ˉ structs.py - 娣诲姞 RequirementInformation 绫?""
    with open(structs_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'fix_pip' in content:
        print(f"[fix] structs.py already patched")
        return True
    
    if 'class RequirementInformation' in content:
        print(f"[fix] RequirementInformation already exists in structs.py")
        return True
    
    if 'class RequirementInfo' not in content:
        print(f"[fix] RequirementInfo not found in structs.py")
        return False
    
    patch = '''
# --- fix_pip: RequirementInformation compat ---
class RequirementInformation:
    """
    Compatibility shim for pip 24+ resolvelib.
    RequirementInformation was removed and replaced with RequirementInfo.
    """
    def __init__(self, candidate, source, parent=None):
        self.candidate = candidate
        self.source = source
        self.parent = parent
    
    def __repr__(self):
        return f"RequirementInformation({self.candidate!r}, {self.source!r})"
    
    def __eq__(self, other):
        if isinstance(other, RequirementInformation):
            return self.candidate == other.candidate
        return False
# --- end fix ---
'''
    
    with open(structs_file, 'a', encoding='utf-8') as f:
        f.write(patch)
    
    print(f"[fix] 鉁?Patched structs.py with RequirementInformation class")
    return True


def find_and_fix_venv_pip():
    """鏌ユ壘骞朵慨澶?p4a venv 鐨?pip"""
    patterns = [
        ".buildozer/android/platform/build-*/build/venv/lib/python*/site-packages/pip/_vendor/resolvelib/structs.py",
    ]
    
    for pattern in patterns:
        for structs_file in glob.glob(pattern):
            print(f"\n[fix] Found: {structs_file}")
            
            # 鏂规1: 淇ˉ resolvers/__init__.py
            if patch_resolvers_init(structs_file):
                return True
            
            # 鏂规2: 淇ˉ structs.py
            if patch_structs_file(structs_file):
                # 閲嶅懡鍚?pip 涓?pip-real 骞跺垱寤?wrapper
                venv_bin = os.path.dirname(os.path.dirname(
                    os.path.dirname(structs_file.replace('/pip/_vendor/resolvelib/structs.py', ''))
                ))
                pip_bin = os.path.join(venv_bin, 'pip')
                pip_real = os.path.join(venv_bin, 'pip-real')
                
                if os.path.exists(pip_bin) and not os.path.exists(pip_real):
                    shutil.copy2(pip_bin, pip_real)
                    os.chmod(pip_bin, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                    
                    # 鍒涘缓 wrapper
                    wrapper = f'''#!/usr/bin/env python3
import sys, os, time, glob, runpy

def _patch():
    for pattern in [".buildozer/android/platform/build-*/build/venv/lib/python*/site-packages/pip/_vendor/resolvelib/structs.py"]:
        for sf in glob.glob(pattern):
            ri = os.path.join(os.path.dirname(sf), "__init__.py")
            if os.path.exists(ri):
                c = open(ri).read()
                if 'fix_pip' not in c and 'RequirementInformation' in c:
                    open(ri, "a").write('''
{repr(PYTHON_PATCH.strip())}
''')
                    print("[pip-w] Patched resolvers/__init__.py", file=sys.stderr)
                    for m in list(sys.modules.keys()):
                        if "pip" in m or "resolvelib" in m:
                            del sys.modules[m]
                    break

if __name__ == "__main__":
    _patch()
    real = "{pip_real}"
    sys.argv[0] = real
    runpy.run_path(real, run_name="__main__")
'''
                    
                    with open(pip_bin, 'w') as f:
                        f.write("#!/usr/bin/env python3\n" + wrapper)
                    os.chmod(pip_bin, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                    print(f"[fix] 鉁?Installed pip wrapper in {venv_bin}")
                
                return True
    
    return False


def main():
    print("=" * 60)
    print("p4a venv pip Fix - RequirementInformation Import Error")
    print("=" * 60)
    
    # 绔嬪嵆灏濊瘯淇ˉ
    if find_and_fix_venv_pip():
        print("\n鉁?Fix applied successfully!")
        return
    
    # 鎸佺画鐩戞帶
    print("\nVenv not found yet, monitoring for 5 minutes...")
    for i in range(300):
        time.sleep(1)
        if find_and_fix_venv_pip():
            print(f"\n鉁?Fix applied at {i}s!")
            return
        
        if i % 15 == 0:
            print(f"  [{i}s] Still monitoring...")
    
    print("\n鈿狅笍 Timeout - venv not found within 5 minutes")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        find_and_fix_venv_pip()
    else:
        main()
