#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9           // Configurable, see typical pin layout above
#define SS_PIN          10          // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
MFRC522::MIFARE_Key key;


const byte BUF_SIZE = 18;
byte buffer[BUF_SIZE];

void setup() {
    Serial.begin(9600); // Initialize serial communications with the PC
    while (!Serial);  // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

    SPI.begin();        // Init SPI bus
    mfrc522.PCD_Init(); // Init MFRC522 card

    // Prepare the key (used both as key A and as key B)
    // using FFFFFFFFFFFFh which is the default at chip delivery from the factory
    for (byte i = 0; i < 6; i++) {
        key.keyByte[i] = 0xFF;
    }

    zeroBuf(buffer, BUF_SIZE);
}

void loop() {
    pingpong();

    zeroBuf(buffer, BUF_SIZE);
    cleanSerial();

    if (!mfrc522.PICC_IsNewCardPresent())
        return;
    if (!mfrc522.PICC_ReadCardSerial())
        return;
    MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
    if(!checkCompat(piccType))
        return;
 
    byte sector         = 1;
    byte blockAddr      = 4;
    byte trailerBlock   = 7;
    MFRC522::StatusCode status;

    // Authenticate using key A
    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        return;
    }

    //read buffer
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(blockAddr, buffer, &BUF_SIZE);
    if (status != MFRC522::STATUS_OK) {
        return;
    }
    send_bytes(buffer, 16);

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
    return;

}









void pingpong(){
    byte idx = 0; 
    while(1){
        int readByte = 0; 
        while( (readByte=Serial.read()) >= 0){
            buffer[idx] = (byte)readByte;
            idx = (idx+1) % BUF_SIZE;
        }
        if(bufContains(buffer, (byte*)"FIS", BUF_SIZE, 3)){
            send_str((byte*)"BADGE");
            return;
        }
    }
}





bool checkCompat(MFRC522::PICC_Type piccType){
   if (     piccType != MFRC522::PICC_TYPE_MIFARE_MINI
        &&  piccType != MFRC522::PICC_TYPE_MIFARE_1K
        &&  piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
        return false;
    }
   return true;
}


void send_str(byte* s){
  byte len = strlen((const char*)s);
  send_bytes(s, len);
}

void send_bytes(byte *buffer, byte size){
    for (byte i = 0; i < size; i++) {
        Serial.print((char)(buffer[i]));
    }
    Serial.flush();
}

bool bufContains(byte* stack, byte* needle, byte stackSize, byte needleSize){
    for(byte i=0; i<stackSize-(needleSize-1); i++){
        boolean contains = true;
        for(byte j=0; j<needleSize; j++){
            contains = contains && stack[i+j] == needle[j];  
        }
        if(contains){
            return true;
        }
    }
    return false;
}

bool cmpBuf(byte* a, byte* b, byte size){
    for(int i=0; i< size; i++){
      if(a[i] != b[i]){
          return false;
      }
    }
    return true;
}

void zeroBuf(byte* buf, byte size){
    for(int i=0; i<size; i++){
      buf[i] = 0x00;
    }
}
void cleanSerial(){
  while(Serial.available()>0){
    Serial.read();
  }
}


