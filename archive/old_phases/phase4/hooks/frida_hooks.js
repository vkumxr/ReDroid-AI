Java.perform(function () {

  const SmsManager = Java.use("android.telephony.SmsManager");

  SmsManager.sendTextMessage.overload(
    'java.lang.String',
    'java.lang.String',
    'java.lang.String',
    'android.app.PendingIntent',
    'android.app.PendingIntent'
  ).implementation = function (dest, sc, text, sent, delivered) {
    console.log("[DYNAMIC] SMS sent to:", dest);
    console.log("[DYNAMIC] Message:", text);
    return this.sendTextMessage(dest, sc, text, sent, delivered);
  };

  const URL = Java.use("java.net.URL");
  URL.$init.overload('java.lang.String').implementation = function (url) {
    console.log("[DYNAMIC] Network URL:", url);
    return this.$init(url);
  };

});