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
> A user makes a move on the physical board → The robot’s camera captures the move → Cloud AI calculates the best response → The robot moves the piece by performing the movement intended by the AI.  

---

## 📽️ Demo  

---

## 📖 Table of Contents  
1. [Components](#-components)  
2. [Hardware Design](#-hardware-design)  
3. [Software Architecture](#-software-architecture)  
   - [Core Modules](#core-modules)  
   - [Cloud Integration](#cloud-integration)
4. [3D components](#-3d-components)  
5. [Contributions](#-amazing-contributions)  
6. [Authors](#-authors)  

---
## ⚡ Electrical Wiring Diagram

The following diagram illustrates the complete wiring of the robot's electronic components, including the Arduino, stepper drivers, relays, power supply, and camera system:

![Wiring Diagram](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/mechanicalTurk_bb.png)

## 🔧 Components  
| Componente                                        | Imagen                                                                 | Enlace                                                                 |
|--------------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Motor NEMA 17 / 3.5 Kg**                        | ![NEMA17](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/NEMA17.jpg) | [Bricogeek](https://tienda.bricogeek.com/motores-paso-a-paso/1360-motor-nema-17-35kg-con-conector-y-cable.html) |
| **Arduino Uno**                                  | ![Arduino Uno](https://upload.wikimedia.org/wikipedia/commons/3/38/Arduino_Uno_-_R3.jpg) | [Arduino.cc](https://store.arduino.cc/products/arduino-uno-rev3)      |
| **Driver A4988**                                  | ![A4988](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Driver.jpg) | [Pololu](https://www.pololu.com/product/1182)                        |
| **Electroimán 12 V / 100 N**                      | ![12V Electroimán](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Iman.jpg) | [TodoElectrónica](https://www.todoelectronica.com/modulo-rele-5vdc-de-1-canal-10a-para-arduino-p-110226.html?srsltid=AfmBOoo3lXE0UYiJQ3rck6Ui3YCa-USp1VEkin8u6RmBwkzYa254TDCxwr0)  |
| **Relé 5 V 10 A**                                 | ![Relé 5V 10A](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Rele.jpg) | [Amazon](https://www.amazon.com/10A-Channel-Relay-Module-Arduino/dp/B07Z432CS3) |
| **Webcam USB Genérica (720p/1080p)**             | ![Webcam Genérica](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/webcam.jpg) | [Amazon – Webcam USB 1080p con micrófono](https://www.amazon.com/-/es/Webcam-Computadora-Micrófono-Resolución-Streaming/dp/B08HRPDYTP) |
| **ATX 500W Power Supply**                         | ![ATX PSU](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/PS.jpg) | [PCComponentes (similar)](https://www.pccomponentes.com/fuentes-de-alimentacion) |
| **456 Point Breadboard**                          | ![ProtoBoard](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/PB.jpg) | [Amazon](https://www.amazon.com/EL-CP-003-Breadboard-Distribution-Solderless-Prototyping/dp/B01EV6LJ7G) |

**Software**:  
- **Google Cloud Vision** (Computer vision)  
- **Stockfish 16** (Chess engine)  
- **FastAPI** (Web interface backend)  

---

## 🛠️ Hardware Design  
*Cartesian robot design with labeled axes and component placements.*  

---

# 🖥️ Software Architecture  

## ☁️ 1. Cloud Infrastructure (Google Cloud)

This project leverages **Google Cloud Platform (GCP)** to handle compute-intensive tasks such as board recognition and AI move generation. The cloud infrastructure is composed of two key services:

#### 🔍 Cloud Function: Board Recognition

A **Cloud Function** receives chessboard images captured via webcam or uploaded through the web interface. These images are processed using a trained machine learning model (TensorFlow or PyTorch), and the function returns a board state encoded as an 8x8 matrix in FEN-like notation.

* **Input:** JPEG or PNG image of the board
* **Output:** JSON object containing the current board state

#### ♟️ Cloud Run: Stockfish

A **Cloud Run** container hosts a persistent instance of the **Stockfish chess engine**. It takes the current board state and returns:

* The best move according to Stockfish (UCI notation)
* The evaluation score of the position (e.g., `+0.8`, `Mate in 2`)

#### 🌐 Web-to-Cloud Communication

The frontend web app communicates with these cloud services:

* Image uploads → sent to the Vision Cloud Function
* Board state → sent to the Stockfish Cloud Run service

#### 🖥️ Web Interface Overview

The web application acts as the **central control panel** for the system. It provides:

* Upload and processing of board images
* A real-time digital rendering of the chessboard
* The ability to play against another human or Stockfish
* Visualization of Stockfish evaluations and suggested moves
* Communication with the robot via HTTP

![Cloud Diagram](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Cloud_Scheme.png)

---

## 🤖 2. Local Robot Software

The robot’s local software is responsible for interpreting commands from the web interface and executing the necessary mechanical movements. It is modular and divided into several blocks, each with a specific role.

#### 🧩 Local System Architecture (Modules Overview)

| Block                              | Description                                                                                                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Server (API Listener)**          | Listens for HTTP POST requests from the web interface. Extracts the move and forwards it to the Central Module.                                                   |
| **Central Module**                 | Orchestrates the logic: processes the move, checks for obstacles, resolves pathfinding, and delegates to the motor control module.                                |
| **Game State Manager**             | Stores and updates the internal state of the chessboard. Translates algebraic coordinates into grid positions.                                                    |
| **Pathfinding & Obstacle Handler** | Detects if a piece is blocked and calculates alternative paths. Can temporarily move blocking pieces, execute the main move, and then restore the original state. |
| **Motor Control**                  | Translates sequences of square coordinates into physical instructions (`w`, `a`, `s`, `d`) that the robot understands and executes.                               |

#### 🔄 Local Software Diagram

![Local Software Diagram](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/local_software_scheme.png)

#### 🛠️ Execution Flow Summary

1. The web sends a POST request with the move and current board state.
2. The server receives the request and passes it to the `CentralModule`.
3. The central logic:

   * Validates the move
   * Checks for blockers
   * Moves the blocker temporarily if necessary
   * Executes the desired move
   * Restores any displaced pieces
4. The motor controller receives movement paths and emits sequential movement signals to the robot (via simulated or actual hardware).


---

## 3. Chessboard and Piece Recognition Using Computer Vision

---

### 1. Introduction

This project is part of a broader initiative to build a fully autonomous chess-playing robot. Our contribution focuses on the vision system, which identifies the real-time state of a physical chessboard via an overhead camera.

We employed image processing and deep learning techniques to detect the board, segment the squares, and classify pieces, converting the results into algebraic notation for robotic interpretation. The system is designed to be robust against lighting variations, board styles, and camera perspectives.

---

### 2. Related Work

Prior research explored digitizing chessboards using computer vision. A project at the Universidad Politécnica de Madrid applied an Xception network with perspective transforms, achieving 98% accuracy in piece recognition. Stanford proposed combining shape descriptors with the Hough transform to recognize boards from angled views, achieving 70–100% accuracy depending on the viewpoint.

Commercial apps like ChessEye and Chessify use CNNs on mobile devices to recognize physical or digital boards, integrating engines like Stockfish or Leela Chess Zero. These approaches demonstrate that vision-based systems are viable alternatives to sensor-based boards such as those from DGT or Novag.

---

### 3. System Overview

The system is based on a CNN trained on a custom dataset of manually captured and labeled chessboard images.

#### Processing Pipeline:
1. **Image Capture**
2. **Board Detection and Square Segmentation**
3. **Square-wise Filtering**
4. **CNN-based Classification**
5. **Translation to Algebraic Notation**

The entire process runs in a cloud function that receives an image and returns an 8x8 matrix of recognized positions. The system’s accuracy has been validated per square and per piece type, confirming its feasibility for robotic integration.

---

### 4. Experiments and Results

#### 4.1 Initial Approach

An overhead image was captured, converted to grayscale, and processed using the Canny edge detector to identify board lines. However, line intersections were inconsistent, leading to incorrect segmentation and failure to isolate all 64 squares. Issues included uneven lighting and imprecise line detection.

#### 4.2 Improved Board Segmentation

We introduced green corner markers on the board to aid square segmentation. These markers enabled reliable detection of board corners, and the board was successfully divided into 64 square images.

Data augmentation was applied to each square (rotations, contrast adjustment) to simulate various conditions. A single model was trained to classify the piece type in each square. However, due to dataset imbalance (many pawns and empty squares), early results were misleadingly high. Normalizing the dataset dropped accuracy to ~60%.

Square segmentation still had occasional misalignments, which affected classification. These issues led to a refined, modular approach for the final system.

---

### 4.3 Final Version

#### 4.3.1 Concept

A modular system was implemented with three independent models:
- **Presence Model**: Detects if a piece exists in the square.
- **Color Model**: Classifies the piece as white or black.
- **Type Model**: Identifies the piece type (Pawn, Knight, Bishop, Rook, Queen, King).

**Test-Time Augmentation (TTA)** is used to increase reliability: each square is augmented with rotations, flips, and filters, and the final prediction is averaged across all augmentations.

#### 4.3.2 Procedure

**Board Segmentation**  
The `crop_and_divide_board` function uses green markers to accurately crop the board into 64 squares. A margin parameter ensures square-centered cropping.

**Test-Time Augmentation (TTA)**  
Each square is augmented by:
- Rotations (90°, 180°, 270°)
- Flips (horizontal/vertical)
- Filters (contrast, gradient, etc.)

**Specialized Model Inference**  
Each augmented square is processed through:
- **Presence Model** (binary classification)
- **Color Model** (binary classification: white or black)
- **Type Model** (multi-class: P, N, B, R, Q, K)

Predictions are averaged across augmentations. If the presence score > 0.5, a piece is assumed. Color and type are only predicted when a piece is present.

**Integration of Results**  
Three boards are created:
- **Presence Board**: marks squares with X or .
- **Color Board**: marks squares with B, N or .
- **Piece Board**: marks squares with piece letters (e.g., 'p', 'K', or '.').

---

#### 4.3.3 Quantitative Results

**Presence Model**  
- Accuracy: >99%
- F1-Score: 0.994

**Color Model**  
- Accuracy: >98%
- F1-Score: 0.987

**Type Model**  
- Accuracy: ~90%
- Best results: Knights and Kings
- Most confusion: Pawns vs Bishops

| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| P     | 0.900     | 0.871  | 0.885    |
| N     | 0.915     | 0.925  | 0.920    |
| B     | 0.860     | 0.893  | 0.876    |
| R     | 0.922     | 0.898  | 0.910    |
| Q     | 0.916     | 0.888  | 0.902    |
| K     | 0.897     | 0.926  | 0.911    |

---

#### 4.3.4 Insights

- **Robustness**: TTA improves prediction consistency under visual noise.
- **Modularity**: Independent models enhance flexibility and debugging.
- **Limitations**: System performance drops if the board is misaligned or highly unlit/unusual in style.

---

### 5. Conclusion

We successfully developed a modular computer vision system capable of reconstructing a chessboard's state from a single image. The multi-stage design combined deep learning, data augmentation, and precise segmentation to achieve high accuracy even under uncontrolled conditions.


#### Future Work:
- Automatic board detection in cluttered scenes
- Handling blurred pieces, reflections, and extreme lighting
- Extension to video-based real-time chess tracking

This project demonstrates the feasibility of high-fidelity chessboard state reconstruction and opens paths for future applications in robotics, game analysis, and education.

---
## 🔧 3D Components

### Components List

1. **Axes** (2 pieces)  
**Description:** Axes that allow movement along the X and Y axes.   
**Dimensions:**  
- **Lenght:** 40.0 cm  
- **Width:** 5.2 cm  
- **Height:** 6.5 cm  
**File:** `axe.stl`
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
