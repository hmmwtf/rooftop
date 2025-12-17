from __future__ import annotations

import io
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from core.models import SimulationResult

class ReportService:
    """Create PDF/Excel artifacts from SimulationResult.

    MVP 버전: 간단한 PDF/Excel 생성.
    추후 템플릿/디자인은 UI팀 스타일에 맞춰 개선 가능.
    """

    def build_pdf(self, result: SimulationResult) -> tuple[bytes, str]:
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        w, h = A4

        y = h - 60
        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, y, "옥상이몽 시뮬레이션 리포트 (MVP)")
        y -= 24
        c.setFont("Helvetica", 10)
        c.drawString(60, y, f"Generated: {datetime.utcnow().isoformat()}Z")
        y -= 18
        c.drawString(60, y, f"Engine: {result.engine_version} | Coeff set: {result.coefficient_set_version}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, "입력값")
        y -= 18
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"- 옥상 면적(㎡): {result.roof_area_m2:,.2f}")
        y -= 16
        c.drawString(60, y, f"- 녹화 유형: {result.greening_type}")
        y -= 16
        c.drawString(60, y, f"- 녹화 비율: {result.coverage_ratio:.2%}")
        y -= 26

        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, "결과")
        y -= 18
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"- 녹화 면적(㎡): {result.green_area_m2:,.2f}")
        y -= 16
        c.drawString(60, y, f"- CO₂ 흡수(kg/년): {result.co2_absorption_kg_per_year:,.2f}")
        y -= 16
        c.drawString(60, y, f"- 온도 저감(℃): {result.temp_reduction_c:,.2f}")
        y -= 16
        c.drawString(60, y, f"- 표면온도(전/후): {result.baseline_surface_temp_c:.1f}℃ → {result.after_surface_temp_c:.1f}℃")
        y -= 16
        c.drawString(60, y, f"- 소나무 환산(그루): {result.tree_equivalent_count}")
        y -= 30

        c.setFont("Helvetica", 9)
        c.drawString(60, y, "※ 본 리포트는 MVP 산출물이며, 실제 정책/심사 제출 전 계수·근거 검증이 필요합니다.")
        c.showPage()
        c.save()

        pdf_bytes = buf.getvalue()
        filename = "okssangimong_report.pdf"
        return pdf_bytes, filename

    def build_excel(self, result: SimulationResult) -> tuple[bytes, str]:
        buf = io.BytesIO()

        inputs = pd.DataFrame(
            [
                {"key": "roof_area_m2", "value": result.roof_area_m2},
                {"key": "greening_type", "value": result.greening_type},
                {"key": "coverage_ratio", "value": result.coverage_ratio},
                {"key": "baseline_surface_temp_c", "value": result.baseline_surface_temp_c},
            ]
        )

        outputs = pd.DataFrame(
            [
                {"key": "green_area_m2", "value": result.green_area_m2},
                {"key": "co2_absorption_kg_per_year", "value": result.co2_absorption_kg_per_year},
                {"key": "temp_reduction_c", "value": result.temp_reduction_c},
                {"key": "after_surface_temp_c", "value": result.after_surface_temp_c},
                {"key": "tree_equivalent_count", "value": result.tree_equivalent_count},
            ]
        )

        meta = pd.DataFrame(
            [
                {"key": "engine_version", "value": result.engine_version},
                {"key": "coefficient_set_version", "value": result.coefficient_set_version},
            ]
        )

        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            inputs.to_excel(writer, index=False, sheet_name="inputs")
            outputs.to_excel(writer, index=False, sheet_name="outputs")
            meta.to_excel(writer, index=False, sheet_name="meta")

        return buf.getvalue(), "okssangimong_result.xlsx"
