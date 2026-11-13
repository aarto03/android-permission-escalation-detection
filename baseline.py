from androguard.core.apk import APK
import json


def generate_baseline(apk_path):
    print(f"[*] Analyzing: {apk_path}")
    try:
        app = APK(apk_path)

        package_name = app.get_package()
        permissions = app.get_permissions()


        activities = app.get_activities()
        services = app.get_services()
        receivers = app.get_receivers()
        providers = app.get_providers()

        baseline = {
            "package": package_name,
            "declared_permissions": permissions,
            "attack_surface": {
                "activities": activities,
                "services": services,
                "receivers": receivers,
                "providers": providers
            }
        }

        output_name = f"{package_name}_baseline.json"
        with open(output_name, "w") as f:
            json.dump(baseline, f, indent=4)

        print(f"\n[+] SUCCESS: Baseline saved to {output_name}")
        print(f"[+] Found {len(permissions)} Declared Permissions")
        print(f"[+] Found {len(activities)} Activities and {len(services)} Services")

    except Exception as e:
        print(f"[-] Error: {str(e)}")


if __name__ == "__main__":
    generate_baseline("testapp.apk")