import os
import json
import csv
from androguard.misc import AnalyzeAPK

def analyze_apk(apk_path):
    """
    Analyze the APK file and extract permissions and intents.
    """
    apk_info, _, _ = AnalyzeAPK(apk_path)
    permissions = apk_info.get_permissions() or []
    intents = {}
    
    # Extract intent filters for each activity
    for activity in apk_info.get_activities():
        intent_filters = {
            "actions": apk_info.get_intent_filters(activity, "action") or [],
            "categories": apk_info.get_intent_filters(activity, "category") or [],
            "data": apk_info.get_intent_filters(activity, "data") or [],
        }
        intents[activity] = intent_filters
    
    return permissions, intents

def process_apk(apk_path):
    """
    Process the APK file and return analyzed data.
    """
    permissions, intents = analyze_apk(apk_path)
    analyze_data = {
        "APK": apk_path,
        "Permissions": permissions,
        "Intents": intents
    }
    return analyze_data

def save_to_csv(data, output_file):
    """
    Save the analyzed data to a CSV file.
    """
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["APK", "Permissions", "Intents"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Format intents for CSV
        intents_str = ';'.join([
            f"{component}:Actions:{','.join(intent['actions']) if intent['actions'] else 'None'},"
            f"Categories:{','.join(intent['categories']) if intent['categories'] else 'None'},"
            f"Data:{','.join(intent['data']) if intent['data'] else 'None'}"
            for component, intent in data['Intents'].items()
        ])
        
        writer.writerow({
            "APK": data['APK'],
            "Permissions": ','.join(data['Permissions']) if data['Permissions'] else 'None',
            "Intents": intents_str
        })

def save_to_json(data, output_file):
    """
    Save the analyzed data to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Define the APK file name and paths
    apk_file = "report.apk"
    csv_path = "report.csv"
    json_path = "report.json"
    
    # Check if the APK file exists
    if os.path.exists(apk_file):
        print(f"Analyzing APK file: {apk_file}")
        
        # Process the APK file
        analyzed_data = process_apk(apk_file)
        
        # Save the analyzed data to CSV and JSON
        save_to_csv(analyzed_data, csv_path)
        save_to_json(analyzed_data, json_path)
        
        print(f"Data saved successfully to {csv_path} and {json_path}")
    else:
        print(f"Error: APK file not found at {apk_file}")