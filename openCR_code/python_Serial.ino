#include <Dynamixel2Arduino.h>
#include <IMU.h>
#define ARDUINO_OpenCR

#define DXL_SERIAL   Serial3
#define DEBUG_SERIAL Serial
const int DXL_DIR_PIN = 84; // OpenCR Board's DIR PIN.

const uint8_t LEFT_MOTOR_ID = 1;
const uint8_t RIGHT_MOTOR_ID = 2;
const float DXL_PROTOCOL_VERSION = 2.0;

Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);
cIMU IMU;

using namespace ControlTableItem;

void setup() {
  DEBUG_SERIAL.begin(115200);
  while(!DEBUG_SERIAL);

  Serial.begin(115200);
  while(!Serial);

  dxl.begin(1000000);
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  dxl.ping(LEFT_MOTOR_ID);
  dxl.ping(RIGHT_MOTOR_ID);

  dxl.torqueOff(LEFT_MOTOR_ID);
  dxl.torqueOff(RIGHT_MOTOR_ID);
  dxl.setOperatingMode(LEFT_MOTOR_ID, OP_VELOCITY);
  dxl.setOperatingMode(RIGHT_MOTOR_ID, OP_VELOCITY);
  dxl.torqueOn(LEFT_MOTOR_ID);
  dxl.torqueOn(RIGHT_MOTOR_ID);

  IMU.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    handleCommand(command);
  }

  // Update the IMU in the loop
  IMU.update();
}

void handleCommand(String command) {
  if (command.startsWith("SET_VELOCITY_LEFT ")) {
    float velocity = command.substring(18).toFloat();
    dxl.setGoalVelocity(LEFT_MOTOR_ID, velocity);
  } else if (command.startsWith("SET_VELOCITY_RIGHT ")) {
    float velocity = command.substring(19).toFloat();
    dxl.setGoalVelocity(RIGHT_MOTOR_ID, velocity);
  } else if (command.startsWith("READ_SENSOR ")) {
    int sensorID = command.substring(12).toInt();
    int position = dxl.getPresentPosition(sensorID);
    Serial.println(position);
  } else if (command.startsWith("READ_IMU_ACC")) {
    Serial.print(IMU.accRaw[0]);    // ACC X
    Serial.print(" \t");
    Serial.print(IMU.accRaw[1]);    // ACC Y
    Serial.print(" \t");
    Serial.print(IMU.accRaw[2]);    // ACC Z
    Serial.println();
  } else if (command.startsWith("READ_IMU_GYRO")) {
    Serial.print(IMU.gyroRaw[0]);    // GYRO X
    Serial.print(" \t");
    Serial.print(IMU.gyroRaw[1]);    // GYRO Y
    Serial.print(" \t");
    Serial.print(IMU.gyroRaw[2]);    // GYRO Z
    Serial.println();
  } else if (command.startsWith("READ_IMU_RPY")) {
    Serial.print(IMU.rpy[0]);    // Roll
    Serial.print(" \t");
    Serial.print(IMU.rpy[1]);    // Pitch
    Serial.print(" \t");
    Serial.print(IMU.rpy[2]);    // Yaw
    Serial.println();
  }
}