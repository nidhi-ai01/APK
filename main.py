import glob
import os
import json
import warnings
from androguard.core.bytecodes.apk import APK

# Suppress deprecation warnings properly
warnings.filterwarnings("ignore", category=DeprecationWarning)

def extract_features(apk_file):
    try:
        # Try loading APK safely
        apk = APK(apk_file)
        
        # Extract features
        features = {
            'app_name': apk.get_app_name(),
            'package_name': apk.get_package(),
            'version_name': apk.get_androidversion_name(),
            'version_code': apk.get_androidversion_code(),
            'min_sdk': apk.get_min_sdk_version(),
            'target_sdk': apk.get_target_sdk_version(),
            'permissions': apk.get_permissions(),
            'main_activity': apk.get_main_activity(),
            'activities': apk.get_activities(),
            'services': apk.get_services(),
            'receivers': apk.get_receivers(),
            'providers': apk.get_providers(),
            'libraries': list(apk.get_libraries()),
        }
        return features
    except Exception as e:
        print(f"❌ Skipping {apk_file}: {e}")
        return None

def save_to_json(data, output_file):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        print(f"✅ Data saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")

if __name__ == "__main__":
    apk_dir = r"C:\Users\CybroNidhi\Documents\Project_IITH\samples\benign"
    output_dir = r"C:\Users\CybroNidhi\Documents\Project_IITH\raw_features"

    for apk_file in glob.glob(os.path.join(apk_dir, "**", "*.apk"), recursive=True):
        file_name, _ = os.path.splitext(os.path.basename(apk_file))
        apk_type = os.path.basename(os.path.dirname(apk_file))
        json_path = os.path.join(output_dir, apk_type, f"{file_name}.json")

        if os.path.exists(apk_file):
            print(f"🔍 Analyzing APK: {apk_file}")
            features = extract_features(apk_file)
            if features:
                save_to_json(features, json_path)
        else:
            print(f"❌ APK not found: {apk_file}")
