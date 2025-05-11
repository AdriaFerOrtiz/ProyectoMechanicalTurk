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
**Hardware**:  
- **Raspberry Pi Zero** (Control center) - (Precio y link)
- **Stepper Motors** (NEMA 17 for X/Y axes) - (Precio y link)
- **Electromagnet** (Piece movement) - (Precio y link)
- **Pi Camera Module** (Board detection) - (Precio y link)

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
