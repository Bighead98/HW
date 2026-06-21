import csv
import io
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="ver12 Day2 과제", page_icon="🎒", layout="wide")

# =========================================================
# ver12. Day2 종합 과제 템플릿
#
# 과제 목표:
# Day1 + Day2에서 배운 기능을 합쳐서 나만의 학습 대시보드 v2를 완성합니다.
#
# 반드시 포함할 기능:
# 1. 기록 입력
# 2. 필터
# 3. 요약 지표
# 4. 차트
# 5. CSV 다운로드
# 6. 표 편집 또는 삭제
# 7. 채팅형 도움말 규칙 1개 추가
#
# 주의:
# - pandas, numpy는 사용하지 않습니다.
# - 기록은 리스트와 딕셔너리로 저장합니다.
# =========================================================

FIELDNAMES = [
    "time",
    "name",
    "team",
    "subject",
    "minutes",
    "focus",
    "difficulty",
    "mood",
    "place",
    "features",
    "score",
    "level",
    "memo",
]

SUBJECTS = ["Python", "Streamlit", "AI", "데이터 시각화"]
TEAMS = ["1팀", "2팀", "3팀", "4팀"]


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def calculate_score(minutes, focus, difficulty, mood):
    """
    과제 미션:
    아래 점수 공식을 자기 방식으로 바꿔보세요.
    예: 기분이 '신남'이면 보너스, 난이도가 높으면 보너스 등
    """
    score = 40
    score += minutes // 3
    score += focus * 4
    score -= difficulty * 3

    if mood == "신남":
        score += 5
    if mood == "피곤함":
        score -= 3

    return max(0, min(100, score))


def calculate_level(score):
    """
    과제 미션:
    레벨 이름을 자기 앱 주제에 맞게 바꿔보세요.
    """
    if score >= 90:
        return "대시보드 마스터"
    if score >= 75:
        return "꾸준한 성장러"
    if score >= 60:
        return "연습 중"
    return "기초 다지기"


def make_record(name, team, subject, minutes, focus, difficulty, mood, place, features, memo):
    score = calculate_score(minutes, focus, difficulty, mood)
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "name": name,
        "team": team,
        "subject": subject,
        "minutes": minutes,
        "focus": focus,
        "difficulty": difficulty,
        "mood": mood,
        "place": place,
        "features": features,
        "score": score,
        "level": calculate_level(score),
        "memo": memo,
    }


def clean_record(row):
    minutes = safe_int(row.get("minutes"), 0)
    focus = safe_int(row.get("focus"), 1)
    difficulty = safe_int(row.get("difficulty"), 3)
    mood = row.get("mood") or "보통"
    score = calculate_score(minutes, focus, difficulty, mood)

    return {
        "time": row.get("time") or datetime.now().strftime("%H:%M:%S"),
        "name": row.get("name") or "이름 없음",
        "team": row.get("team") or "미정",
        "subject": row.get("subject") or "미정",
        "minutes": minutes,
        "focus": focus,
        "difficulty": difficulty,
        "mood": mood,
        "place": row.get("place") or "미정",
        "features": row.get("features") or "",
        "score": score,
        "level": calculate_level(score),
        "memo": row.get("memo") or "",
    }


def sample_records():
    return [
        make_record("민준", "1팀", "Python", 45, 7, 3, "좋음", "교실", "입력 위젯, 폼", "조건문을 다시 봤어요."),
        make_record("서연", "2팀", "Streamlit", 70, 8, 3, "신남", "집", "사이드바, 차트", "차트를 넣으니 앱 같아졌어요."),
        make_record("지호", "3팀", "AI", 35, 6, 4, "보통", "도서관", "탭, 상태 저장", "점수 계산 공식을 바꾸고 싶어요."),
        make_record("하윤", "1팀", "데이터 시각화", 80, 9, 2, "좋음", "교실", "표, 차트", "필터를 추가하고 싶어요."),
    ]


def average(records, key):
    if len(records) == 0:
        return 0
    return sum(row[key] for row in records) / len(records)


def count_by(records, key):
    result = {}
    for row in records:
        value = row[key]
        if value not in result:
            result[value] = 0
        result[value] += 1
    return result


def filter_records(records, team, subject, min_score):
    filtered = []
    for row in records:
        team_ok = team == "전체" or row["team"] == team
        subject_ok = subject == "전체" or row["subject"] == subject
        score_ok = row["score"] >= min_score
        if team_ok and subject_ok and score_ok:
            filtered.append(row)
    return filtered


def counts_to_chart_rows(counts, label_name):
    rows = []
    for label, count in counts.items():
        rows.append({label_name: label, "개수": count})
    return rows


def trend_rows(records, value_key):
    rows = []
    for index, row in enumerate(records, start=1):
        rows.append({"순서": index, value_key: row[value_key]})
    return rows


@st.cache_data
def parse_csv_text(csv_text):
    reader = csv.DictReader(io.StringIO(csv_text))
    records = []
    for row in reader:
        records.append(clean_record(row))
    return records


def records_to_csv_text(records):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDNAMES)
    writer.writeheader()
    for row in records:
        safe_row = {}
        for field in FIELDNAMES:
            safe_row[field] = row.get(field, "")
        writer.writerow(safe_row)
    return output.getvalue()


def make_chat_reply(user_text, records):
    """
    과제 미션:
    아래 if 문을 참고해서 나만의 질문 규칙을 1개 이상 추가하세요.
    """
    text = user_text.lower().replace(" ", "")

    if len(records) == 0:
        return "아직 기록이 없습니다. 먼저 기록을 추가해보세요."

    if "최고" in text or "best" in text:
        best = max(records, key=lambda row: row["score"])
        return f"최고 기록은 {best['name']}님의 {best['subject']} 기록입니다. {best['score']}점입니다."

    if "평균" in text:
        return f"평균 점수는 {average(records, 'score'):.1f}점, 평균 공부 시간은 {average(records, 'minutes'):.1f}분입니다."

    if "팀" in text:
        return f"팀별 기록 개수는 {count_by(records, 'team')} 입니다."

    if "장소" in text:
        return f"장소별 기록 개수는 {count_by(records, 'place')} 입니다."

    # TODO: 여기에 나만의 규칙을 추가하세요.
    # 예: '낮은 점수'가 들어오면 가장 낮은 점수 기록을 알려주기

    return "아직 답변 규칙이 없는 질문입니다. make_chat_reply 함수에 새로운 if 문을 추가해보세요."


if "records" not in st.session_state:
    st.session_state.records = sample_records()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! Day2 과제용 학습 대시보드 도우미입니다."}
    ]

# =========================================================
# 화면 시작
# =========================================================
st.title("ver12. Day2 종합 과제: 나만의 학습 대시보드 v2")
st.caption("목표: Day1과 Day2에서 배운 기능을 합쳐 하나의 앱을 완성합니다.")
st.info("이 파일은 과제 출발점입니다. TODO 주석과 과제 안내 탭을 보고 자기 스타일로 바꿔보세요.")

# =========================================================
# 사이드바 필터
# =========================================================
st.sidebar.header("보기 설정")
selected_team = st.sidebar.selectbox("팀 필터", ["전체"] + TEAMS)
selected_subject = st.sidebar.selectbox("주제 필터", ["전체"] + SUBJECTS)
min_score = st.sidebar.slider("최소 점수", 0, 100, 0, 5)
show_table = st.sidebar.checkbox("기록 표 보기", value=True)

st.sidebar.divider()
if st.sidebar.button("예시 데이터 다시 불러오기"):
    st.session_state.records = sample_records()
    st.rerun()

if st.sidebar.button("모든 기록 삭제"):
    st.session_state.records = []
    st.rerun()

records = st.session_state.records
filtered_records = filter_records(records, selected_team, selected_subject, min_score)

# =========================================================
# 탭 구성
# =========================================================
tab_input, tab_dashboard, tab_files, tab_edit, tab_chat, tab_homework = st.tabs(
    ["1. 기록 입력", "2. 대시보드", "3. CSV", "4. 편집/삭제", "5. 채팅 도움말", "6. 과제 안내"]
)

# ---------------------------------------------------------
# 탭 1. 기록 입력
# ---------------------------------------------------------
with tab_input:
    st.subheader("새 학습 기록 입력")
    left, right = st.columns([1, 1])

    with left:
        with st.form("record_form"):
            name = st.text_input("이름", value="학생")
            team = st.selectbox("팀", TEAMS)
            subject = st.selectbox("주제", SUBJECTS)
            minutes = st.slider("공부 시간(분)", 0, 180, 45, 5)
            focus = st.slider("집중도", 1, 10, 7)
            difficulty = st.slider("난이도", 1, 5, 3)
            mood = st.selectbox("기분", ["좋음", "보통", "피곤함", "신남"])

            # Day2 과제에서 이미 하나 추가해둔 입력 항목입니다.
            # TODO: 이 항목을 바꾸거나, 입력 항목을 하나 더 추가해보세요.
            place = st.selectbox("공부 장소", ["교실", "집", "도서관", "카페", "기타"])

            features = st.multiselect(
                "사용한 기능",
                ["출력", "입력 위젯", "레이아웃", "폼", "상태 저장", "차트", "CSV", "채팅 UI"],
                default=["출력", "입력 위젯"],
            )
            memo = st.text_area("메모", value="오늘 배운 내용을 적어보세요.")
            submitted = st.form_submit_button("기록 저장")

        if submitted:
            feature_text = ", ".join(features)
            new_record = make_record(name, team, subject, minutes, focus, difficulty, mood, place, feature_text, memo)
            st.session_state.records.append(new_record)
            st.success(f"{name}님의 기록을 저장했습니다. 점수는 {new_record['score']}점입니다.")
            st.balloons()

    with right:
        preview_score = calculate_score(minutes, focus, difficulty, mood)
        preview_level = calculate_level(preview_score)
        st.metric("예상 점수", f"{preview_score}점")
        st.metric("예상 레벨", preview_level)
        st.write(f"{team}의 {name}님은 {place}에서 {subject}를 공부했습니다.")
        st.write(f"공부 시간 {minutes}분, 집중도 {focus}/10, 난이도 {difficulty}/5")

# ---------------------------------------------------------
# 탭 2. 대시보드
# ---------------------------------------------------------
with tab_dashboard:
    st.subheader("필터가 적용된 대시보드")

    if len(filtered_records) == 0:
        st.info("조건에 맞는 기록이 없습니다. 사이드바 필터를 바꿔보세요.")
    else:
        best = max(filtered_records, key=lambda row: row["score"])
        longest = max(filtered_records, key=lambda row: row["minutes"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("기록 수", len(filtered_records))
        col2.metric("평균 점수", f"{average(filtered_records, 'score'):.1f}점")
        col3.metric("평균 집중도", f"{average(filtered_records, 'focus'):.1f}/10")
        col4.metric("평균 시간", f"{average(filtered_records, 'minutes'):.1f}분")

        st.success(f"최고 기록: {best['name']} / {best['subject']} / {best['score']}점")
        st.info(f"가장 오래 공부한 기록: {longest['name']} / {longest['minutes']}분")

        left, right = st.columns(2)
        with left:
            st.write("주제별 기록 개수")
            subject_chart = counts_to_chart_rows(count_by(filtered_records, "subject"), "주제")
            st.bar_chart(subject_chart, x="주제", y="개수", use_container_width=True)

        with right:
            st.write("장소별 기록 개수")
            # TODO: 장소별 차트를 팀별 차트나 기분별 차트로 바꿔보세요.
            place_chart = counts_to_chart_rows(count_by(filtered_records, "place"), "장소")
            st.bar_chart(place_chart, x="장소", y="개수", use_container_width=True)

        st.write("기록 순서별 점수 변화")
        st.line_chart(trend_rows(filtered_records, "score"), x="순서", y="score", use_container_width=True)

    if show_table:
        st.divider()
        st.write("현재 필터 기록")
        st.dataframe(filtered_records, use_container_width=True)

# ---------------------------------------------------------
# 탭 3. CSV
# ---------------------------------------------------------
with tab_files:
    st.subheader("CSV 업로드와 다운로드")

    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if uploaded_file is not None:
        csv_text = uploaded_file.read().decode("utf-8-sig")
        uploaded_records = parse_csv_text(csv_text)
        st.write(f"업로드에서 읽은 기록 수: {len(uploaded_records)}개")
        st.dataframe(uploaded_records, use_container_width=True)

        if st.button("업로드 기록으로 교체"):
            st.session_state.records = uploaded_records
            st.rerun()

    if len(records) == 0:
        st.info("다운로드할 기록이 없습니다.")
    else:
        csv_text = records_to_csv_text(records)
        st.download_button(
            "현재 전체 기록 CSV 다운로드",
            data=csv_text.encode("utf-8-sig"),
            file_name="my_day2_records.csv",
            mime="text/csv",
        )

# ---------------------------------------------------------
# 탭 4. 편집/삭제
# ---------------------------------------------------------
with tab_edit:
    st.subheader("표 편집과 삭제")

    if len(records) == 0:
        st.info("편집할 기록이 없습니다.")
    else:
        edited_records = st.data_editor(records, num_rows="dynamic", use_container_width=True, key="homework_editor")

        if st.button("편집 내용 저장 + 점수 재계산"):
            cleaned = []
            for row in edited_records:
                cleaned.append(clean_record(row))
            st.session_state.records = cleaned
            st.rerun()

        st.divider()
        labels = []
        for index, row in enumerate(records):
            labels.append(f"{index + 1}. {row['name']} / {row['subject']} / {row['score']}점")
        selected = st.selectbox("삭제할 기록 선택", labels)
        selected_index = labels.index(selected)

        confirm_delete = st.checkbox("정말 삭제하겠습니다")
        if st.button("선택한 기록 삭제"):
            if confirm_delete:
                st.session_state.records.pop(selected_index)
                st.rerun()
            else:
                st.warning("삭제하려면 확인 체크박스를 먼저 눌러주세요.")

# ---------------------------------------------------------
# 탭 5. 채팅 도움말
# ---------------------------------------------------------
with tab_chat:
    st.subheader("채팅형 도움말")
    st.caption("실제 AI가 아니라, make_chat_reply 함수의 규칙에 따라 답합니다.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_text = st.chat_input("질문을 입력하세요. 예: 평균 알려줘")
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        reply = make_chat_reply(user_text, records)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("채팅 기록 삭제"):
        st.session_state.messages = [
            {"role": "assistant", "content": "채팅 기록을 지웠습니다. 다시 질문해보세요."}
        ]
        st.rerun()

# ---------------------------------------------------------
# 탭 6. 과제 안내
# ---------------------------------------------------------
with tab_homework:
    st.subheader("Day2 종합 과제 안내")

    st.markdown("### 필수 미션")
    st.write("1. 앱 제목과 설명을 자기 주제에 맞게 바꾸기")
    st.write("2. 입력 항목을 1개 이상 추가하거나, 기존 `공부 장소` 항목을 자기 주제에 맞게 바꾸기")
    st.write("3. 필터 1개 이상 추가 또는 수정하기")
    st.write("4. 차트 1개 이상 기준 바꾸기. 예: 장소별 → 기분별, 주제별 → 팀별")
    st.write("5. CSV 다운로드 버튼 유지하기")
    st.write("6. 표 편집 또는 선택 삭제 기능 유지하기")
    st.write("7. `make_chat_reply` 함수에 채팅 답변 규칙 1개 이상 추가하기")
    st.write("8. 실행 화면 캡처 1장 제출하기")
    st.write("9. 내가 수정한 코드 5줄 이상 설명하기")

    st.markdown("### 선택 미션")
    st.write("- 가장 낮은 점수 기록 찾기")
    st.write("- 팀별 평균 점수 차트 만들기")
    st.write("- 기분별 추천 문장 만들기")
    st.write("- 필터된 기록만 CSV로 다운로드하기")
    st.write("- 사이드바에 앱 사용 설명 추가하기")

    st.markdown("### 제출물")
    st.write("1. 완성한 `.py` 파일")
    st.write("2. 실행 화면 캡처 1장")
    st.write("3. 추가/수정한 기능 설명 3줄")
    st.write("4. 수정한 코드 5줄 이상")
    st.write("5. 어려웠던 점 1줄, 다음에 더 해보고 싶은 점 1줄")

    with st.expander("힌트: 가장 낮은 점수 기록 찾기"):
        st.code(
            '''
lowest = min(records, key=lambda row: row["score"])
st.write(f"가장 낮은 점수: {lowest['name']} / {lowest['score']}점")
'''.strip(),
            language="python",
        )

    with st.expander("힌트: 기분별 차트 만들기"):
        st.code(
            '''
mood_chart = counts_to_chart_rows(count_by(filtered_records, "mood"), "기분")
st.bar_chart(mood_chart, x="기분", y="개수", use_container_width=True)
'''.strip(),
            language="python",
        )
