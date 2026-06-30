#!/usr/bin/env python3
"""
Fix pip 26.x resolvelib RequirementInformation import error in p4a venv.

Root cause:
  pip 26.1.2 bundles resolvelib where RequirementInformation was moved from
  structs.py to resolvers/candidates.py. The resolvers/__init__.py still
  tries "from ..structs import RequirementInformation" which fails.

Fix:
  Patch resolvers/__init__.py to import from the correct location.
  Use absolute import from the resolvers package.
"""
import sys
import os
import time
import glob

def log(msg):
    print(msg, flush=True)

def find_venv_structs(workspace):
    """Find the venv structs.py file."""
    search_paths = [
        os.path.join(workspace, ".buildozer", "android", "platform", "build-arm64-v8a_armeabi-v7a",
                     "build", "venv", "lib", "python3.11", "site-packages",
                     "pip", "_vendor", "resolvelib", "resolvers", "__init__.py"),
        os.path.join(workspace, ".buildozer", "android", "platform", "build-armeabi-v7a",
                     "build", "venv", "lib", "python3.11", "site-packages",
                     "pip", "_vendor", "resolvelib", "resolvers", "__init__.py"),
    ]
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    # Fallback: glob
    patterns = [
        os.path.join(workspace, ".buildozer", "android", "platform", "build-*",
                     "build", "venv", "lib", "python3.11", "site-packages",
                     "pip", "_vendor", "resolvelib", "resolvers", "__init__.py"),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        for m in matches:
            return m
    return None

def patch_resolvers_init(resolvers_init_path):
    """Patch resolvers/__init__.py to fix RequirementInformation import."""
    structs_path = resolvers_init_path.replace("/resolvers/__init__.py", "/structs.py")
    
    with open(resolvers_init_path, encoding="utf-8") as f:
        content = f.read()
    
    if "fix_pip_v4" in content:
        log(f"[OK] Already patched: {resolvers_init_path}")
        return True
    
    # The problematic line
    bad_import = "from ..structs import RequirementInformation"
    
    if bad_import not in content:
        log(f"[SKIP] Import line not found (already fixed or different version)")
        log(f"  First 3 lines: {content.split(chr(10))[:3]}")
        return True
    
    # Build the fix: try structs, then try candidates, then fallback
    new_import = '''# fix_pip_v4: safe RequirementInformation import (pip 26+ compatibility)
try:
    from ..structs import RequirementInformation
except ImportError:
    try:
        from .candidates import RequirementInformation
    except ImportError:
        try:
            from . import RequirementInformation
        except ImportError:
            from collections import namedtuple
            RequirementInformation = namedtuple("RequirementInformation", ["requirement", "parent"])
'''
    
    content = content.replace(bad_import, new_import)
    
    with open(resolvers_init_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    log(f"[OK] Patched resolvers/__init__.py")
    return True

def patch_structs_also(structs_path):
    """Also patch structs.py to ensure RequirementInformation is available."""
    if not os.path.exists(structs_path):
        return False
    
    with open(structs_path, encoding="utf-8") as f:
        content = f.read()
    
    if "fix_pip_v4" in content:
        return True
    
    # Only patch if RequirementInformation is inside TYPE_CHECKING and no fallback exists
    has_ri_at_top = False
    for line in content.split("\n"):
        stripped = line.strip()
        if (stripped.startswith("RequirementInformation = ") and
            not stripped.startswith("try:")):
            has_ri_at_top = True
            break
    
    if not has_ri_at_top and "from .resolvers.candidates" not in content:
        # Try to import from candidates.py
        candidates_path = os.path.join(os.path.dirname(structs_path), "candidates.py")
        has_candidates_ri = False
        if os.path.exists(candidates_path):
            with open(candidates_path, encoding="utf-8") as f:
                has_candidates_ri = "class RequirementInformation" in f.read() or \
                                   "def RequirementInformation" in f.read() or \
                                   "RequirementInformation = " in f.read()
        
        if has_candidates_ri:
            patch = '''
# fix_pip_v4: ensure RequirementInformation available at module level
try:
    from .resolvers.candidates import RequirementInformation
except ImportError:
    pass
try:
    from . import RequirementInformation
except ImportError:
    pass
if "RequirementInformation" not in dir():
    from collections import namedtuple
    RequirementInformation = namedtuple("RequirementInformation", ["requirement", "parent"])
'''
            with open(structs_path, "a", encoding="utf-8") as f:
                f.write(patch)
            log(f"[OK] Patched structs.py")
    
    return True

def run_fix():
    """Run the fix once."""
    workspace = os.environ.get("GITHUB_WORKSPACE", 
                              os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    log(f"[FIX] Python: {sys.version}")
    log(f"[FIX] Workspace: {workspace}")
    log(f"[FIX] CWD: {os.getcwd()}")
    
    resolvers_init = find_venv_structs(workspace)
    if resolvers_init:
        log(f"[FIX] Found: {resolvers_init}")
        patch_resolvers_init(resolvers_init)
        structs_path = resolvers_init.replace("/resolvers/__init__.py", "/structs.py")
        patch_structs_also(structs_path)
        log("[FIX] Done!")
        return True
    else:
        log(f"[FIX] Venv resolvers/__init__.py not found")
        return False

def main():
    log("=" * 60)
    log("p4a pip 26.x RequirementInformation fix (v4)")
    log("=" * 60)
    
    # Try immediately
    if run_fix():
        return
    
    # Monitor for up to 30 minutes
    log("Venv not found, monitoring for 30 minutes...")
    for i in range(1800):
        time.sleep(1)
        if run_fix():
            log(f"[FIX] Applied at t={i}s")
            return
        if i % 60 == 0 and i > 0:
            log(f"  Still monitoring... t={i}s")
    
    log("Timeout - venv not found")

if __name__ == "__main__":
    main()
