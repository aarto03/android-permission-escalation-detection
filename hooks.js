console.log("[*] Frida script loaded and surveillance active...");
Java.perform(function () {
    var TelephonyManager = Java.use('android.telephony.TelephonyManager');
    TelephonyManager.getDeviceId.overload().implementation = function () {
        console.log("\n[!] ALERT: Permission Goldmining Detected!");
        console.log("[!] ALERT: App is requesting Device ID (IMEI)");
        console.log("[!] This permission was NOT found in the Static Baseline JSON.");
        return this.getDeviceId();
    };

    var LocationManager = Java.use('android.location.LocationManager');
    LocationManager.requestLocationUpdates.overload(
            'java.lang.String', 'long', 'float', 'android.location.LocationListener'
    ).implementation = function (provider, minTime, minDistance, listener) {
        console.log("[!] ALERT: App is requesting location via: " + provider);
        return this.requestLocationUpdates(provider, minTime, minDistance, listener);
    };
});

Java.perform(function () {
    var SQLiteDatabase = Java.use('android.database.sqlite.SQLiteDatabase');
    SQLiteDatabase.openDatabase.overload('java.lang.String', 'android.database.sqlite.SQLiteDatabase$CursorFactory', 'int').implementation = function (path, factory, flags) {
        console.log("[+] Intercepted Database Open: " + path);
        return this.openDatabase(path, factory, flags);
    };
});

Java.perform(function () {
    var SQLiteDatabase = Java.use('android.database.sqlite.SQLiteDatabase');
    
    // Hooking the openDatabase method
    SQLiteDatabase.openDatabase.overload('java.lang.String', 'android.database.sqlite.SQLiteDatabase$CursorFactory', 'int').implementation = function (path, factory, flags) {
        console.log("[+] Activity Detected: Opening Database at " + path);
        return this.openDatabase(path, factory, flags);
    };
});

Java.perform(function() {
    const classToHook = 'com.example.comnononsenseappssecuritytest.VulnerableService';

    var hookStarted = false;
    
    function tryHook() {
        if (hookStarted) return;
        
        try {
            var VulnerableService = Java.use(classToHook);
            VulnerableService.onStartCommand.implementation = function (intent, flags, startId) {
                console.log("\n[!] SECURITY ALERT: Exported Component Entry Detected!");
                console.log("[!] External source triggered .VulnerableService via Intent.");
                return this.onStartCommand(intent, flags, startId);
            };
            console.log("[+] Successfully hooked VulnerableService!");
            hookStarted = true;
        } catch (e) {
        }
    }

    tryHook();

    setInterval(tryHook, 500);
});