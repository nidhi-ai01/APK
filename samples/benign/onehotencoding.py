import pandas as pd
import json

apk_data = {
    "permissions": [
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.ACCESS_WIFI_STATE",
        "android.permission.VIBRATE",
        "com.google.android.c2dm.permission.RECEIVE",
        "android.permission.WAKE_LOCK"
    ],
    "main_activity": "com.hp.marketingreport.AuthenticationActivity",
    "activities": [
        "com.hp.marketingreport.HomeActivity",
        "com.hp.marketingreport.AuthenticationActivity",
        "com.google.firebase.auth.internal.GenericIdpActivity",
        "com.google.firebase.auth.internal.RecaptchaActivity",
        "com.google.android.gms.common.api.GoogleApiActivity"
    ],
    "services": [
        "com.hp.marketingreport.PushNotificationService",
        "com.google.firebase.auth.api.fallback.service.FirebaseAuthFallbackService",
        "com.google.firebase.components.ComponentDiscoveryService",
        "com.google.firebase.messaging.FirebaseMessagingService",
        "com.google.android.datatransport.runtime.backends.TransportBackendDiscovery",
        "com.google.android.datatransport.runtime.scheduling.jobscheduling.JobInfoSchedulerService"
    ],
    "receivers": [
        "com.google.firebase.iid.FirebaseInstanceIdReceiver",
        "com.google.android.datatransport.runtime.scheduling.jobscheduling.AlarmManagerSchedulerBroadcastReceiver"
    ],
    "providers": [
        "com.google.firebase.provider.FirebaseInitProvider",
        "androidx.startup.InitializationProvider"
    ],
    "libraries": [
        "org.apache.http.legacy",
        "androidx.window.extensions",
        "androidx.window.sidecar"
    ]
}

# Convert categorical lists into a structured format
def convert_to_ohe_dict(data):
    ohe_dict = {}

    for category, values in data.items():
        if isinstance(values, list):
            for value in values:
                ohe_dict[f"{category}_{value}"] = 1
        else:
            ohe_dict[category] = values  # Keep non-list values as is

    return ohe_dict

# Apply transformation
encoded_data = convert_to_ohe_dict(apk_data)

# Convert to DataFrame
df = pd.DataFrame([encoded_data]).fillna(0)  # Fill missing values with 0

# Display encoded DataFrame
print(df.head())

# Save to CSV for further processing
df.to_csv("encoded_apk_data.csv", index=False)

apk_info = {
    "app_name": "Marketing Report Admin",
    "package_name": "com.hp.marketingreport",
    "version_name": "1.0",
    "version_code": "1",
    "min_sdk": "24",
    "target_sdk": "32"
}

# Print the dictionary
print(apk_info)


apk_set = set(apk_info.values())

# Print the set
print(apk_set)
