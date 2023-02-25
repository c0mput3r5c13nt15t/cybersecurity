// open-terminal.ino
// This script opens a terminal on MacOs and executes a simple command (for german keyboard layout)

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
  // Open the terminal
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
