import json

def run_comparison(baseline_file, frida_log):
    with open(baseline_file, 'r') as f:
        static_data = json.load(f)
    
    declared_perms = static_data.get("declared_permissions", [])
    package_name = static_data.get("package", "Unknown")

    with open(frida_log, 'r') as f:
        logs = f.read()

    print(f"\n" + "="*50)
    print(f"AUTOMATED SECURITY AUDIT: {package_name}")
    print("="*50)

    goldmining_attempts = logs.count("Permission Goldmining Detected")
    deputy_attempts = logs.count("Exported Component Entry Detected")
    
    if goldmining_attempts > 0:
        has_permission = any(p in declared_perms for p in [
            "android.permission.READ_PHONE_STATE", 
            "android.permission.READ_PRIVILEGED_PHONE_STATE"
        ])
        
        if not has_permission:
            print(f"[!] CRITICAL: {goldmining_attempts} Goldmining attempt(s) detected!")
            print("    -> App accessed Device ID (IMEI) without Manifest declaration.")

    if deputy_attempts > 0:
        print(f"[!] WARNING: {deputy_attempts} Confused Deputy event(s) detected!")
        print("    -> Exported service was successfully triggered externally.")

    total_violations = goldmining_attempts + deputy_attempts
    risk_level = "LOW"
    if total_violations > 0: risk_level = "MEDIUM"
    if goldmining_attempts > 0: risk_level = "CRITICAL" # Goldmining is usually a higher tier risk

    print("-" * 50)
    print(f"TOTAL VIOLATIONS: {total_violations}")
    print(f"FINAL RISK RATING: {risk_level}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_comparison("com.example.comnononsenseappssecuritytest_baseline.json", "frida_log.txt")