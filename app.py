import streamlit as st
import plotly.graph_objects as go
from agents import (DataCleaningAgent, CulturalValueAgent,
                    EconomicValueAgent, ValuationAgent, ReportAgent)

st.set_page_config(page_title="文脉估 · 非遗数据资产AI估值平台", layout="wide")
st.title("文脉估 · 非遗数据资产AI估值平台")
st.write("用AI把非遗数据变成银行看得懂的信用资产")

with st.sidebar:
    st.header("📝 数据录入")
    heritage_level = st.selectbox("非遗级别", ["国家级", "省级", "市级"])
    inheritor_level = st.selectbox("传承人资质", ["国家级传承人", "省级传承人", "无"])
    digital_items = st.number_input("已数字化数据条目数", min_value=0, value=5000)
    video_views = st.number_input("近12月短视频总播放量（万）", min_value=0, value=200)
    ecommerce_sales = st.number_input("近12月线上销售额（万元）", min_value=0, value=50)
    license_count = st.number_input("已发生IP授权次数", min_value=0, value=2)

if st.button("开始估值"):
    # Agent 1：数据清洗
    cleaner = DataCleaningAgent()
    cleaned = cleaner.process({
        "digital_items": digital_items, "video_views": video_views,
        "ecommerce_sales": ecommerce_sales, "license_count": license_count
    })
    st.info(f"🔹 {cleaner.name}：{cleaner.log[-1]}")

    # Agent 2：文化价值评估
    cultural_agent = CulturalValueAgent()
    cvi = cultural_agent.evaluate(heritage_level, inheritor_level, cleaned["digital_items"])
    st.info(f"🔹 {cultural_agent.name}：CVI = {cvi}")

    # Agent 3：经济价值评估
    economic_agent = EconomicValueAgent()
    economic_score = economic_agent.evaluate(
        cleaned["video_views"], cleaned["ecommerce_sales"], cleaned["license_count"])
    st.info(f"🔹 {economic_agent.name}：经济价值得分 = {economic_score}")

    # Agent 4：估值融合
    valuation_agent = ValuationAgent()
    result = valuation_agent.fuse(cvi, economic_score, cleaned["digital_items"], heritage_level)
    st.info(f"🔹 {valuation_agent.name}：估值计算完成")

    # 展示结果
    st.divider()
    st.subheader("📊 AI估值结果")
    col1, col2, col3 = st.columns(3)
    col1.metric("估值下限（万元）", result["lower"])
    col2.metric("估值中位数（万元）", result["median"])
    col3.metric("估值上限（万元）", result["upper"])

    # 雷达图
    categories = ['文化价值', '经济价值', '数据规模', '传播热度', '变现能力']
    values = [cvi, economic_score, min(cleaned["digital_items"]/20000, 1),
              min(cleaned["video_views"]/1000, 1), min(cleaned["license_count"]/10, 1)]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
    st.plotly_chart(fig)

    # Agent 5：报告生成
    report_agent = ReportAgent()
    report_text = report_agent.generate(result, heritage_level, inheritor_level)
    with st.expander("📄 查看完整估值报告"):
        st.text(report_text)