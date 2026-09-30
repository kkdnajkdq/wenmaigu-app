import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="文脉估 · 非遗数据资产AI估值平台", layout="wide")

st.title("文脉估 · 非遗数据资产AI估值平台")
st.write("用AI把非遗数据变成银行看得懂的信用资产")

# 侧边栏：数据录入
with st.sidebar:
    st.header("📝 数据录入")
    heritage_level = st.selectbox("非遗级别", ["国家级", "省级", "市级"])
    inheritor_level = st.selectbox("传承人资质", ["国家级传承人", "省级传承人", "无"])
    digital_items = st.number_input("已数字化数据条目数", min_value=0, value=5000)
    video_views = st.number_input("近12月短视频总播放量（万）", min_value=0, value=200)
    ecommerce_sales = st.number_input("近12月线上销售额（万元）", min_value=0, value=50)
    license_count = st.number_input("已发生IP授权次数", min_value=0, value=2)

# 估值计算逻辑
level_map = {"国家级": 1.0, "省级": 0.7, "市级": 0.4}
inheritor_map = {"国家级传承人": 1.0, "省级传承人": 0.8, "无": 0.5}

cultural_score = level_map[heritage_level] * 0.4 + inheritor_map[inheritor_level] * 0.3 + 0.3
economic_score = min(video_views / 1000, 1.0) * 0.3 + min(ecommerce_sales / 500, 1.0) * 0.3 + min(license_count / 10, 1.0) * 0.4

base_cost = digital_items * 200  # 每条数据平均采集成本200元
estimated_value = base_cost + cultural_score * economic_score * 500000

st.divider()

# 展示结果
st.subheader("📊 AI估值结果")
col1, col2, col3 = st.columns(3)
col1.metric("估值下限（万元）", f"{estimated_value * 0.7 / 10000:.1f}")
col2.metric("估值中位数（万元）", f"{estimated_value / 10000:.1f}")
col3.metric("估值上限（万元）", f"{estimated_value * 1.3 / 10000:.1f}")

# 雷达图
categories = ['文化价值', '经济价值', '数据规模', '传播热度', '变现能力']
values = [cultural_score, economic_score, min(digital_items/20000, 1), min(video_views/1000, 1), min(license_count/10, 1)]

fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
st.plotly_chart(fig)