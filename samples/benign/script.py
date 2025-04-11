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
import glob

def flatten_features(features):
    """
    Convert lists and dictionaries into JSON strings for CSV compatibility.
    """
    flat = {}
    for key, value in features.items():
        if isinstance(value, (list, dict)):
            flat[key] = json.dumps(value, ensure_ascii=False)
        else:
            flat[key] = value
    return flat

def convert_json_to_individual_csv(json_dir, output_dir):
    """
    Convert each JSON file in the directory into an individual CSV file.
    """
    for json_file in glob.glob(os.path.join(json_dir, "**", "*.json"), recursive=True):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                flat_data = flatten_features(data)

            # Build CSV path
            rel_path = os.path.relpath(json_file, json_dir)
            csv_file = os.path.splitext(rel_path)[0] + ".csv"
            csv_output_path = os.path.join(output_dir, csv_file)
            os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)

            # Write to CSV
            with open(csv_output_path, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=flat_data.keys())
                writer.writeheader()
                writer.writerow(flat_data)

            print(f"✅ CSV saved: {csv_output_path}")
        
        except Exception as e:
            print(f"❌ Error processing {json_file}: {e}")

# Example usage
if __name__ == "__main__":
    json_dir = r"C:\Users\CybroNidhi\Documents\Project_IITH\raw_features"
    output_dir = r"C:\Users\CybroNidhi\Documents\Project_IITH\csv_features"
    convert_json_to_individual_csv(json_dir, output_dir)

