import os
import json
import glob
import warnings
from androguard.core.bytecodes.apk import APK

# Suppress Deprecation Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def extract_features(apk_file):
    try:
        apk = APK(apk_file)
        features = {
            "app_name": apk.get_app_name(),
            "package_name": apk.get_package(),
            "version_name": apk.get_androidversion_name(),
            "version_code": apk.get_androidversion_code(),
            "min_sdk": apk.get_min_sdk_version(),
            "target_sdk": apk.get_target_sdk_version(),
            "permissions": apk.get_permissions(),
            "main_activity": apk.get_main_activity(),
            "activities": apk.get_activities(),
            "services": apk.get_services(),
            "receivers": apk.get_receivers(),
            "providers": apk.get_providers(),
            "libraries": list(apk.get_libraries()),
        }
        return features
    except Exception as e:
        print(f"❌ Failed to analyze {apk_file}: {e}")
        return None

def save_json(data, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Saved: {output_path}")
    except Exception as e:
        print(f"❌ Failed to save JSON: {e}")

def main():
    apk_folder = r"C:\Users\CybroNidhi\Documents\Project_IITH\samples\benign"
    output_folder = r"C:\Users\CybroNidhi\Documents\Project_IITH\23_jsons"

    apk_files = glob.glob(os.path.join(apk_folder, "*.apk"))

    print(f"🔎 Found {len(apk_files)} APK files.")

    for apk_path in apk_files:
        file_name = os.path.splitext(os.path.basename(apk_path))[0]
        json_file = os.path.join(output_folder, f"{file_name}.json")
        print(f"📦 Processing: {file_name}.apk")

        features = extract_features(apk_path)
        if features:
            save_json(features, json_file)

if __name__ == "__main__":
    main()
