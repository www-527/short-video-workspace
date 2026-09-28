from __future__ import annotations

import json
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PACKAGE_ROOT = Path(os.environ["WASHCUT_PACKAGE_ROOT"])
PLAN_PATH = PACKAGE_ROOT / "manifests" / "package-plan.json"
EVIDENCE_DIR = PACKAGE_ROOT / "sources" / "license-evidence"
FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")


def register_font() -> str:
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Chinese font is missing: {FONT_PATH}")
    pdfmetrics.registerFont(TTFont("MicrosoftYaHei", str(FONT_PATH), subfontIndex=0))
    return "MicrosoftYaHei"


FONT = register_font()
STYLES = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "TitleZh",
    parent=STYLES["Title"],
    fontName=FONT,
    fontSize=18,
    leading=25,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17233C"),
    spaceAfter=8 * mm,
)
HEADING = ParagraphStyle(
    "HeadingZh",
    parent=STYLES["Heading2"],
    fontName=FONT,
    fontSize=12,
    leading=18,
    textColor=colors.HexColor("#0B5FFF"),
    spaceBefore=4 * mm,
    spaceAfter=2 * mm,
)
BODY = ParagraphStyle(
    "BodyZh",
    parent=STYLES["BodyText"],
    fontName=FONT,
    fontSize=9.5,
    leading=15,
    textColor=colors.HexColor("#202737"),
    wordWrap="CJK",
)
SMALL = ParagraphStyle(
    "SmallZh",
    parent=BODY,
    fontSize=8,
    leading=12,
    textColor=colors.HexColor("#586174"),
)
NOTICE = ParagraphStyle(
    "NoticeZh",
    parent=BODY,
    fontSize=9.5,
    leading=15,
    backColor=colors.HexColor("#FFF5D9"),
    borderColor=colors.HexColor("#F1B928"),
    borderWidth=0.8,
    borderPadding=8,
    spaceAfter=5 * mm,
)


def paragraph(value: object, style: ParagraphStyle = BODY) -> Paragraph:
    text = str(value or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(text, style)


def write_pdf(path: Path, title: str, story: list[object]) -> None:
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=17 * mm,
        title=title,
        author="Washcut internal test package",
        subject="Source and license review evidence",
    )
    doc.build([paragraph(title, TITLE), *story])


def metadata_table(rows: list[tuple[str, object]]) -> Table:
    data = [[paragraph(label, SMALL), paragraph(value, BODY)] for label, value in rows]
    table = Table(data, colWidths=[39 * mm, 132 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F6FB")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D7DCE5")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def license_story(kind: str) -> list[object]:
    if kind == "license":
        title = "Pexels License 复核记录"
        rows = [
            ("官方页面", "https://www.pexels.com/license/"),
            ("复核日期", "2026-09-01"),
            ("许可名称", "Pexels License"),
            ("允许事项", "Pexels 页面说明照片和视频可免费使用、通常无需署名，并允许修改。"),
            ("主要限制", "不得暗示画面中的人物或品牌为产品背书；不得把未作实质创作处理的素材作为独立素材转售或分发；不得用于商标或服务标识。"),
            ("本包结论", "仅用于本机内部 AI 链路测试。testOnly=true；publishable=false。"),
        ]
    else:
        title = "Pexels Terms of Service 复核记录"
        rows = [
            ("官方页面", "https://www.pexels.com/terms-of-service/"),
            ("页面标注更新时间", "2024-11-15"),
            ("复核日期", "2026-09-01"),
            ("内容许可", "条款第 5 节授予下载、使用、复制、修改或适配内容的全球、非独占、免版税许可，但须遵守禁止用途。"),
            ("第三方权利", "条款提醒人物、商标、品牌、建筑、隐私和其他第三方权利可能另需授权，判断责任由使用者承担。"),
            ("自动化边界", "条款禁止未经授权的数据挖掘、抓取和批量或系统性复制。本测试包没有再次抓取或批量下载素材。"),
            ("本包结论", "不声称完成商用发布权清理；全部文件仅作内部测试。"),
        ]
    return [
        paragraph(
            "证据类型：人工/AI 复核记录。自动化打印官方 Pexels 页面时触发安全验证，因此本文件不冒充网页原样截图；请使用下列官方 URL 在需要发布前再次人工复核。",
            NOTICE,
        ),
        metadata_table(rows),
        paragraph("记录依据", HEADING),
        paragraph("本记录基于 2026-09-01 访问到的 Pexels 官方页面内容制作，并与测试包的来源清单、文件哈希和不可发布标记一并保存。"),
    ]


def source_story(source: dict[str, object]) -> list[object]:
    rows = [
        ("素材页面", source["sourcePageUrl"]),
        ("作品标题", source["sourceTitle"]),
        ("作者/上传者", source["sourceAuthor"]),
        ("本地源文件", source["fileName"]),
        ("源文件 SHA-256", source["sourceSha256"]),
        ("下载日期", "2026-08-12"),
        ("许可复核日期", "2026-09-01"),
        ("许可", "Pexels License - https://www.pexels.com/license/"),
        ("直接下载 URL", "未从原下载记录中恢复；因此不可标记为可发布。"),
        ("可识别人脸", str(bool(source["containsFace"])).lower()),
        ("可见车牌", str(bool(source["containsPlate"])).lower()),
        ("可见商标/产品特征", str(bool(source["containsTrademark"])).lower()),
        ("允许公开发布", "false"),
    ]
    return [
        paragraph(
            "证据类型：来源复核记录。Pexels 对自动化浏览器显示安全验证页，因此本 PDF 不是网页截图。标题和作者信息来自上列官方素材页面；源文件身份由本地 SHA-256 固定。发布前必须在普通浏览器中重新打开官方页面核对。",
            NOTICE,
        ),
        metadata_table(rows),
        paragraph("用途与修改", HEADING),
        paragraph("用于洗车视频 AI 理解、排序、字幕和渲染的本机内部测试。输出会裁切为 9:16、替换音轨；部分测试片加入始终带“测试数据”的优惠或到店字卡。"),
        Spacer(1, 3 * mm),
        paragraph("权利边界", HEADING),
        paragraph("素材许可不等于人物、商标、车辆设计、场地和其他第三方权利均已清理。本包及所有衍生片均标记 testOnly=true、publishable=false。"),
    ]


def main() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    write_pdf(EVIDENCE_DIR / "pexels-license.pdf", "Pexels License 复核记录", license_story("license"))
    write_pdf(EVIDENCE_DIR / "pexels-terms.pdf", "Pexels Terms of Service 复核记录", license_story("terms"))

    output_names = {
        "interior": "source-4822916-interior.pdf",
        "white-polish": "source-4822552-white-polish.pdf",
        "black-polish": "source-6161632-black-polish.pdf",
        "wide-foam": "source-4243807-wide-foam.pdf",
        "foam": "source-6873499-foam.pdf",
        "pov": "source-4863265-pov.pdf",
        "rinse": "source-6872072-rinse.pdf",
        "glass": "source-8469669-glass.pdf",
        "wheel": "source-6873496-wheel.pdf",
    }
    for source in plan["sources"]:
        path = EVIDENCE_DIR / output_names[source["key"]]
        write_pdf(path, f"Pexels 素材来源复核 - {source['sourceTitle']}", source_story(source))


if __name__ == "__main__":
    main()
