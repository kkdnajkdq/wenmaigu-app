# agents.py

class DataCleaningAgent:
    """数据采集与清洗Agent"""
    def __init__(self):
        self.name = "数据清洗Agent"
        self.log = []

    def process(self, raw_data):
        cleaned = {}
        for key, value in raw_data.items():
            if value < 0:
                self.log.append(f"异常值：{key}={value}，已修正为0")
                cleaned[key] = 0
            else:
                cleaned[key] = value
        self.log.append(f"已处理{len(raw_data)}项输入，发现{len([v for v in raw_data.values() if v < 0])}个异常值")
        return cleaned


class CulturalValueAgent:
    """文化价值评估Agent：计算CVI"""
    def __init__(self):
        self.name = "文化价值评估Agent"

    def evaluate(self, heritage_level, inheritor_level, digital_items):
        level_map = {"国家级": 1.0, "省级": 0.7, "市级": 0.4}
        inheritor_map = {"国家级传承人": 1.0, "省级传承人": 0.8, "无": 0.5}

        # 本体价值（35%）
        ontology = level_map[heritage_level] * inheritor_map[inheritor_level] * 0.35
        # 衍生潜力（30%）
        derivative = min(digital_items / 20000, 1.0) * 0.30
        # 稀缺性（15%）
        scarcity = max(0, 1 - digital_items / 20000) * 0.15
        # 功能价值（10%）
        function = 0.5 * 0.10
        # 传播价值（10%）
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
        economic_score = views_score * 0.3 + sales_score * 0.3 + license_score * 0.4
        return round(economic_score, 4)


class ValuationAgent:
    """估值融合Agent：V = Vb × (1 + α × CVI)"""
    def __init__(self):
        self.name = "估值融合Agent"

    def fuse(self, cvi, economic_score, digital_items, heritage_level):
        alpha_map = {"国家级": 0.5, "省级": 0.4, "市级": 0.3}
        alpha = alpha_map[heritage_level]

        base_cost = digital_items * 200
        vb = base_cost + economic_score * 300000
        estimated_value = vb * (1 + alpha * cvi)

        return {
            "lower": round(estimated_value * 0.7 / 10000, 1),
            "median": round(estimated_value / 10000, 1),
            "upper": round(estimated_value * 1.3 / 10000, 1),
            "alpha": alpha,
            "cvi": cvi
        }


class ReportAgent:
    """报告生成Agent"""
    def __init__(self):
        self.name = "报告生成Agent"

    def generate(self, valuation_result, heritage_level, inheritor_level):
        report = f"""
        非遗数据资产估值报告
        ====================
        非遗级别：{heritage_level}
        传承人资质：{inheritor_level}
        文化价值指数（CVI）：{valuation_result['cvi']}
        文化价值系数（α）：{valuation_result['alpha']}
        估值下限：{valuation_result['lower']}万元
        估值中位数：{valuation_result['median']}万元
        估值上限：{valuation_result['upper']}万元
        置信等级：B级（基于原型模型，待真实数据校准）
        说明：本报告仅供参考，最终贷款额度以银行审批为准。
        """
        return report