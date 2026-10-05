# agents.py
import pandas as pd
from datetime import datetime


class DataLoadingAgent:
    """数据加载Agent：从CSV文件读取已采集的数据"""
    def __init__(self):
        self.name = "数据加载Agent"
        self.log = []

    def load(self, file_path="非遗项目数据.csv"):
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            # 再次确保缺失值被填充（防止手工修改CSV时遗漏）
            df['级别'] = df['级别'].fillna('国家级')
            df['类别'] = df['类别'].fillna('传统技艺')
            df['地区'] = df['地区'].fillna('中国')
            self.log.append(f"成功加载 {len(df)} 条数据")
            return df
        except FileNotFoundError:
            self.log.append("未找到CSV文件，请先运行spider.py生成数据")
            return pd.DataFrame()
        except Exception as e:
            self.log.append(f"加载失败：{e}")
            return pd.DataFrame()


class DataCleaningAgent:
    """数据清洗与验证Agent"""
    def __init__(self):
        self.name = "数据清洗Agent"
        self.log = []

    def process(self, raw_data):
        cleaned = {}
        anomalies = 0
        for key, value in raw_data.items():
            try:
                v = float(value)
            except (TypeError, ValueError):
                v = 0
            if v < 0:
                anomalies += 1
                v = 0
            cleaned[key] = v
        self.log.append(f"已处理{len(raw_data)}项输入，发现{anomalies}个异常值")
        return cleaned


class CulturalValueAgent:
    """文化价值评估Agent：计算CVI"""
    def __init__(self):
        self.name = "文化价值评估Agent"

    def evaluate(self, heritage_level, inheritor_level, digital_items):
        level_map = {"国家级": 1.0, "省级": 0.7, "市级": 0.4}
        inheritor_map = {"国家级传承人": 1.0, "省级传承人": 0.8, "无": 0.5}

        ontology = level_map.get(heritage_level, 0.5) * \
                   inheritor_map.get(inheritor_level, 0.5) * 0.35
        derivative = min(digital_items / 20000, 1.0) * 0.30
        scarcity = max(0, 1 - digital_items / 20000) * 0.15
        function = 0.5 * 0.10
        communication = 0.5 * 0.10

        cvi = ontology + derivative + scarcity + function + communication
        return round(cvi, 4)


class EconomicValueAgent:
    """经济价值评估Agent"""
    def __init__(self):
        self.name = "经济价值评估Agent"

    def evaluate(self, video_views, ecommerce_sales, license_count):
        views_score = min(video_views / 1000, 1.0)
        sales_score = min(ecommerce_sales / 500, 1.0)
        license_score = min(license_count / 10, 1.0)
        economic_score = (views_score * 0.3 +
                          sales_score * 0.3 +
                          license_score * 0.4)
        return round(economic_score, 4)


class ValuationAgent:
    """估值融合Agent：V = Vb × (1 + α × CVI)"""
    def __init__(self):
        self.name = "估值融合Agent"

    def fuse(self, cvi, economic_score, digital_items, heritage_level):
        alpha_map = {"国家级": 0.5, "省级": 0.4, "市级": 0.3}
        alpha = alpha_map.get(heritage_level, 0.3)

        base_cost = digital_items * 200
        vb = base_cost + economic_score * 300000
        estimated_value = vb * (1 + alpha * cvi)

        return {
            "lower": round(estimated_value * 0.7 / 10000, 1),
            "median": round(estimated_value / 10000, 1),
            "upper": round(estimated_value * 1.3 / 10000, 1),
            "alpha": alpha,
            "cvi": cvi,
        }


class ReportAgent:
    """报告生成Agent"""
    def __init__(self):
        self.name = "报告生成Agent"

    def generate(self, valuation_result, heritage_level,
                 inheritor_level, economic_score):
        report = f"""
非遗数据资产估值报告
====================
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

一、基本信息
    非遗级别：{heritage_level}
    传承人资质：{inheritor_level}

二、估值指标
    文化价值指数（CVI）：{valuation_result['cvi']}
    文化价值系数（α）：{valuation_result['alpha']}
    经济价值得分：{economic_score}

三、估值结果（万元）
    估值下限：{valuation_result['lower']}
    估值中位数：{valuation_result['median']}
    估值上限：{valuation_result['upper']}

四、关键影响因素
    1. 文化价值维度贡献最大，非遗级别和传承人资质是核心锚点
    2. 经济价值维度中，IP授权次数的边际影响最显著
    3. 数据规模（数字化条目数）通过采集成本项影响基础估值

五、提升建议
    1. 持续积累数字化影像、纹样数据库，扩大数据规模
    2. 加强短视频平台内容运营，提升传播热度得分
    3. 积极拓展IP授权合作，提高变现能力得分

六、置信等级与说明
    置信等级：B级（基于原型模型，待真实数据校准）
    说明：本报告仅供参考，最终贷款额度以银行审批为准。
    输出格式参照GB/T 47949-2026、GB/T 47950-2026规范。
        """
        return report