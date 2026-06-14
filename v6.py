import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="ver06 종합 과제",
    page_icon="🎒",
    layout="wide",
)

# =========================================================
# ver06 종합 과제
# 사용한 내용:
# - v1: title, caption, write, info, success, warning, code
# - v2: text_input, selectbox, radio, slider, multiselect, checkbox, button
# - v3: sidebar, columns, metric, tabs, expander
# - v4: form, form_submit_button, session_state, list/dict 기록 저장
# - v5: 점수 계산 함수, 레벨 계산 함수, 필터, 요약 대시보드
#
# 주의:
# - pandas를 사용하지 않습니다.
# - 기록은 st.session_state.records 라는 리스트에 딕셔너리로 저장합니다.
# =========================================================


# -----------------------------
# 1. 기록을 저장할 공간 만들기
# -----------------------------
if "records" not in st.session_state:
    st.session_state.records = []


# -----------------------------
# 2. 점수 계산 함수
# -----------------------------
def calculate_score(minutes, focus, difficulty):
    """
    공부 시간, 집중도, 난이도를 이용해서 가상 점수를 계산합니다.
    학생 미션: 아래 공식을 자기 방식으로 바꿔보세요.
    """
    score = 40
    score = score + minutes // 3
    score = score + focus * 4
    score = score - difficulty * 3

    if score > 100:
        score = 100
    if score < 0:
        score = 0

    return score


# -----------------------------
# 3. 레벨 계산 함수
# -----------------------------
def calculate_level(score):
    """
    점수에 따라 레벨 이름을 정합니다.
    학생 미션: 레벨 이름을 자기 스타일로 바꿔보세요.
    """
    if score >= 90:
        return "최고 집중러"
    if score >= 75:
        return "꾸준한 성장러"
    if score >= 60:
        return "연습 중"
    return "기초 다지기"


# -----------------------------
# 4. 추천 문장 함수
# -----------------------------
def make_recommendation(focus, difficulty):
    """
    집중도와 난이도에 따라 간단한 추천 문장을 만듭니다.
    """
    if focus >= 8 and difficulty <= 3:
        return "오늘은 새로운 기능을 하나 더 추가해봐도 좋습니다."
    if focus <= 4:
        return "오늘은 쉬운 예제를 다시 따라 하면서 흐름을 익혀보세요."
    if difficulty >= 4:
        return "어려웠던 부분을 메모하고, 친구나 선생님에게 질문해보세요."
    return "지금처럼 차근차근 기록을 쌓아보세요."


# -----------------------------
# 5. 앱 제목과 설명
# -----------------------------
st.title("ver06. 종합 과제: 나만의 학습 기록 앱")
st.caption("목표: v1부터 v5까지 배운 기능만 사용해서 작은 Streamlit 앱을 완성합니다.")

st.info("이 파일은 완성된 정답이 아니라 과제 출발점입니다. 주석에 적힌 학생 미션을 보고 직접 바꿔보세요.")
st.warning("pandas는 사용하지 않습니다. 기록은 리스트와 딕셔너리로만 저장합니다.")


# -----------------------------
# 6. 사이드바 설정
# -----------------------------
st.sidebar.header("보기 설정")

selected_subject = st.sidebar.selectbox(
    "주제 필터",
    ["전체", "Python", "Streamlit", "AI", "데이터 시각화"],
)

show_records = st.sidebar.checkbox("기록 표 보기", value=True)
show_mission = st.sidebar.checkbox("학생 미션 보기", value=True)

st.sidebar.divider()
st.sidebar.write("현재 저장된 기록 수")
st.sidebar.metric("기록 개수", len(st.session_state.records))


# -----------------------------
# 7. 필터 적용
# -----------------------------
records = st.session_state.records

if selected_subject != "전체":
    records = [row for row in records if row["subject"] == selected_subject]


# -----------------------------
# 8. 탭 구성
# -----------------------------
tab_input, tab_summary, tab_records, tab_mission = st.tabs(
    ["1. 기록 입력", "2. 요약 보기", "3. 기록 목록", "4. 과제 안내"]
)


# =========================================================
# 탭 1. 기록 입력
# =========================================================
with tab_input:
    left, right = st.columns([1, 1])

    with left:
        st.subheader("새 학습 기록 입력")

        with st.form("record_form"):
            name = st.text_input("이름", value="학생")
            team = st.selectbox("팀", ["1팀", "2팀", "3팀", "4팀"])
            subject = st.radio(
                "오늘 공부한 주제",
                ["Python", "Streamlit", "AI", "데이터 시각화"],
                horizontal=True,
            )

            minutes = st.slider("공부 시간(분)", 0, 180, 45, 5)
            focus = st.slider("집중도", 1, 10, 7)
            difficulty = st.slider("체감 난이도", 1, 5, 3)

            mood = st.selectbox("오늘의 기분", ["좋음", "보통", "피곤함", "신남"])

            features = st.multiselect(
                "오늘 사용한 Streamlit 기능",
                ["글자 출력", "입력 위젯", "사이드바", "컬럼", "탭", "폼", "상태 저장"],
                default=["글자 출력", "입력 위젯"],
            )

            memo = st.text_area("오늘의 메모", value="오늘 배운 내용을 적어보세요.")

            # 학생 미션 예시:
            # 아래처럼 입력 항목을 하나 더 만들어보세요.
            # place = st.selectbox("공부 장소", ["교실", "집", "도서관", "카페"])

            submit = st.form_submit_button("기록 저장")

        if submit:
            score = calculate_score(minutes, focus, difficulty)
            level = calculate_level(score)

            new_record = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "name": name,
                "team": team,
                "subject": subject,
                "minutes": minutes,
                "focus": focus,
                "difficulty": difficulty,
                "mood": mood,
                "features": features,
                "score": score,
                "level": level,
                "memo": memo,
            }

            # 학생 미션:
            # 입력 항목을 새로 추가했다면, 위 new_record에도 같이 넣어야 합니다.
            # 예: "place": place,

            st.session_state.records.append(new_record)
            st.success(f"{name}님의 기록을 저장했습니다. 점수는 {score}점입니다.")
            st.balloons()

    with right:
        st.subheader("입력 결과 미리보기")

        preview_score = calculate_score(minutes, focus, difficulty)
        preview_level = calculate_level(preview_score)
        recommendation = make_recommendation(focus, difficulty)

        col1, col2 = st.columns(2)
        col1.metric("예상 점수", f"{preview_score}점")
        col2.metric("예상 레벨", preview_level)

        st.write(f"**{team}의 {name}님**은 오늘 **{subject}** 주제를 공부했습니다.")
        st.write(f"공부 시간은 **{minutes}분**, 집중도는 **{focus}/10**, 난이도는 **{difficulty}/5**입니다.")
        st.write("오늘 사용한 기능:", features)

        if mood == "신남":
            st.success("오늘은 에너지가 좋아 보입니다!")
        elif mood == "피곤함":
            st.warning("오늘은 너무 무리하지 말고 천천히 해도 괜찮습니다.")
        else:
            st.info("꾸준히 기록하는 것이 가장 중요합니다.")

        st.write("추천:", recommendation)


# =========================================================
# 탭 2. 요약 보기
# =========================================================
with tab_summary:
    st.subheader("현재 기록 요약")

    total = len(records)

    if total == 0:
        st.info("아직 요약할 기록이 없습니다. 먼저 기록을 저장해보세요.")
    else:
        avg_score = sum(row["score"] for row in records) / total
        avg_focus = sum(row["focus"] for row in records) / total
        avg_minutes = sum(row["minutes"] for row in records) / total

        best = max(records, key=lambda row: row["score"])
        longest = max(records, key=lambda row: row["minutes"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("기록 수", total)
        col2.metric("평균 점수", f"{avg_score:.1f}점")
        col3.metric("평균 집중도", f"{avg_focus:.1f}/10")
        col4.metric("평균 공부 시간", f"{avg_minutes:.1f}분")

        st.progress(int(avg_score))

        st.success(
            f"최고 점수 기록: {best['name']} / {best['subject']} / {best['score']}점 / {best['level']}"
        )
        st.info(
            f"가장 오래 공부한 기록: {longest['name']} / {longest['subject']} / {longest['minutes']}분"
        )

        with st.expander("요약 계산에 사용한 코드 보기"):
            st.code(
                """
total = len(records)
avg_score = sum(row["score"] for row in records) / total
best = max(records, key=lambda row: row["score"])
longest = max(records, key=lambda row: row["minutes"])
""".strip(),
                language="python",
            )


# =========================================================
# 탭 3. 기록 목록
# =========================================================
with tab_records:
    st.subheader("저장된 기록 목록")

    if len(st.session_state.records) == 0:
        st.info("아직 저장된 기록이 없습니다.")
    else:
        if selected_subject != "전체":
            st.write(f"현재 **{selected_subject}** 주제 기록만 보고 있습니다.")
        else:
            st.write("현재 전체 기록을 보고 있습니다.")

        if show_records:
            # pandas가 아니라, 리스트 안의 딕셔너리를 Streamlit이 표처럼 보여주는 것입니다.
            st.dataframe(records, use_container_width=True)
        else:
            st.write("사이드바에서 '기록 표 보기'를 켜면 표가 나타납니다.")

        st.divider()

        st.subheader("한 줄 기록 보기")

        for row in records:
            with st.expander(f"{row['time']} / {row['name']} / {row['subject']} / {row['score']}점"):
                st.write(f"팀: {row['team']}")
                st.write(f"공부 시간: {row['minutes']}분")
                st.write(f"집중도: {row['focus']}/10")
                st.write(f"난이도: {row['difficulty']}/5")
                st.write(f"기분: {row['mood']}")
                st.write(f"레벨: {row['level']}")
                st.write("사용한 기능:", row["features"])
                st.write(f"메모: {row['memo']}")

    st.divider()

    col_delete, col_example = st.columns(2)

    with col_delete:
        if st.button("모든 기록 삭제"):
            st.session_state.records = []
            st.rerun()

    with col_example:
        if st.button("예시 기록 1개 추가"):
            example_score = calculate_score(60, 8, 3)
            st.session_state.records.append(
                {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "name": "예시학생",
                    "team": "1팀",
                    "subject": "Streamlit",
                    "minutes": 60,
                    "focus": 8,
                    "difficulty": 3,
                    "mood": "좋음",
                    "features": ["글자 출력", "입력 위젯", "폼"],
                    "score": example_score,
                    "level": calculate_level(example_score),
                    "memo": "예시로 추가한 기록입니다.",
                }
            )
            st.rerun()


# =========================================================
# 탭 4. 과제 안내
# =========================================================
with tab_mission:
    st.subheader("학생 종합 과제")

    if show_mission:
        st.write("아래 미션을 따라 `v6.py`를 나만의 앱으로 바꿔보세요.")

        st.markdown("### 필수 미션")
        st.write("1. 앱 제목과 소개 문장을 자기 주제에 맞게 바꾸기")
        st.write("2. 입력 항목을 1개 이상 추가하기")
        st.write("3. 추가한 입력 항목이 저장 기록에도 나오게 만들기")
        st.write("4. 점수 계산 공식 또는 레벨 이름 중 하나 이상 바꾸기")
        st.write("5. 실행 화면을 캡처해서 제출하기")
        st.write("6. 내가 바꾼 코드 3줄 이상 설명하기")

        st.markdown("### 선택 미션")
        st.write("- 주제 필터 대신 팀 필터 만들기")
        st.write("- 추천 문장을 더 재미있게 바꾸기")
        st.write("- 기분에 따라 점수 보너스 주기")
        st.write("- 기록을 펼침 영역 말고 다른 방식으로 보여주기")
        st.write("- 레벨 이름을 게임처럼 바꾸기")

        st.markdown("### 제출물")
        st.write("1. 실행 화면 캡처 1장")
        st.write("2. 내가 추가한 기능 설명 2줄")
        st.write("3. 내가 수정한 코드 3줄 이상")
        st.write("4. 어려웠던 점 1줄, 재미있었던 점 1줄")

        with st.expander("입력 항목 추가 힌트"):
            st.write("폼 안에 아래 코드를 추가합니다.")
            st.code(
                """
place = st.selectbox("공부 장소", ["교실", "집", "도서관", "카페"])
""".strip(),
                language="python",
            )
            st.write("그리고 new_record 안에도 아래처럼 추가합니다.")
            st.code(
                """
"place": place,
""".strip(),
                language="python",
            )

        with st.expander("점수 공식 바꾸기 힌트"):
            st.write("calculate_score 함수 안의 공식을 바꿔보세요.")
            st.code(
                """
score = 30
score = score + minutes // 2
score = score + focus * 5
score = score - difficulty * 4
""".strip(),
                language="python",
            )

        with st.expander("레벨 이름 바꾸기 힌트"):
            st.write("calculate_level 함수의 return 문장을 바꿔보세요.")
            st.code(
                """
if score >= 90:
    return "학습 마스터"
if score >= 75:
    return "성장 중"py
    
if score >= 60:
    return "연습 중"
return "다시 도전"
""".strip(),
                language="python",
            )
    else:
        st.info("사이드바에서 '학생 미션 보기'를 켜면 과제 안내가 나타납니다.")
