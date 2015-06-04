/* 
 * Move the split flap display to show the data that is received on serial
 */
#define NUMBER_OF_CHARS 2
const int motor_pins[] = {2, 3};
const int full_flip_sensor_pins[] = {9, 10};
const int reset_button_pin = 0;

#define MOTOR_STEPS_PER_LETTER = 12;
char current_chars[NUMBER_OF_CHARS];
const char sign_character_map[] = {
    ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '?', '?', '?', '-', '.', '(', ')', '!', ':', '/', '"', ',', '=', '?', '@'
};


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
  }

  if (Serial.available() >= NUMBER_OF_CHARS) {
    char new_values[NUMBER_OF_CHARS];
    for(int i=0; i < NUMBER_OF_CHARS; i++){
      new_values[i] = Serial.read();
    }
    Serial.println(new_values);
    changeLetters(new_values);
  }

  delay(100);
}

void reset_all() {
  /*
   *  reset the all the letter to the space character
  */ 

  int pin_delay = 5;
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
    change_complete = false;

    for (int i = 0; i < NUMBER_OF_CHARS; i++){
      if (number_of_changes[i] > 0){
        //move the motor one step
        change_complete = true;
        digitalWrite(motor_pins[i], HIGH);
      }
    }
    delay(100); // this is too long
    for (int i = 0; i < NUMBER_OF_CHARS; i++){
      if (number_of_changes[i] > 0){
        //move the motor one step
        digitalWrite(motor_pins[i], LOW);
      }
    }

    // reset the number of changes remaining
    if (num_steps == 4) {
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


// @TODO: test: HOW MANY TIMES DOES THIS EXECUTE?
// @TODO: test: HOW LONG DOES THIS TAKE?
int getNumberForLetter(char letter){
  /*
   * Find the number that corresponds to a particular character in the split flap
   */
   
  // XXX: is there a faster way to do this?
  for(int i = 0; i < sizeof(sign_character_map); i++){
    if (sign_character_map[i] == letter){
      return i;
    }
  }
  return 0;
}
