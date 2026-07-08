# 만약 pyvenv Scripts\activate 실행이 안된다면 아래의 실행 명령어를 사용하여 권한 부여

## 초기 1회만 실행하면 됨

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 영구적 부여가 부담스럽다면 아래의 코드 사용하여 임시로 권한 부여
> powershell을 새로 열거나 지우는 경우 다시 실행해야 정상적으로 권한이 부여됨

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```