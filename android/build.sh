#!/bin/bash
# Build the veniz shop APK without Gradle (aapt + javac + d8 + apksigner).
set -e

BASE=/home/z/my-project/scripts/veniz-android
SDK=/home/z/my-project/scripts/android-sdk
JDK=/home/z/my-project/scripts/jdk
export JAVA_HOME=$JDK
export PATH=$JDK/bin:$PATH

BT=$SDK/build-tools/34.0.0
PLAT=$SDK/platforms/android-34/android.jar

cd "$BASE"

echo "== 0. assets =="
mkdir -p assets
cp -f /home/z/my-project/download/veniz-shop.html assets/index.html
ls -la assets/

echo "== 1. generate R.java =="
rm -rf gen classes build
mkdir -p gen classes build
"$BT/aapt" package -f -m -M AndroidManifest.xml -S res -I "$PLAT" -J gen

echo "== 2. javac =="
javac --release 8 -classpath "$PLAT" -d classes \
    gen/com/veniz/shop/R.java src/com/veniz/shop/MainActivity.java

echo "== 3. d8 (dex) =="
"$BT/d8" --release --lib "$PLAT" --min-api 21 --output build \
    classes/com/veniz/shop/*.class

echo "== 4. package resources + assets =="
"$BT/aapt" package -f -M AndroidManifest.xml -S res -A assets -I "$PLAT" \
    -F build/unsigned.apk

echo "== 5. add classes.dex =="
( cd build && "$BT/aapt" add unsigned.apk classes.dex )

echo "== 6. zipalign =="
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk

echo "== 7. keystore =="
[ -f veniz.keystore ] || keytool -genkeypair -keystore veniz.keystore \
    -alias veniz -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass veniz1404 -keypass veniz1404 \
    -dname "CN=veniz-shop, OU=shop, O=veniz, L=Tehran, C=IR"

echo "== 8. sign =="
"$BT/apksigner" sign --ks veniz.keystore --ks-pass pass:veniz1404 \
    --key-pass pass:veniz1404 --out veniz-shop.apk build/aligned.apk

echo "== 9. verify =="
"$BT/apksigner" verify --print-certs veniz-shop.apk
ls -la veniz-shop.apk
echo "BUILD-OK"
