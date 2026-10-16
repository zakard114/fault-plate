# 권한

fault-plate-check와 plate-reviewer는 규격을 읽기만 한다. 앱 파일을 고치거나 커밋하지 않는다.

MCP 도구 get_plate는 GET /plates만 호출한다. 저장, 삭제, 배포를 하지 않는다. 비밀 값을 보내지 않는다.

훅 check_plate.py는 입력 JSON에 다섯 필드가 있는지만 본다. 파일을 만들거나 고치지 않는다. 모든 셸 명령 앞에 붙이지 않는다.
