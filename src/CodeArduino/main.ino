const int dirPin1 = 8;
const int stepPin1 = 9;
const int dirPin2 = 4;
const int stepPin2 = 5;
const int electroimanPin = 7;  // Pin para el electroimán
const int steps = 289;
int stepDelay = 4000;

void setup() {
  Serial.begin(9600); // Inicializa la comunicación serial
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(electroimanPin, OUTPUT); // Configura el pin del electroimán
  digitalWrite(electroimanPin, LOW); // Imán desactivado por defecto
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    // Control del electroimán
    if (comando == 'e') {
      digitalWrite(electroimanPin, HIGH);  // Activa el imán
      Serial.println("Electroimán ACTIVADO");
    }
    if (comando == 'f') {
      digitalWrite(electroimanPin, LOW);   // Desactiva el imán
      Serial.println("Electroimán DESACTIVADO");
    }

    // Motor 1 adelante
    if (comando == 'a') {
      digitalWrite(dirPin1, HIGH);
      for (int x = 0; x < steps; x++) {
        digitalWrite(stepPin1, HIGH);
        delayMicroseconds(stepDelay);
        digitalWrite(stepPin1, LOW);
        delayMicroseconds(stepDelay);
      }
    }
    // Motor 1 atrás
    if (comando == 'd') {
      digitalWrite(dirPin1, LOW);
      for (int x = 0; x < steps; x++) {
        digitalWrite(stepPin1, HIGH);
        delayMicroseconds(stepDelay);
        digitalWrite(stepPin1, LOW);
        delayMicroseconds(stepDelay);
      }
    }
    // Motor 2 adelante
    if (comando == 'w') {
      digitalWrite(dirPin2, HIGH);
      for (int x = 0; x < steps; x++) {
        digitalWrite(stepPin2, HIGH);
        delayMicroseconds(stepDelay);
        digitalWrite(stepPin2, LOW);
        delayMicroseconds(stepDelay);
      }
    }
    // Motor 2 atrás
    if (comando == 's') {
      digitalWrite(dirPin2, LOW);
      for (int x = 0; x < steps; x++) {
        digitalWrite(stepPin2, HIGH);
        delayMicroseconds(stepDelay);
        digitalWrite(stepPin2, LOW);
        delayMicroseconds(stepDelay);
      }
    }
  }
}