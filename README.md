# 🚒 ROS 2 화재 감지 및 거리 측정 시스템

본 프로젝트는 **ROS 2 (Humble)** 기반으로  
**화재 감지 → 로봇 제어 → 회전 기반 거리 측정 → 시리얼 통신**을 통합한  
모듈형 로봇 시스템이다.

단일 RGB 카메라와 회전 기하학을 활용하여 **추가 거리 센서 없이도**
화재와의 상대적 거리를 관측·분석할 수 있는 파이프라인을 구현하였다.

---

## 📌 주요 특징

- ONNX Runtime 기반 실시간 화재 감지
- 화재 감지 시 외부 장치(Arduino)와 시리얼 통신
- 화재 중심 정렬 + 회전 기반 관측 데이터 수집
- SLAM Toolbox 연동 실시간 지도 생성
- 단일 launch 파일로 전체 시스템 실행
- 모듈 교체 및 확장에 용이한 ROS 2 구조

---

## 📦 패키지 구성 상세

| 패키지 이름 | 빌드 타입 | 주요 기능 | 상세 설명 |
|------------|----------|----------|----------|
| **fire_vision** | ament_python | ONNX 기반 화재 감지 및 시리얼 출력 | ONNX Runtime을 이용해 카메라 영상에서 화재를 감지하고, 감지 결과를 ROS 토픽 및 외부 시리얼 장치로 전달 |
| **fire_distance** | ament_python | 자율 중심 정렬 및 거리 측정 데이터 수집 | 화재를 목표로 로봇을 제자리 회전 제어하여 정렬하고, 회전 전·후 관측값을 수집하는 핵심 파이프라인 |
| **fire_slam** | ament_cmake | 동시적 위치 추정 및 지도 작성 (SLAM) | slam_toolbox를 이용한 로봇 위치 추정 및 지도 생성 |
| **fire_bringup** | ament_python | 시스템 통합 및 일괄 실행 | 모든 핵심 노드를 단일 launch 파일로 실행하는 통합 패키지 |

---

## 🧩 시스템 아키텍처 개요
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

```
cd ~/fire_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

---

2️⃣ 전체 시스템 실행
ros2 launch fire_bringup bringup_all.launch.py


위 명령 하나로 다음 노드들이 동시에 실행된다.

화재 감지 (ONNX)

시리얼 통신

화재 중심 정렬

회전 및 거리 관측

SLAM 지도 생성

🔄 노드별 데이터 흐름 상세 

A. 화재 감지 및 통신 (fire_vision)
| 노드                 | 입력 / 출력                                               | 설명                                                       |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------------- |
| fire_detector_onnx | 입력: 웹캠(0번)<br>출력: `/fire_detected`, `/fire_center_px` | 320×320 영상으로 ONNX 추론을 수행하고, 화재 존재 여부 및 화재 중심 픽셀 좌표를 퍼블리시 |
| fire_serial_sender | 입력: `/fire_detected`<br>출력: `/dev/ttyUSB0`            | 화재 감지 시 `b'1'`을 시리얼로 전송                                  |

B. 거리 측정 파이프라인 (fire_distance)
| 노드                            | 입력 / 출력                                                                                                       | 설명                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------ |
| fire_centering_node           | 입력: `/fire_center_px`<br>출력: `/cmd_vel`, `/fire/centered`                                                     | P 제어를 이용해 화재를 화면 중앙으로 정렬 |
| fire_rotation_measure_node    | 입력: `/fire/centered`, `/fire_center_px`, `/imu`<br>출력: `/fire/x0_px`, `/fire/x1_px`, `/fire/actual_delta_deg` | 회전 전·후 관측값 및 실제 회전각 측정   |
| fire_distance_controller_node | 입력: `/fire/x0_px`, `/fire/x1_px`, `/fire/actual_delta_deg`<br>출력: `/fire/distance_batch`                      | 관측 데이터를 JSON 형태로 통합 출력   |

---
🛠️ 개발 환경

OS: Ubuntu 22.04

ROS: ROS 2 Humble

언어: Python 3.10, C++

비전 추론: ONNX Runtime

SLAM: slam_toolbox

시각화: RViz2

빌드 시스템: ament_python / ament_cmake
