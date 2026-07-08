# 만약 pyvenv Scripts\activate 실행이 안된다면 아래의 실행 명령어를 사용하여 권한 부여

# 문제 목록 (해당되는 문제를 클릭)

1. [(pyvenv)\Scripts\activate가 실행이 안되는 경우](#pyvenvscriptsactivate가-실행이-안되는-경우)

2. [mujoco를 설치하고 실행이 되지 않는 경우](#mujoco를-설치하고-실행이-되지-않는-경우)

---

## pyvenv\Scripts\activate가 실행이 안되는 경우

- 대부분 권한이 부여되지 않아 발생한다. 아래의 코드를 PowerShell에서 실행하여 권한을 부여하면 대부분 해결됨.

### 영구 권한 부여(초기 1회만 실행)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 임시 권한 부여(영구적 부여가 부담스럽다면 아래의 코드 사용)
> powershell을 새로 열거나 지우는 경우 다시 실행해야 정상적으로 권한이 부여됨

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

---

## mujoco를 설치하고 실행이 되지 않는 경우

- Windows 보안 정책에 막혀 실행되지 않는 경우가 있습니다. 아래 방법을 통해 우회 혹은 보안을 낮춰 실행할 수 있습니다.

### WSL2를 사용하는 방법
> WSL(Windows Subsystem for Linux)은 Windows 내에서 가상 리눅스환경을 구축하는 기술로, 이를 통해 Windows의 보안 정책을 우회하여 mujoco를 실행할 수 있습니다.

- PowerShell에 관리자권한으로 열어 아래 코드를 실행한 후 wsl에 접속하여 `pip install mujoco`를 통해 재설치하여 mujoco를 실행할 수 있습니다.
```
wsl --install
```

### Windows 11 스마트 앱 제어 끄기

- `Windows 보안 > 앱 및 브라우저 컨트롤 > 스마트 앱 컨트롤 > 스마트 앱 컨드롤 설정 > 끄기`

----