import streamlit as st
import numpy as np
import plotly.graph_objects as go
import evaluation_processor

model,tokenizer = evaluation_processor.load_model()
# 페이지를 Wide 모드로 설정
st.set_page_config(page_title="PPP - 소셜 미디어 게시물 인기도 예측기", layout="wide")

# 별점 계산을 위한 함수
def get_star_rating(score):
    full_stars = int(score)
    half_star = score - full_stars
    return "★" * full_stars + ("½" if half_star >= 0.5 else "") + "☆" * (5 - full_stars - (1 if half_star >= 0.5 else 0))

# 박스 형태 점수 표시 함수
def score_box(score):
    filled = "■" * score
    empty = "□" * (10 - score)
    return f"{filled}{empty}"

# 1단: 헤더 및 서비스 소개
st.title("PPP - 소셜 미디어 게시물 인기도 예측기")
st.subheader("당신의 게시물을 더 효과적으로 만들어 보세요!")

# 간단한 서비스 설명
st.info("""
    PPP를 사용하여 LinkedIn 게시물을 분석하고, 성과를 개선하기 위한 개인화된 피드백과 
    예상 결과를 예측해드립니다.
""")

# 2단: 입력 및 스타일 선택
st.markdown("### LinkedIn 게시물 입력 및 스타일 선택:")

# 입력과 슬라이더를 4:1 비율로 배치
col1, col2 = st.columns([4, 1])

with col1:
    # 포스트 입력창의 높이를 3배로 설정
    post_input = st.text_area("게시물을 입력하세요", 
                              placeholder="여기에 LinkedIn 게시물을 복사하여 붙여넣으세요...", 
                              height=300)

with col2:
    st.markdown("#### 스타일 선택:")
    tone = st.slider("Tone (Official <-> Casual)", 0, 10, 5)
    purpose = st.slider("Purpose (Informative <-> Motivational)", 0, 10, 5)
    engagement = st.slider("Engagement (Engaging <-> Descriptive)", 0, 10, 5)

# 분석 버튼을 입력 창 바로 아래에 배치
analyze_button = st.button("게시물 분석")

# 3단: 분석 결과 처리
st.markdown("---")

if analyze_button:
    if post_input.strip() == "":
        st.error("분석을 위해 LinkedIn 게시물을 입력해주세요.")
    else:
        
        # 평가 결과를 처리하는 함수 호출
        results = evaluation_processor.process_evaluation_results(post_input,model,tokenizer)
        
        # 평균 점수 계산
        user_score_average = np.mean(results["scores"])
        dummy_average = 5.8  # 더미 사용자 평균 점수
        
        # 평균 점수와 사용자 평균 점수를 별점으로 변환
        user_star_rating = get_star_rating(user_score_average / 2)  # 10점 만점을 5점 만점으로 변환
        dummy_star_rating = get_star_rating(dummy_average / 2)

        # 평균 점수와 별점 표시
        st.markdown("### 📊 평균 점수")
        st.success(f"이 게시물의 평균 점수: **{user_score_average:.1f}** ({user_star_rating})")
        st.info(f"서비스를 이용한 사용자들의 평균 점수: **{dummy_average:.1f}** ({dummy_star_rating})")

        # 4단: 레이더 차트와 세부 분석을 나란히 표시
        st.markdown("### 분석 결과")
        col1, col2 = st.columns([1, 1])

        # 첫 번째 컬럼: 레이더 차트
        with col1:
            st.markdown("#### 스타일 개요")
            categories = results["categories"]
            scores = results["scores"]
            
            # Plotly로 레이더 차트 생성
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],  # 마지막 값을 첫번째 값으로 연결해 레이더 차트를 닫음
                theta=categories + [categories[0]],  # 카테고리의 시작과 끝을 연결
                fill='toself',
                line=dict(color='blue')
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 10])
                ),
                showlegend=False,
                template="plotly_white"  # 깔끔한 UI를 위한 Plotly 스타일
            )

            st.plotly_chart(fig)

        # 두 번째 컬럼: 세부 분석 (토글 형태로 표시)
        with col2:
            st.markdown("#### 세부 분석")
            for i, category in enumerate(results["categories"]):
                with st.expander(f"{category} -  {results['scores'][i]}/10"):
                    st.write(f"**설명:** {results['explanations'][i]}")
                    st.warning(f"**개선 제안:** {results['suggestions'][i]}")

        # 5단: 해시태그 추천 및 참조 필요 여부를 카드 형태로 좌우 분리
        st.markdown("### 추가 분석 정보")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**해시태그 추천**")
            st.success(f"추천 해시태그: {', '.join(results['additional_analysis']['recommended_hashtags'])}")

        with col2:
            st.markdown("**참조 필요 여부**")
            st.info(f"참조 필요 여부: {'필요' if results['additional_analysis']['references_needed'] else '필요하지 않음'}")

        # 6단: 원본과 개선본 비교 및 강조
        st.markdown("### 원본과 개선본 비교")
        original_text = post_input
        improved_text = """
        여기에서 개선된 게시물 텍스트를 예로 추가할 수 있습니다. 
        변경된 부분 또는 추가된 부분을 하이라이트해보세요. 예를 들어, 중요한 변경사항은 **굵게** 표시.
        """

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**원본**")
            st.write(original_text)

        with col2:
            st.markdown("**개선본**")
            st.write(improved_text)

        # 개선된 텍스트의 변경된 부분 강조 (예시로 굵게 표시)
        improved_highlighted = improved_text.replace("개선된", "**개선된**").replace("추가된 부분", "**추가된 부분**")
        st.markdown(f"**개선된 부분 강조**: {improved_highlighted}")
else:
    st.info("분석 버튼을 눌러 분석 결과를 확인하세요.")
