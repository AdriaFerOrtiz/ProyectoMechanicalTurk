# MechanicalTurk  
*A modern robotic chess player inspired by the historical "Mechanical Turk," combining computer vision, cloud-based AI, and precision robotics to play chess autonomously.*  

---

## 🎯 Project Description  
**MechanicalTurk-ChessRobot** is an autonomous chess-playing robot that bridges physical and digital gameplay. It uses a **cartesian robotic system** to move pieces on a physical board, guided by:  
- **Computer Vision**: Detects piece positions via a camera.  
- **Cloud AI**: Leverages Stockfish or Leela Chess Zero for move calculations.  
- **Precision Robotics**: Moves pieces magnetically from beneath the board.  

**Key Features**:  
- Plays against humans or acts as a physical proxy for online games.  
- Handles edge cases like **obstacle avoidance** (e.g., moving blocking pieces temporarily).  
- **Web interface** to play remotely (like Chess.com but with a real robot).  

**Example Scenario**:  
> A user makes a move on the physical board → The robot’s camera captures the move → Cloud AI calculates the best response → The robot moves a piece with sub-millimeter precision.  

---

## 📽️ Demo  

---

## 📖 Table of Contents  
1. [Components](#-components)  
2. [Hardware Design](#-hardware-design)  
3. [Software Architecture](#-software-architecture)  
   - [Core Modules](#core-modules)  
   - [Cloud Integration](#cloud-integration)  
4. [Contributions](#-amazing-contributions)  
5. [Authors](#-authors)  

---

## 🔧 Components  
| Componente                                        | Imagen                                                                 | Enlace                                                                 |
|--------------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Motor NEMA 17 / 3.5 Kg**                        | ![NEMA17](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/NEMA17.jpg) | [Bricogeek](https://tienda.bricogeek.com/motores-paso-a-paso/1360-motor-nema-17-35kg-con-conector-y-cable.html) |
| **Arduino Uno**                                  | ![Arduino Uno](https://upload.wikimedia.org/wikipedia/commons/3/38/Arduino_Uno_-_R3.jpg) | [Arduino.cc](https://store.arduino.cc/products/arduino-uno-rev3)      |
| **Driver A4988**                                  | ![A4988](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Driver.jpg) | [Pololu](https://www.pololu.com/product/1182)                        |
| **Electroimán 12 V / 100 N**                      | ![12V Electroimán](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Iman.jpg) | [todoelectronica relé 5VDC de 1 Canal (10A)](https://www.todoelectronica.com/modulo-rele-5vdc-de-1-canal-10a-para-arduino-p-110226.html?srsltid=AfmBOoo3lXE0UYiJQ3rck6Ui3YCa-USp1VEkin8u6RmBwkzYa254TDCxwr0)  |
| **Relé 5 V 10 A**                                 | ![Relé 5V 10A](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Rele.jpg) | [Amazon 5 V 10 A Relay Module](https://www.amazon.com/10A-Channel-Relay-Module-Arduino/dp/B07Z432CS3) :contentReference[oaicite:2]{index=2} |


**Software**:  
- **Google Cloud Vision** (Computer vision)  
- **Stockfish 16** (Chess engine)  
- **FastAPI** (Web interface backend)  

---

## 🛠️ Hardware Design  
*Cartesian robot design with labeled axes and component placements.*  

---

## 🖥️ Software Architecture  
### Core Modules  
![Module Diagram](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Arquitectura_Software_Completa.png)  
- **`VisionModule`**: Processes board images (local or cloud).  
- **`IAModule`**: Calculates moves using Stockfish API.  
- **`ControlRobot`**: Converts UCI moves to motor commands.  

### Cloud Integration  
- **Computer Vision**: Images are sent to Google Cloud for piece detection.  
- **AI Moves**: Stockfish runs on Cloud Run for scalable computation.  
- **Sync**: Firebase stores game states for remote play.  

---

## ✨ Amazing Contributions  
- **Obstacle Avoidance**: The robot plans alternative paths if pieces block movement.  
- **Low-Cost Precision**: Achieves sub-millimeter accuracy with budget stepper motors.  
- **Social Impact**: Makes chess accessible for visually impaired players via physical interaction.  

---

## 👥 Authors  
- Eduard José García Mendeleac
- Adrià Fernández Ortiz
- Luis Adrián Gómez Batista
