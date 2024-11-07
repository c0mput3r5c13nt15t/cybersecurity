// open-terminal.ino
// This script opens a terminal on Linux and executes a simple command (for german keyboard layout)

// Import libraries
#include <Keyboard.h>
#include <Keyboard_de_DE.h>

void setup()
{
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
  Keyboard.print("echo 'You have been pawned'");
  Keyboard.press(KEY_RETURN);
  delay(10);
  Keyboard.releaseAll();
  Keyboard.end();
}
void loop() {}
