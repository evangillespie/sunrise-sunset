/* 
 * Move the split flap display to show the data that is received on serial
 */
#define NUMBER_OF_CHARS 25
const int motor_pins[] = {3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53};
const int full_flip_sensor_pins[] = {2, 4, 6, 8, 10, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52};
const int reset_button_pin = 13;

#define MOTOR_STEPS_PER_LETTER = 12;
char current_chars[NUMBER_OF_CHARS];
char new_values[NUMBER_OF_CHARS];
const char sign_character_map[] = {
    ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '?', '?', '?', '-', '.', '(', ')', '!', ':', '/', '"', ',', '=', '?', '@'
};
int pin_delay = 4;


void setup() {
  //set pin modes
  pinMode(reset_button_pin, INPUT);

  for(int i=0; i < NUMBER_OF_CHARS; i++) {
    pinMode(motor_pins[i], OUTPUT);  // stepper motor step pin
    pinMode(full_flip_sensor_pins[i], INPUT); // large ring sensor
    digitalWrite(motor_pins[i], LOW);  //initialiaze
  }
 
  Serial.begin(9600);
  delay(500);

  reset_all();
}

void loop() {
  if (digitalRead(reset_button_pin) == HIGH) {
    reset_all();
    // clear the incoming serial buffer
    while(Serial.available()){
      Serial.read();
    }
  }

  if (Serial.available() >= NUMBER_OF_CHARS) {
    for(int i=0; i < NUMBER_OF_CHARS; i++){
      new_values[i] = Serial.read();
    }
    if (is_blank(new_values) == true){
      reset_all();
    } else {
      changeLetters(new_values);
    }
  }

  delay(100);
}


void reset_all() {
  /*
   *  reset all the letters to the space character
  */

  int sensor_counter = 0;

  // move all characters off the space char
  do{
    sensor_counter = 0;
    for(int i=0; i < NUMBER_OF_CHARS; i++){
      if (digitalRead(full_flip_sensor_pins[i]) == LOW){
        sensor_counter++;
        digitalWrite(motor_pins[i], HIGH);
      }
    }
    delay(pin_delay);
    for(int i=0; i < NUMBER_OF_CHARS; i++){
      digitalWrite(motor_pins[i], LOW);
    }
    delay(pin_delay);
  } while (sensor_counter > 0);


  // spin all characters around until you get to the space
  while (sensor_counter < NUMBER_OF_CHARS){
    sensor_counter = 0;
    for(int i=0; i < NUMBER_OF_CHARS; i++){
      if (digitalRead(full_flip_sensor_pins[i]) == LOW){
        sensor_counter++;
      } else {
        digitalWrite(motor_pins[i], HIGH);
      }
    }
    delay(pin_delay);
    for(int i=0; i < NUMBER_OF_CHARS; i++){
      digitalWrite(motor_pins[i], LOW);
    }
    delay(pin_delay);
  }

  // reset the current chars array
  for (int i = 0; i < NUMBER_OF_CHARS; i++){
    current_chars[i] = ' ';
  }
}


bool is_blank(char string[]){
  /*
   * Return true if the char array is all spaces
   */
   for (int i = 0; i < NUMBER_OF_CHARS; i++){
      if (string[i] != ' '){
        return false;
      }
   }
   return true;
}


void changeLetters(char new_values[]){
  /*
   * change all characters to new values
   */

  int number_of_changes[NUMBER_OF_CHARS];
  for(int i = 0; i < NUMBER_OF_CHARS; i++){
    number_of_changes[i] = getNumLetterChanges(current_chars[i], new_values[i]);
  }

  int num_steps = 0;
  bool change_complete = false;
  while (change_complete == false) {
    num_steps += 1;
    change_complete = true;

    for (int i = 0; i < NUMBER_OF_CHARS; i++){
      if (number_of_changes[i] > 0){
        //move the motor one step
        change_complete = false;
        digitalWrite(motor_pins[i], HIGH);
      }
    }
    delay(pin_delay);
    for (int i = 0; i < NUMBER_OF_CHARS; i++){
      if (number_of_changes[i] > 0){
        //move the motor one step
        digitalWrite(motor_pins[i], LOW);
      }
    }
    delay(pin_delay);

    // reset the number of changes remaining
    if (num_steps % 12 == 0) {
      for (int i = 0; i < NUMBER_OF_CHARS; i++){
        if (number_of_changes[i] > 0){
          number_of_changes[i] -= 1;
        }
      }
    }
  }

  for(int i = 0; i < NUMBER_OF_CHARS; i++){
    current_chars[i] = new_values[i];
  }
}


int getNumLetterChanges(char src_letter, char dst_letter) {
  /*
   * get the number of flaps that must fall to get from the srd_letter
   * to the dst_letter
   *
   */
   int src_letter_num = getNumberForLetter(src_letter);
   int dst_letter_num = getNumberForLetter(dst_letter);

   if (src_letter_num == dst_letter_num) {
     return 0;
   } else if (src_letter_num < dst_letter_num){
     return dst_letter_num - src_letter_num;
   } else {
     return dst_letter_num - src_letter_num + sizeof(sign_character_map); 
   }
}


int getNumberForLetter(char letter){
  /*
   * Find the number that corresponds to a particular character in the split flap
   */
  for(int i = 0; i < sizeof(sign_character_map); i++){
    if (sign_character_map[i] == letter){
      return i;
    }
  }

  return 0;
}
