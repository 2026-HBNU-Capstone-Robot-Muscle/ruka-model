import os
import time
import math
import mujoco
import mujoco.viewer

def set_hand_close(model, data, fraction):
    # fraction: 0.0 (fully open) to 1.0 (fully closed)
    # Define actuator target ranges for folding
    targets = {
        "Index_MCP_actuator": 1.8,
        "Index_DIP_actuator": 1.5,
        "Index_PIP_actuator": 1.5,
        "Middle_MCP_actuator": 1.8,
        "Middle_DIP_actuator": 1.5,
        "Middle_PIP_actuator": 1.5,
        "Ring_MCP_actuator": 1.8,
        "Ring_DIP_actuator": 1.5,
        "Ring_PIP_actuator": 1.5,
        "Pinky_MCP_actuator": 1.8,
        "Pinky_DIP_actuator": 1.5,
        "Pinky_PIP_actuator": 1.5,
        "Thumb_CMC_actuator": -1.5,
        "Thumb_MCP_actuator": 1.0,
        "Thumb_PIP_actuator": 1.5,
    }
    
    for name, max_val in targets.items():
        act_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)
        if act_id != -1:
            data.ctrl[act_id] = max_val * fraction

def main():
    # 이 스크립트 파일의 위치를 기준으로 한 xml 상대 경로 설정 (상자가 포함된 scene 로드)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.join(script_dir, "assets", "xml", "hand_box_scene.xml")
    
    print(f"Loading MuJoCo model from: {xml_path}")
    
    if not os.path.exists(xml_path):
        print(f"Error: {xml_path} file not found!")
        return

    try:
        # MuJoCo 모델 및 데이터 로드
        model = mujoco.MjModel.from_xml_path(xml_path)
        data = mujoco.MjData(model)
        
        # 기본 'home' 키프레임이 있으면 해당 키프레임 위치로 초기화
        home_key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, "home")
        if home_key_id != -1:
            mujoco.mj_resetDataKeyframe(model, data, home_key_id)
            print("Reset simulation to 'home' keyframe.")
        
        # 비차단(passive) 인터랙티브 뷰어 실행
        print("Launching MuJoCo Viewer. Close the viewer window to exit.")
        with mujoco.viewer.launch_passive(model, data) as viewer:
            
            # 충돌체 시각화 (Geom Group 2 활성화)
            viewer.opt.geomgroup[2] = True
            
            # 충돌 접촉 지점(Contact Point) 및 접촉력(Contact Force) 시각화 활성화
            try:
                viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = False
                viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = False
            except AttributeError:
                pass
            
            print("Starting control loop. The hand will fold and unfold repeatedly.")
            
            # 제어 루프 실행
            while viewer.is_running():
                step_start = time.time()
                
                # data.time을 기준으로 사인파를 이용해 -1.0(활짝 폄) ~ 1.0(꽉 접힘) 사이를 왕복
                # 엑추에이터가 단순 토크(힘) 제어기이므로, 반대 방향 힘(음수 토크)을 줘야 손가락이 펴집니다.
                cycle_speed = 2.0  # 속도 조절
                fraction = math.sin(data.time * cycle_speed)
                
                # 손가락 제어 값 적용
                set_hand_close(model, data, fraction)
                
                # 시뮬레이션 물리 스텝 전진
                mujoco.mj_step(model, data)
                
                # 뷰어 동기화
                viewer.sync()
                
                # 실시간 시뮬레이션 속도 유지
                time_until_next_step = model.opt.timestep - (time.time() - step_start)
                if time_until_next_step > 0:
                    time.sleep(time_until_next_step)
                    
    except Exception as e:
        print(f"An error occurred while running the simulation: {e}")

if __name__ == "__main__":
    main()

