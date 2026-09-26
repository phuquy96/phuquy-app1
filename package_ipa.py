import os
import sys
import struct
import shutil
import zipfile
from make_signable_macho import create_signable_arm64_macho

def create_ipa_package(base_dir):
    payload_dir = os.path.join(base_dir, "Payload")
    app_dir = os.path.join(payload_dir, "TEST PHUQUY.app")
    
    if os.path.exists(payload_dir):
        shutil.rmtree(payload_dir)
    os.makedirs(app_dir, exist_ok=True)

    # 1. Mach-O Executable with full __LINKEDIT and LC_CODE_SIGNATURE (Fixes Scarlet/ESign signing failure)
    exec_path = os.path.join(app_dir, "TEST PHUQUY")
    create_signable_arm64_macho(exec_path, bundle_id="com.phuquy.testkey")

    # 2. Info.plist with complete CFBundleIcons & device platforms
    src_info = os.path.join(base_dir, "TEST_PHUQUY", "Info.plist")
    dst_info = os.path.join(app_dir, "Info.plist")
    shutil.copy2(src_info, dst_info)

    # 3. PkgInfo
    with open(os.path.join(app_dir, "PkgInfo"), "w") as f:
        f.write("APPL????")

    # 4. Logo and Icons - copy to all standard iOS icon names so Scarlet/ESign displays the logo
    src_logo = os.path.join(base_dir, "logo.png")
    icon_names = [
        "logo.png",
        "icon.png",
        "icon@2x.png",
        "icon_1024.png",
        "AppIcon60x60@2x.png",
        "AppIcon60x60@3x.png",
        "AppIcon76x76@2x~ipad.png",
        "Icon-60@2x.png",
        "Icon-60@3x.png",
        "Icon-72.png",
        "Icon-76.png",
        "Icon-Small.png",
        "Icon-Small@2x.png",
        "Icon-Small@3x.png"
    ]
    if os.path.exists(src_logo):
        for ic in icon_names:
            shutil.copy2(src_logo, os.path.join(app_dir, ic))

    # Also copy all generated xcassets icons
    icon_set_dir = os.path.join(base_dir, "TEST_PHUQUY", "Assets.xcassets", "AppIcon.appiconset")
    if os.path.exists(icon_set_dir):
        for ic in os.listdir(icon_set_dir):
            if ic.endswith(".png"):
                shutil.copy2(os.path.join(icon_set_dir, ic), os.path.join(app_dir, ic))

    # 5. HTML preview resource
    src_html = os.path.join(base_dir, "index.html")
    if os.path.exists(src_html):
        shutil.copy2(src_html, os.path.join(app_dir, "index.html"))

    # 6. Create dcukey.ipa
    ipa_path = os.path.join(base_dir, "dcukey.ipa")
    if os.path.exists(ipa_path):
        os.remove(ipa_path)

    with zipfile.ZipFile(ipa_path, "w", zipfile.ZIP_DEFLATED) as ipa_zip:
        for root, dirs, files in os.walk(payload_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                ipa_zip.write(full_path, rel_path)
    print(f"Created IPA: {ipa_path} ({os.path.getsize(ipa_path)} bytes)")

def create_zip_archive(base_dir):
    zip_path = os.path.join(base_dir, "dcukey.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    ignore_names = {"dcukey.zip", ".git"}
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in ignore_names and not d.startswith(".system")]
            for file in files:
                if file in ignore_names:
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                z.write(full_path, rel_path)
    print(f"Created ZIP: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    base = os.path.abspath("C:/Users/Admin/.gemini/antigravity-ide/scratch/TEST_PHUQUY")
    create_ipa_package(base)
    create_zip_archive(base)
