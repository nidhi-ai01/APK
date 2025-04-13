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
import os
import json
import csv

# Path to folder containing your JSON files
folder_path = r"C:\Users\CybroNidhi\Documents\Project_IITH\23_jsons"
print(type(folder_path))

# Get all JSON files in the folder
json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# This will hold all flattened records
all_data = []

for file in json_files:
    file_path = os.path.join(folder_path, file)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # Flatten lists to semicolon-separated strings
        flat_data = {k: '; '.join(v) if isinstance(v, list) else v for k, v in data.items()}
        all_data.append(flat_data)

# Determine fieldnames from the first file
fieldnames = all_data[0].keys()

# Write all data to a single CSV
csv_file = os.path.join(folder_path, "combined_apk_info.csv")
with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
    writer = csv.DictWriter(cf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print(f"✅ Combined CSV saved as: {csv_file}")
