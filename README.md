# PPT Master & Live Interactive Math Studio 🚀

AI 시대 교육의 문법을 바꾸는 **동적 프레젠테이션 & 수학교육 실시간 시뮬레이터 스튜디오**입니다.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

---

## 🌟 주요 기능 및 구성

### 1. 📐 수학교육 에디션 & Live Math Lab (수학.pptx)
- **Paperlogy 서체 패밀리** 적용 및 LaTeX 고해상도 수식
- **HTML5 Canvas 실시간 인터랙티브 랩**:
  - 마우스 드래그 & 슬라이더 조절
  - 이차함수 포물선 꼭짓점 기하학
  - 삼각함수 파동(진폭/주기/위상)
  - 미분계수와 접선의 순간변화율
  - 정적분 리만합과 면적 수렴
- **파워포인트 슬라이드 쇼 중 원클릭 GUI 시뮬레이터 연동**

### 2. 🌟 어린왕자 에디션 (22장)
- **완전 자율재생 (Autoplay)**: 슬라이드 전환 타이머와 Edge-TTS 고품질 나레이션 자동 연동
- **오브젝트별 순차 등장 애니메이션**: 제목 닦아내기 & 본문 카드 페이드인
- **하이브리드 조작**: 가만히 두면 저절로 흘러나오며, 마우스 클릭으로도 즉시 진행 가능
- **우하단 나레이션 툴바**: 볼륨 조절 및 일시정지 제어 지원

---

## 🚀 빠른 시작 가이드 (로컬 실행)

### 원클릭 배치 파일
- **`실시간_프리뷰_실행.bat`**: 통합 웹 스튜디오 서버 실행 (`http://localhost:5050`)
- **`수학_시뮬레이터_실행.bat`**: Paperlogy 인터랙티브 GUI 시뮬레이터 실행
- **`수학_웹_시뮬레이터_실행.bat`**: 웹 Live Math Lab 브라우저 실행
- **`어린왕자.bat`**: 어린왕자 프레젠테이션 통합 실행 메뉴

---

## 🌐 Vercel 배포 안내

이 프로젝트는 Vercel 정적 호스팅(Static Web Hosting)에 최적화되어 있습니다:
- `vercel.json` 내장
- 정적 API Fallback (`/api/slides_math.json`, `/api/slides_prince.json`) 내장
- GitHub 저장소와 Vercel을 연동하면 Push 한 번으로 자동 배포됩니다.

