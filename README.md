# 🚒 ROS 2 화재 감지 및 거리 측정 시스템

> 단일 RGB 카메라와 회전 기하학으로 추가 거리 센서 없이 화재 위치를 감지·측정하는 모듈형 ROS 2 로봇 시스템

[![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?style=flat-square&logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![C++](https://img.shields.io/badge/C%2B%2B-17-00599C?style=flat-square&logo=cplusplus&logoColor=white)](https://isocpp.org/)
[![ONNX](https://img.shields.io/badge/ONNX-Runtime-005CED?style=flat-square&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=flat-square&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

---

## 📌 주요 특징

- ONNX Runtime 기반 실시간 화재 감지
- 화재 감지 시 외부 장치(Arduino)와 시리얼 통신
- 화재 중심 정렬 + 회전 기반 관측 데이터 수집
- SLAM Toolbox 연동 실시간 지도 생성
- 단일 launch 파일로 전체 시스템 실행
- 모듈 교체 및 확장에 용이한 ROS 2 구조

---

## 🛠️ 기술 스택

| Category | Tools |
|---|---|
| Framework | ROS 2 Humble |
| Language | Python 3.10, C++17 |
| Vision | ONNX Runtime |
| SLAM | slam_toolbox |
| Visualization | RViz2 |
| Communication | pyserial (Arduino via USB) |
| Build System | ament_python, ament_cmake |
| OS | Ubuntu 22.04 |

---

## 📦 패키지 구성

| 패키지 | 빌드 타입 | 주요 기능 |
|---|---|---|
| `fire_vision` | ament_python | ONNX 기반 화재 감지 및 시리얼 출력 |
| `fire_distance` | ament_python | 자율 중심 정렬 및 회전 기반 거리 측정 |
| `fire_slam` | ament_cmake | SLAM Toolbox 연동 위치 추정 및 지도 생성 |
| `fire_bringup` | ament_python | 전체 노드 단일 launch 파일로 통합 실행 |

---

## 🧩 시스템 아키텍처

```
Camera
│
▼
[ fire_detector_onnx ]
├─ /fire_detected
└─ /fire_center_px
│
▼
[ fire_centering_node ]
├─ /cmd_vel
└─ /fire/centered
│
▼
[ fire_rotation_measure_node ]
├─ /fire/x0_px
├─ /fire/x1_px
└─ /fire/actual_delta_deg
│
▼
[ fire_distance_controller_node ]
└─ /fire/distance_batch

[ slam_toolbox ]
└─ /map, /tf
```

---

## 🚀 시스템 실행 방법

### 1️⃣ 워크스페이스 빌드

```bash
cd ~/fire_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### 2️⃣ 전체 시스템 실행

```bash
ros2 launch fire_bringup bringup_all.launch.py
```

위 명령 하나로 다음 노드들이 동시에 실행된다.

- 화재 감지 (ONNX)
- 시리얼 통신
- 화재 중심 정렬
- 회전 및 거리 관측
- SLAM 지도 생성

---

## 🔄 노드별 데이터 흐름

### A. 화재 감지 및 통신 (`fire_vision`)

| 노드 | 입력 / 출력 | 설명 |
|---|---|---|
| `fire_detector_onnx` | 입력: 웹캠(0번)<br>출력: `/fire_detected`, `/fire_center_px` | 320×320 영상 ONNX 추론 → 화재 여부 및 중심 픽셀 퍼블리시 |
| `fire_serial_sender` | 입력: `/fire_detected`<br>출력: `/dev/ttyUSB0` | 화재 감지 시 `b'1'` 시리얼 전송 |

### B. 거리 측정 파이프라인 (`fire_distance`)

| 노드 | 입력 / 출력 | 설명 |
|---|---|---|
| `fire_centering_node` | 입력: `/fire_center_px`<br>출력: `/cmd_vel`, `/fire/centered` | 화재를 화면 중앙으로 정렬 제어 |
| `fire_rotation_measure_node` | 입력: `/fire/centered`, `/fire_center_px`, `/imu`<br>출력: `/fire/x0_px`, `/fire/x1_px`, `/fire/actual_delta_deg` | 회전 전·후 관측값 및 실제 회전각 측정 |
| `fire_distance_controller_node` | 입력: `/fire/x0_px`, `/fire/x1_px`, `/fire/actual_delta_deg`<br>출력: `/fire/distance_batch` | 관측 데이터를 JSON 형태로 통합 출력 |
