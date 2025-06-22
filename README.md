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
| **Motor NEMA 17 / 3.5Kg**                        | ![Motor](./path/to/fe5c3b23-cea6-45c7-a9ad-f711a1c5e8ca.png)           | [Bricogeek](https://tienda.bricogeek.com/motores-paso-a-paso/1360-motor-nema-17-35kg-con-conector-y-cable.html) |
| **Arduino Uno**                                  | ![Arduino Uno](https://upload.wikimedia.org/wikipedia/commons/3/38/Arduino_Uno_-_R3.jpg) | [Arduino.cc](https://store.arduino.cc/products/arduino-uno-rev3)      |
| **Driver A4988 (Controlador de motor paso a paso)** | ![A4988](https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/A4988_stepper_motor_driver.jpg/320px-A4988_stepper_motor_driver.jpg) | [Pololu](https://www.pololu.com/product/1182) |
| **Electroimán 12V (OcioDual)**                   | *(Imagen no disponible)*                                               | *(Agregar enlace si se dispone)*                                      |
| **Relé 5V 10A (para controlar electroimán)**     | *(Imagen no disponible)*                                               | *(Agregar enlace si se dispone)*                                      |
| **Cámara OV5647 1080p**                          | ![Cámara](./path/to/6058a319-a7b1-4d6f-acd9-45edbf7381c6.png)           | [Bricogeek](https://tienda.bricogeek.com/accesorios-raspberry-pi/1472-camara-5mp-ov5647-1080p-para-raspberry-pi-zero.html) |


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
