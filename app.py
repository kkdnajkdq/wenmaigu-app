# app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from agents import (
    DataLoadingAgent,
    DataCleaningAgent,
    CulturalValueAgent,
    EconomicValueAgent,
    ValuationAgent,
    ReportAgent,
)

st.set_page_config(
    page_title="文脉估 · 非遗数据资产AI估值平台",
    layout="wide",
)
st.title("文脉估 · 非遗数据资产AI估值平台")
st.write("用AI把非遗数据变成银行看得懂的信用资产")

# 初始化 session_state
if 'collected_data' not in st.session_state:
    st.session_state['collected_data'] = pd.DataFrame()

# ============ 侧边栏：数据加载 + 数据录入 ============
with st.sidebar:
    st.header("📂 数据加载")

    if st.button("加载已采集数据（CSV）"):
        loader = DataLoadingAgent()
        df = loader.load("非遗项目数据.csv")
        if not df.empty:
            st.session_state['collected_data'] = df
            st.success(f"已加载 {len(df)} 条数据")
        else:
            st.error(loader.log[-1] if loader.log else "加载失败")

    st.divider()
    st.header("📝 数据录入")

    selected_project = "（手动输入）"
    # 显示已加载的数据，并允许选择
    if not st.session_state['collected_data'].empty:
        df = st.session_state['collected_data']
        st.dataframe(df[['项目名称', '级别', '地区']].head())
        project_options = df['项目名称'].tolist()
        selected_project = st.selectbox(
            "选择要估值的项目", 
            ["（手动输入）"] + project_options, 
            key="project_selector"
        )

    # 根据选中项目，提取默认值
    default_level = "国家级"
    default_views = 200
    default_sales = 50
    default_licenses = 2
    default_inheritor = "国家级传承人"

    if selected_project != "（手动输入）":
        row = df[df['项目名称'] == selected_project].iloc[0]
        raw_level = row.get('级别', '国家级')
        default_level = raw_level if raw_level in ["国家级", "省级", "市级"] else "国家级"
        default_views = int(row.get('近3月播放量(万)', 200))
        default_sales = int(row.get('近3月销售额(万)', 50))
        default_licenses = int(row.get('IP授权次数', 2))

    # 使用动态 key：确保选择不同项目时，输入框强制刷新
    heritage_level = st.selectbox(
        "非遗级别", ["国家级", "省级", "市级"],
        index=["国家级", "省级", "市级"].index(default_level),
        key=f"level_{selected_project}"  # 动态key，强制刷新
    )
    inheritor_level = st.selectbox(
        "传承人资质", ["国家级传承人", "省级传承人", "无"],
        index=["国家级传承人", "省级传承人", "无"].index(default_inheritor),
        key=f"inheritor_{selected_project}"
    )
    digital_items = st.number_input(
        "已数字化数据条目数", min_value=0, value=5000,
        key=f"digital_{selected_project}"
    )
    video_views = st.number_input(
        "近12月短视频总播放量（万）", min_value=0, value=default_views,
        key=f"views_{selected_project}"
    )
    ecommerce_sales = st.number_input(
        "近12月线上销售额（万元）", min_value=0, value=default_sales,
        key=f"sales_{selected_project}"
    )
    license_count = st.number_input(
        "已发生IP授权次数", min_value=0, value=default_licenses,
        key=f"licenses_{selected_project}"
    )

# ============ 主区域：估值流程 ============
if st.button("开始估值", type="primary"):
    # Agent 0：数据加载
    if st.session_state['collected_data'].empty:
        st.info("🔹 数据加载Agent：尚未加载数据，建议先在左侧点击“加载已采集数据”")
    else:
        st.info(f"🔹 数据加载Agent：已加载 {len(st.session_state['collected_data'])} 条数据")

    # Agent 1：数据清洗
    cleaner = DataCleaningAgent()
    cleaned = cleaner.process({
        "digital_items": digital_items,
        "video_views": video_views,
        "ecommerce_sales": ecommerce_sales,
        "license_count": license_count,
    })
    st.info(f"🔹 {cleaner.name}：{cleaner.log[-1]}")

    # Agent 2：文化价值评估
    cultural_agent = CulturalValueAgent()
    cvi = cultural_agent.evaluate(heritage_level, inheritor_level, cleaned["digital_items"])
    st.info(f"🔹 {cultural_agent.name}：CVI = {cvi}")

    # Agent 3：经济价值评估
    economic_agent = EconomicValueAgent()
    economic_score = economic_agent.evaluate(
        cleaned["video_views"], cleaned["ecommerce_sales"], cleaned["license_count"]
    )
    st.info(f"🔹 {economic_agent.name}：经济价值得分 = {economic_score}")

    # Agent 4：估值融合
    valuation_agent = ValuationAgent()
    result = valuation_agent.fuse(cvi, economic_score, cleaned["digital_items"], heritage_level)
    st.info(f"🔹 {valuation_agent.name}：估值计算完成")

    # 展示估值结果
    st.divider()
    st.subheader("📊 AI估值结果")
    col1, col2, col3 = st.columns(3)
    col1.metric("估值下限（万元）", result["lower"])
    col2.metric("估值中位数（万元）", result["median"])
    col3.metric("估值上限（万元）", result["upper"])

    # 雷达图
    categories = ['文化价值', '经济价值', '数据规模', '传播热度', '变现能力']
    values = [
        cvi, economic_score,
        min(cleaned["digital_items"] / 20000, 1),
        min(cleaned["video_views"] / 1000, 1),
        min(cleaned["license_count"] / 10, 1),
    ]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
    )
    st.plotly_chart(fig)

    # Agent 5：报告生成
    report_agent = ReportAgent()
    report_text = report_agent.generate(result, heritage_level, inheritor_level, economic_score)
    with st.expander("📄 查看完整估值报告"):
        st.text(report_text)