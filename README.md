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

[Video of the robot in action](https://drive.google.com/file/d/1c9VE16P7BDXVjnB_LtAGnboGmgiGng_8/view?usp=drive_link )

---

## 📖 Table of Contents  
1. [Installation](#installation)
   - [Google Cloud Plataform (GCP)](#-1-google-cloud-platform-gcp)
   - [Local Robot Sofrware](#2-local-software)
2. [Electrical Wiring Diagram](#electrical-wiring-diagram)
3. [Components](#components)  
4. [Hardware Design](#hardware-design)  
5. [Software Architecture](#software-architecture)  
   - [Cloud Infrastructure (Google Cloud)](#1-cloud-infrastructure-google-cloud)  
   - [Local Robot Software](#-2-local-robot-software)
   - [Chessboard and Piece Recognition Using Computer Vision](#3-chessboard-and-piece-recognition-using-computer-vision)
6. [3D components](#3d-components)  
7. [Contributions](#amazing-contributions)  
8. [Authors](#authors)  

---

## Installation

This project is composed of two main components:

1. 🌐 The **Google Cloud** infrastructure, which handles vision and chess engine logic.
2. 🤖 The **local robot software**, which controls physical movements and logic.

---

### 🌐 1. Google Cloud Platform (GCP)

#### 📁 Project structure

In the `Google-Cloud/` directory, you will find:

* `chessboard_model/`: (Not required for installation) Training code for the original vision model.
* `chessboard_visual_function/`: Code used in the **Cloud Function** for detecting the board and pieces from an image.
* `chessboard_web/`: Frontend code and Firebase project. Contains:

  * `public/`: The web app (`index.html`, `script.js`, `styles.css`).
* `stockfish_cloud_run/`: Code for deploying **Stockfish** to **Cloud Run**.

#### ☁️ Google Cloud Setup

Make sure you have the Google Cloud CLI installed and authenticated:

```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

##### 🔸 Deploy the Vision Cloud Function

Go to the folder:

```bash
cd Google-Cloud/chessboard_visual_function
```

Deploy the function:

```bash
gcloud functions deploy predict_chessboard \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-southwest1 \
  --entry-point predict_chessboard
```

##### 🔸 Deploy Stockfish on Cloud Run

From the folder:

```bash
cd Google-Cloud/stockfish_cloud_run
```

Deploy with:

```bash
gcloud run deploy stockfish-service \
  --source . \
  --allow-unauthenticated \
  --region europe-west1
```

##### 🔸 Web Setup (Firebase Hosting)

You can test the web from the `public/` folder using any static server:

```bash
cd Google-Cloud/chessboard_web/public
python3 -m http.server 8000
# Or open index.html manually in your browser
```

If you have Firebase CLI configured and wish to deploy:

```bash
cd Google-Cloud/chessboard_web
firebase deploy
```

> ⚠️ Remember to update the endpoints in `script.js` with your actual deployed URLs for:
>
> * `predict_chessboard`
> * `stockfish-service`

---

### 2. Local Software

#### 📁 Project location

The local code is in the `src/` folder and includes:

* `modulo_central.py`: Handles logic and piece coordination.
* `motor_control.py`: Translates paths into robot movement commands.
* `game_state.py`: Board representation and utilities.
* `conexion_web.py`: A simulated Flask server to receive move commands.

#### ✅ Requirements

Since there's no `requirements.txt`, you can install the necessary packages with:

```bash
pip install flask flask-cors requests serial
```

If needed, here’s a `requirements.txt` you can create inside `src/`:

```txt
flask
flask-cors
requests
serial
```

#### 🚀 Running the robot server

Launch the Flask server to allow robot communication:

```bash
cd src
python conexion_web.py
```

This server listens on port `5000` and logs moves received from the web interface.

---
## Electrical Wiring Diagram

The following diagram illustrates the complete wiring of the robot's electronic components, including the Arduino, stepper drivers, relays, power supply, and camera system:

![Wiring Diagram](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/mechanicalTurk_bb.png)

## Components
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

## Hardware Design
*Cartesian robot design.*  

![Hardware movement gif](https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/hardware_movment.gif)

---

## Software Architecture

### 1. Cloud Infrastructure (Google Cloud)

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

### 🤖 2. Local Robot Software

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

### 3. Chessboard and Piece Recognition Using Computer Vision

---

#### 1. Introduction

This project is part of a broader initiative to build a fully autonomous chess-playing robot. Our contribution focuses on the vision system, which identifies the real-time state of a physical chessboard via an overhead camera.

We employed image processing and deep learning techniques to detect the board, segment the squares, and classify pieces, converting the results into algebraic notation for robotic interpretation. The system is designed to be robust against lighting variations, board styles, and camera perspectives.

---

#### 2. Related Work

Prior research explored digitizing chessboards using computer vision. A project at the Universidad Politécnica de Madrid applied an Xception network with perspective transforms, achieving 98% accuracy in piece recognition. Stanford proposed combining shape descriptors with the Hough transform to recognize boards from angled views, achieving 70–100% accuracy depending on the viewpoint.

Commercial apps like ChessEye and Chessify use CNNs on mobile devices to recognize physical or digital boards, integrating engines like Stockfish or Leela Chess Zero. These approaches demonstrate that vision-based systems are viable alternatives to sensor-based boards such as those from DGT or Novag.

---

#### 3. System Overview

The system is based on a CNN trained on a custom dataset of manually captured and labeled chessboard images.

#### Processing Pipeline:
1. **Image Capture**
3. **Board Detection and Square Segmentation**
4. **Square-wise Filtering**
5. **CNN-based Classification**
6. **Translation to Algebraic Notation**

The entire process runs in a cloud function that receives an image and returns an 8x8 matrix of recognized positions. The system’s accuracy has been validated per square and per piece type, confirming its feasibility for robotic integration.

---

#### 4. Experiments and Results

##### 4.1 Initial Approach

An overhead image was captured, converted to grayscale, and processed using the Canny edge detector to identify board lines. However, line intersections were inconsistent, leading to incorrect segmentation and failure to isolate all 64 squares. Issues included uneven lighting and imprecise line detection.

##### 4.2 Improved Board Segmentation

We introduced green corner markers on the board to aid square segmentation. These markers enabled reliable detection of board corners, and the board was successfully divided into 64 square images.

Data augmentation was applied to each square (rotations, contrast adjustment) to simulate various conditions. A single model was trained to classify the piece type in each square. However, due to dataset imbalance (many pawns and empty squares), early results were misleadingly high. Normalizing the dataset dropped accuracy to ~60%.

Square segmentation still had occasional misalignments, which affected classification. These issues led to a refined, modular approach for the final system.

---

#### 4.3 Final Version

##### 4.3.1 Concept

A modular system was implemented with three independent models:
- **Presence Model**: Detects if a piece exists in the square.
- **Color Model**: Classifies the piece as white or black.
- **Type Model**: Identifies the piece type (Pawn, Knight, Bishop, Rook, Queen, King).

**Test-Time Augmentation (TTA)** is used to increase reliability: each square is augmented with rotations, flips, and filters, and the final prediction is averaged across all augmentations.

##### 4.3.2 Procedure

**Board Segmentation**  
The `crop_and_divide_board` function uses green markers to accurately crop the board into 64 squares. A margin parameter ensures square-centered cropping.

<h4>Step-by-Step Image Processing Pipeline</h4>

<table>
  <tr>
    <th>Step</th>
    <th>Image</th>
    <th>Description</th>
  </tr>

  <tr>
    <td><strong>1. Original Image</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_1.png?raw=true" width="400"/></td>
    <td>The input image as captured from the camera. It shows the chessboard including the green corner markers.</td>
  </tr>

  <tr>
    <td><strong>2. HSV Conversion</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_2.png?raw=true" width="400"/></td>
    <td>The image converted to HSV color space, which is more suitable for color filtering (used to detect green markers).</td>
  </tr>

  <tr>
    <td><strong>3. Green Mask</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_3.png?raw=true" width="400"/></td>
    <td>A binary mask that highlights areas with green color based on a defined HSV range. This helps isolate the board corners.</td>
  </tr>

  <tr>
    <td><strong>4. Corner Detection</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_4.png?raw=true" width="400"/></td>
    <td>Green circular blobs are detected as corners using contour filtering and centroid extraction. These are used to define the board's geometry.</td>
  </tr>

  <tr>
    <td><strong>5. Ordered Corners</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_5.png?raw=true" width="400"/></td>
    <td>The detected corners are reordered to follow a consistent pattern: top-left, top-right, bottom-right, bottom-left. This is critical for perspective correction.</td>
  </tr>

  <tr>
    <td><strong>6. Perspective Correction</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_6.png?raw=true" width="400"/></td>
    <td>The chessboard is warped into a square using a perspective transform. This produces a flat, aligned top-down view of the board.</td>
  </tr>

  <tr>
    <td><strong>7. Board Grid Division</strong></td>
    <td><img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_7.png?raw=true" width="400"/></td>
    <td>The aligned board is divided into an 8x8 grid, generating 64 individual cell images. These are used for per-square analysis and classification.</td>
  </tr>

</table>

**Test-Time Augmentation (TTA)**  
Each square is augmented by:
- Rotations (90°, 180°, 270°)
- Flips (horizontal/vertical)
- Filters (contrast, gradient, etc.)

| Filter       | Image        |
|--------------|--------------|
| **Filter1** | <img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_8.png?raw=true" width="100%"/> |
| **Filter2** | <img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_9.png?raw=true" width="100%"/> |
| **Filter3** | <img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_10.png?raw=true" width="100%"/> |
| **Filter4** | <img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_11.png?raw=true" width="100%"/> |
| **Filter5** | <img src="https://github.com/AdriaFerOrtiz/ProyectoMechanicalTurk/blob/main/Schemes-Img/Figure_12.png?raw=true" width="100%"/> |

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

##### 4.3.3 Quantitative Results

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

##### 4.3.4 Insights

- **Robustness**: TTA improves prediction consistency under visual noise.
- **Modularity**: Independent models enhance flexibility and debugging.
- **Limitations**: System performance drops if the board is misaligned or highly unlit/unusual in style.

---

#### 5. Conclusion

We successfully developed a modular computer vision system capable of reconstructing a chessboard's state from a single image. The multi-stage design combined deep learning, data augmentation, and precise segmentation to achieve high accuracy even under uncontrolled conditions.


##### Future Work:
- Automatic board detection in cluttered scenes
- Handling blurred pieces, reflections, and extreme lighting
- Extension to video-based real-time chess tracking

This project demonstrates the feasibility of high-fidelity chessboard state reconstruction and opens paths for future applications in robotics, game analysis, and education.

---
## 3D Components

### Components List

**1. Axis (4 pieces)**

*  **Description**: Axes that allow movement along the X and Y axes.
*  **Dimensions**:
     * Length: 20 cm
       
     * Width: 5.2 cm
       
     * Height: 6.5 cm
       
*  **File**: axis.stl
<img src="3D_files/images/axis.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

**2. Box**

*  **Description**: Box where all the robot's mechanism is
*  **Dimensions**:
     * Length: 45 cm
       
     * Width: 45 cm
       
     * Height: 20 cm
       
*  **File**: box.svg
<img src="3D_files/images/box.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

**3. Box_lid**

*  **Description**: Lid of the box where the chessboard is painted
*  **Dimensions**:
     * Length: 45 cm
       
     * Width: 45 cm
       
     * Height: 0.6 cm
       
*  **File**: box_lid.stl
<img src="3D_files/images/box_lid.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

**4. Cylinders (2 pieces)**

*  **Description**: Support cylinders for the movement of the axis.
*  **Dimensions**:
     * Length: 0.8 cm
       
     * Width: 0.8 cm
       
     * Height: 3 cm
       
*  **File**: cylinder.stl
<img src="3D_files/images/cylinder.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

**5. Lid_brace**

*  **Description**: Lace piece for the box lid.
*  **Dimensions**:
     * Length: 42 cm
       
     * Width: 42 cm
       
     * Height: 1 cm
       
*  **File**: lid_brace.stl
<img src="3D_files/images/lid_brace.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

**6. Platform (2 pieces)**

*  **Description**: Platform to move the electromagnet around the chessboard.
*  **Dimensions**:
     * Length: 12 cm
       
     * Width: 5.7 cm
       
     * Height: 1 cm
       
*  **File**: platform.stl
<img src="3D_files/images/platform.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

**7. Toothed_cylinders (2 pieces)**

*  **Description**: Toothed cylinders to move along the axes.
*  **Dimensions**:
     * Length: 0.9 cm
       
     * Width: 0.9 cm
       
     * Height: 1.5 cm
       
*  **File**: toothed_cylinders.stl
<img src="3D_files/images/toothed_cylinder.png" alt="Axis Preview" width="600" style="border-radius: 10px;"/>

### Summary Table

| # | Component           | Pieces | File               |
|---|---------------------|--------|--------------------|
| 1 | Axis                | 4      | axis.stl           |
| 2 | Box                 | 1      | box.stl            |
| 3 | Box Lid             | 1      | box_lid.stl        |
| 4 | Cylinders           | 2      | cylinder.stl       |
| 5 | Lid Brace           | 1      | lid_brace.stl      |
| 6 | Platform            | 2      | platform.stl       |
| 7 | Toothed Cylinders   | 2      | toothed_cylinders.stl |

### How to Use the 3D Files

1. **Download**: All STL files are located in the `/3D_files` directory of this repository.
2. **Open**: Use a slicer like [Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura) or [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) to open the `.stl` files.
3. **Print Settings** (recommended):
   - Layer height: 0.2 mm
   - Infill: 20% – 40%
   - Supports: As needed depending on the piece
   - Material: PLA or PETG

---

## Amazing Contributions  
- **Obstacle Avoidance**: The robot plans alternative paths if pieces block movement.  
- **Low-Cost Precision**: Achieves sub-millimeter accuracy with budget stepper motors.  
- **Social Impact**: Makes chess accessible for visually impaired players via physical interaction.  

---

## Authors  
- Eduard José García Mendeleac
- Adrià Fernández Ortiz
- Luis Adrián Gómez Batista
