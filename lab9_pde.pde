import processing.serial.*;

  // Luke Paltzer - 657837873 - lpaltz2
  // Lab 9 - Graphing sensor data on a PC
  // This displays data from variable resistors 
  // Data is read on an Arduino and graphed using Processing
  // This is a linux mint 18.2 machine.
  // Processing version 3.3.7
  // VSS = 0V -- VDD = 5V
  // Data from pot is read on A0
  // 5V -- PhotoResistor -- 0V
  //              Pin A0 ^ 
  // 5V -- POT -- 0V
  // Pin A1 ^
  // Data is sent in in comma seperated form - photo,pot
  // Values are sent over serial at 9600 baud
  // Values.split(','), map(0,height), and FloatList.append(result)
  // Draw the shape with vertex(i,FloatList[i])
  // When FloatList.size == width --> blank the sketch and FloatList.clear
  // POT = Purple
  // PHOTO = Blue
  // Resources - LAB 5
  // https://learn.sparkfun.com/tutorials/connecting-arduino-to-processing#introduction
  // https://www.arduino.cc/en/Tutorial/Graph
  // https://processing.org/reference/FloatList.html
  // https://processing.org/discourse/beta/num_1217385866.html
  // Pot controls X scale of Photo

Serial my_port;
String input;
String[] data;
FloatList photo, pot;

void setup(){
  size(400, 400);
  background(0);
  photo = new FloatList();
  pot = new FloatList();
  noLoop();
  my_port = new Serial(this, Serial.list()[0], 9600);
}

void draw(){
  background(0); // clear the background for sharper lines
  
  noFill();
  stroke(227, 34, 255); // purple
  strokeWeight(1.0);
  strokeJoin(ROUND);
  beginShape();
  for (int i = 0; i < pot.size(); i++){
    vertex(i, height - pot.get(i));
  }
  endShape();
  
  noFill();
  stroke(127, 134, 255); // blue
  strokeWeight(1.0);
  strokeJoin(ROUND);
  beginShape();
  for (int i = 0; i < photo.size(); i++){
    vertex(i * pot.get((pot.size()-1)) / 50, height - photo.get(i));
  }
  endShape();
  
  if (pot.size() >= width){
    background(0);
    pot.clear();
    photo.clear();
  }
}

void serialEvent (Serial my_port) {
  try{
    if (my_port.available() > 0){
      input = my_port.readStringUntil('\n');
      if (input != null) {
        data = split(input, ',');
        if (!Float.isNaN(float(data[0])))
          photo.append(map(float(data[0]), 0, 1023, 0, height));
        if (!Float.isNaN(float(data[1])))
          pot.append(map(float(data[1]), 0, 1023, 0, height));
        // println(input);
        redraw(); // draw only when updated
      }
    }
  }
  catch (Exception e){ // avoid crashing if serial read is not present or fails
    println("Serial Exception Intercepted");
  }
}
