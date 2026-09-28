from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_SECTION

OUT = r"D:\短视频\洗车营销视频Agent方案_MVP.docx"

# Compact Reference Guide preset, resolved for this product plan.
INK = "18282E"
BLUE = "1497B7"
ORANGE = "F05B38"
MIST = "F2F5F6"
PALE_BLUE = "E8F4F7"
PALE_ORANGE = "FFF0EB"
MUTED = "5F7078"
WHITE = "FFFFFF"
PAGE_WIDTH = 9360


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_width(cell, width_dxa):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(width_dxa))
    tc_w.set(qn("w:type"), "dxa")


def set_table_geometry(table, widths):
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.first_child_found_in("w:tblW")
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(sum(widths)))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.first_child_found_in("w:tblInd")
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), "120")
    tbl_ind.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    for row in table.rows:
        for index, cell in enumerate(row.cells):
            set_cell_width(cell, widths[index])
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_font(run, size=None, bold=None, color=None, name="Calibri"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def shade_paragraph(p, fill):
    p_pr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    p_pr.append(shd)


def add_bottom_border(p, color=BLUE, size="10"):
    p_pr = p._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), "7")
    bottom.set(qn("w:color"), color)
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def add_text(doc, text, style="Normal", after=None, color=None, bold=False, size=None, align=None):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, color=color)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.375)
    p.paragraph_format.first_line_indent = Inches(-0.188)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    r = p.add_run(text)
    set_font(r)
    return p


def add_number(doc, text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = Inches(0.375)
    p.paragraph_format.first_line_indent = Inches(-0.188)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    r = p.add_run(text)
    set_font(r)
    return p


def add_callout(doc, label, body, fill=PALE_BLUE, accent=BLUE):
    table = doc.add_table(rows=1, cols=1)
    set_table_geometry(table, [PAGE_WIDTH])
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label + "  ")
    set_font(r, size=10.5, bold=True, color=accent)
    r2 = p.add_run(body)
    set_font(r2, size=10.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def add_table(doc, headers, rows, widths, header_fill="E8F4F7"):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    set_table_geometry(table, widths)
    header_cells = table.rows[0].cells
    for i, label in enumerate(headers):
        cell = header_cells[i]
        set_cell_shading(cell, header_fill)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(label)
        set_font(r, size=10, bold=True, color=INK)
    for row_values in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row_values):
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(value)
            set_font(r, size=9.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_flow(doc, items):
    table = doc.add_table(rows=1, cols=len(items) * 2 - 1)
    arrow_width = 240
    item_width = (PAGE_WIDTH - arrow_width * (len(items) - 1)) // len(items)
    widths = []
    for i in range(len(items) * 2 - 1):
        widths.append(item_width if i % 2 == 0 else arrow_width)
    widths[-1] += PAGE_WIDTH - sum(widths)
    set_table_geometry(table, widths)
    for i, item in enumerate(items):
        cell = table.cell(0, i * 2)
        set_cell_shading(cell, PALE_BLUE)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(item)
        set_font(r, size=8.5, bold=True, color=INK)
        if i < len(items) - 1:
            ac = table.cell(0, i * 2 + 1)
            p2 = ac.paragraphs[0]
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p2.paragraph_format.space_after = Pt(0)
            r2 = p2.add_run("→")
            set_font(r2, size=12, bold=True, color=BLUE)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)


def set_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    normal.font.size = Pt(11)
    pf = normal.paragraph_format
    pf.space_after = Pt(6)
    pf.line_spacing = 1.25

    for name, size, color, before, after in [
        ("Heading 1", 16, BLUE, 18, 10),
        ("Heading 2", 13, BLUE, 14, 7),
        ("Heading 3", 12, "1F4D78", 10, 5),
    ]:
        style = doc.styles[name]
        style.font.name = "Calibri"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True


def set_header_footer(section):
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("WASHCUT  /  洗车营销视频 AGENT")
    set_font(r, size=8.5, bold=True, color=MUTED)
    add_bottom_border(p, color="D8E6E9", size="4")

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("产品方案 · MVP · 2026-08-11")
    set_font(r, size=8.5, color=MUTED)


def add_cover(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(42)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("PRODUCT DESIGN BRIEF")
    set_font(r, size=10, bold=True, color=BLUE)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("洗车营销视频\nAgent 方案")
    set_font(r, size=28, bold=True, color=INK)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run("从门店真实素材到完整竖屏营销视频的产品、网页与 Agent 架构设计")
    set_font(r, size=13, color=MUTED)

    table = doc.add_table(rows=1, cols=3)
    set_table_geometry(table, [3120, 3120, 3120])
    values = [("业务范围", "洗车门店"), ("交付形态", "15–180 秒竖屏视频"), ("核心引擎", "LLM + Remotion")]
    for idx, (label, value) in enumerate(values):
        cell = table.cell(0, idx)
        set_cell_shading(cell, PALE_BLUE)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(label)
        set_font(r, size=9, bold=True, color=BLUE)
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(value)
        set_font(r2, size=11, bold=True, color=INK)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    add_callout(doc, "方案结论", "第一版应是可控的生产流水线，而不是带复杂时间轴的剪辑器或自由聊天式多 Agent 系统。用户提交素材和事实信息后，Agent 自动构思、编排、配音、加字幕与 BGM，并导出成片。", fill=PALE_ORANGE, accent=ORANGE)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(124)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("内部产品设计文档\n版本 1.0")
    set_font(r, size=10, color=MUTED)
    doc.add_page_break()


def build_document():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)
    set_styles(doc)
    set_header_footer(section)

    add_cover(doc)

    doc.add_heading("1. 产品定义与边界", level=1)
    add_text(doc, "产品定义", style="Heading 2")
    add_text(doc, "面向洗车门店、代运营和本地生活运营人员的营销视频生成系统。用户上传门店图片、视频和活动信息，选择视频时长，系统自动构思并生成带配音、字幕、背景音乐的竖屏营销视频。")
    add_text(doc, "第一版目标", style="Heading 2")
    add_bullet(doc, "将用户的真实门店素材作为视频可信度的主体。")
    add_bullet(doc, "在用户素材不足时，从平台自有且已授权的洗车素材库补充通用镜头。")
    add_bullet(doc, "生成 15–180 秒、9:16 的完整营销视频，包括配音、字幕、BGM、封面和素材来源清单。")
    add_bullet(doc, "把 LLM 的创意决策沉淀为结构化规格，确保可渲染、可追溯、可复现。")
    add_text(doc, "第一版不做", style="Heading 2")
    add_table(doc, ["暂不纳入", "原因"], [
        ("生成后的自然语言修改", "会引入局部重渲染、版本管理和时间轴编辑的额外复杂度。"),
        ("人工时间轴编辑器", "首版目标是自动交付，不要求用户学习剪辑软件。"),
        ("跨行业视频生成", "先沉淀洗车素材语义、营销知识和质量标准。"),
        ("未授权平台素材抓取", "避免版权、来源和门店真实性风险。")
    ], [2700, 6660])

    doc.add_heading("2. 用户输入与时长策略", level=1)
    add_text(doc, "用户需要提交的内容", style="Heading 2")
    add_table(doc, ["输入类别", "内容", "系统用途"], [
        ("门店素材", "门头、店内环境、洗车过程、洗后效果、Logo", "建立真实性，提供实际可剪的画面。"),
        ("营销事实", "门店名、城市/区域、优惠、价格、规则、CTA", "约束口播、字幕与行动引导，禁止模型编造。"),
        ("视频时长", "自动推荐，或 15 / 30 / 45 / 60 / 90 / 120 / 180 秒", "决定叙事密度、脚本长度和镜头数量。"),
        ("内容调性", "真实探店、促销直接、专业服务、轻松车主口吻", "影响口播语气、字幕风格和 BGM 选择。"),
        ("素材库授权", "是否允许使用自有洗车素材库补充通用镜头", "决定素材不足时的处理方式。")
    ], [1800, 3960, 3600])
    add_callout(doc, "时长原则", "时长由用户选择或系统自动推荐共同决定；系统评估的是“非重复且有叙事价值的有效画面”，而不是上传文件的原始总时长。", fill=PALE_BLUE)
    add_table(doc, ["时长", "内容组织方式"], [
        ("15–30 秒", "聚焦一个利益点，快速建立注意力，清楚给出优惠与 CTA。"),
        ("30–60 秒", "增加真实服务过程、价格解释、门店证明和适用说明。"),
        ("60–90 秒", "展开洗车流程、项目内容与用户顾虑，适合探店或服务讲解。"),
        ("90–180 秒", "支持完整流程、套餐解释、洗车知识、门店故事和更充分的服务证明。")
    ], [2100, 7260])

    doc.add_heading("3. 素材策略与素材库", level=1)
    add_text(doc, "素材使用的基本原则", style="Heading 2")
    add_text(doc, "用户素材决定门店真实性；已授权洗车素材库补充通用洗车动作与氛围。素材库不是替代门店素材的主角，更不能把其他门店内容伪装为本店现场。")
    add_table(doc, ["素材类型", "优先来源", "是否可由素材库补充", "使用约束"], [
        ("高压冲洗、泡沫、轮毂清洗", "用户素材", "可以", "可作为通用服务过程和视觉冲击镜头。"),
        ("洗前/洗后质感", "用户素材", "可以", "不得暗示素材库车辆就是本店客户车辆。"),
        ("门头、店内环境、Logo", "用户上传", "不可以", "必须来自该门店。"),
        ("价格、套餐、活动规则", "用户填写", "不可以", "只能引用已确认的业务事实。"),
        ("技师与服务背书", "用户素材", "谨慎", "素材库人物不能被表述为本店员工。")
    ], [1900, 1800, 1900, 3760])
    add_text(doc, "洗车素材库的最小结构", style="Heading 2")
    add_table(doc, ["对象", "关键内容"], [
        ("assets", "素材文件、来源、商用授权范围、有效期、分辨率、横竖屏。"),
        ("asset_segments", "片段起止时间、缩略图、动作描述、镜头景别、可用性。"),
        ("asset_tags", "高压冲洗、泡沫、轮毂、吹干、内饰、洗后反光、门头等语义标签。"),
        ("render_specs", "每支成片具体使用的片段、文字、声音和来源。"),
        ("performance_feedback", "发布后的完播、点击、团购转化，用于后续优化。")
    ], [2200, 7160])
    add_callout(doc, "来源追溯", "每条成片都应保留：用户上传素材、授权素材库片段、生成的配音/字幕/CTA 卡片。这样便于替换、下架、版权核查和投诉处理。", fill=PALE_ORANGE, accent=ORANGE)

    doc.add_heading("4. 网页信息架构与排版", level=1)
    add_text(doc, "设计定位", style="Heading 2")
    add_text(doc, "网页应是“单次创作工作台”，而不是传统剪辑器。用户的任务是交付门店素材与营销事实，而不是手动拖拽时间轴。界面以洗美工位为视觉语言：雾灰背景、清洁留白、清洗蓝状态色和优惠橙数字。")
    add_text(doc, "桌面端新建项目页", style="Heading 2")
    add_table(doc, ["区域", "版面比例", "主要内容", "设计目的"], [
        ("顶部导航", "全宽", "品牌、项目入口、素材库入口", "保持导航轻量，不做数据大屏。"),
        ("素材区", "约 65%", "上传区、素材缩略图、识别标签、时长", "让真实素材成为页面视觉主角。"),
        ("活动信息区", "约 35%", "门店、优惠、规则、时长、调性、素材库授权", "集中收集创作所需的业务事实。"),
        ("底部操作区", "全宽固定", "素材使用说明、生成按钮", "任何时候都明确下一步动作。")
    ], [1500, 1300, 3600, 2960])
    add_text(doc, "推荐页面骨架", style="Heading 2")
    add_flow(doc, ["上传素材", "填写活动", "选择时长", "生成视频"])
    add_bullet(doc, "素材区以真实缩略图呈现，并只显示用户可理解的信息：内容识别、时长、是否可用、删除操作。")
    add_bullet(doc, "右侧表单按“门店与活动 / 视频目标 / 素材库授权”分组，避免一长串无层级输入框。")
    add_bullet(doc, "生成中保留用户素材和活动信息，展示明确的生产步骤，而不是只有等待动画。")
    add_bullet(doc, "成片页是交付页：9:16 预览、MP4、封面、字幕和素材来源，不做编辑器。")
    add_callout(doc, "界面签名", "用一条“洗车导流线”表达真实工作顺序：素材入槽 → 信息确认 → Agent 剪辑 → 视频出片。它只在状态变化时运动一次，不使用无意义的 AI 装饰动效。", fill=PALE_BLUE)

    doc.add_heading("5. Agent 框架", level=1)
    add_text(doc, "框架选择", style="Heading 2")
    add_text(doc, "第一版采用工作流编排型 Agent：一个总编排器调用职责明确的专业模块。它比自由协作的多 Agent 对话更适合确定的生产流水线，具有更好的稳定性、成本可控性和故障可追踪性。")
    add_text(doc, "总体生产链", style="Heading 2")
    add_flow(doc, ["素材理解", "创意导演", "视觉编导", "音频生产", "Remotion", "质量检查"])
    add_table(doc, ["模块", "回答的问题", "主要输出"], [
        ("素材理解 Agent", "用户和素材库里有什么可用画面？", "AssetManifest：素材、片段、标签、覆盖情况。"),
        ("创意导演 Agent", "这条视频应该讲什么故事？", "CreativeSpec：脚本、口播、叙事段落与镜头意图。"),
        ("视觉编导 Agent", "具体用哪段画面、怎样排、怎样衔接？", "VideoSpec：素材片段、时长、裁切、字幕位置、转场。"),
        ("音频生产模块", "声音如何与画面同步？", "TTS、字幕时间轴、BGM 和混音参数。"),
        ("Remotion 渲染器", "如何精确输出成片？", "MP4、封面、字幕文件。"),
        ("质量检查 Agent", "成片是否真实、清楚、可投放？", "通过 / 内部重规划 / 失败原因。")
    ], [2000, 3600, 3760])

    doc.add_heading("6. 视觉编导 Agent：画面编排责任", level=1)
    add_text(doc, "画面编排的唯一责任主体是视觉编导 Agent。创意导演决定“要讲什么”，Remotion 决定“如何渲染”，视觉编导决定“观众具体看到什么”。")
    add_table(doc, ["输入", "视觉编导需要做出的决策"], [
        ("用户素材与素材库候选", "选用用户素材或授权素材库片段；确定原视频的起止时间。"),
        ("创意导演的分镜意图", "把“表达低价”转成具体画面，例如高压水枪、泡沫、价格卡或用户门头。"),
        ("9:16 与目标时长", "裁切主体、控制镜头时长、在长视频中建立节奏变化。"),
        ("口播与字幕", "给每句字幕选择安全位置，避免遮挡车辆、人物和核心服务动作。"),
        ("品牌与事实约束", "门头、Logo、价格、规则等内容必须使用用户真实信息。")
    ], [3000, 6360])
    add_text(doc, "示例：49 元 6 次洗车卡", style="Heading 2")
    add_table(doc, ["叙事任务", "视觉编导决策"], [
        ("开头引起注意", "优先选用户的高压水枪近景；没有时从授权库选择无门店品牌的冲洗镜头。"),
        ("清楚展示优惠", "在画面留白较多的泡沫或车身镜头上放“49元6次洗车卡”。"),
        ("证明门店真实", "必须使用用户上传的门头、店内工位或本店服务画面。"),
        ("完成行动引导", "使用用户洗后效果或门头，叠加由系统生成的 CTA 卡片。")
    ], [2400, 6960])
    add_callout(doc, "关键边界", "视觉编导 Agent 不可把其他门店的门头、员工或服务承诺当成用户门店内容。通用洗车过程可以补位，门店真实性与业务事实不能补造。", fill=PALE_ORANGE, accent=ORANGE)

    doc.add_heading("7. 关键数据合同", level=1)
    add_text(doc, "所有模块围绕结构化数据协作，LLM 不直接生成 Remotion 代码。", style="Normal", after=6)
    add_table(doc, ["数据对象", "由谁生成", "包含内容", "下游用途"], [
        ("AssetManifest", "素材理解 Agent", "素材、片段、标签、可用性、有效画面时长", "给创意导演和视觉编导理解素材边界。"),
        ("CreativeSpec", "创意导演 Agent", "视频主题、脚本、口播、叙事任务、事实引用", "指导素材检索与画面编排。"),
        ("VideoSpec", "视觉编导 + 音频模块", "精确片段、画面裁切、字幕、配音、BGM、来源", "作为 Remotion 的唯一渲染输入。"),
        ("RenderJob", "编排器", "任务状态、重试、产物路径、失败原因", "支持进度展示和断点恢复。")
    ], [1900, 2100, 3000, 2360])
    add_text(doc, "VideoSpec 中每个镜头应至少记录", style="Heading 2")
    add_bullet(doc, "叙事任务：该镜头要让观众理解什么。")
    add_bullet(doc, "来源：用户素材 / 已授权素材库 / 系统生成卡片。")
    add_bullet(doc, "精确片段：文件 ID、起止时间、在成片中的开始时间和持续时间。")
    add_bullet(doc, "画面规则：竖屏裁切、主体焦点、速度、转场、字幕位置。")
    add_bullet(doc, "事实引用：价格、门店、规则等信息对应的用户输入字段。")

    doc.add_heading("8. 任务编排、渲染与质检", level=1)
    add_text(doc, "任务状态", style="Heading 2")
    add_flow(doc, ["排队", "分析素材", "构思", "补充素材", "制作音频", "渲染", "质检", "完成"])
    add_text(doc, "编排器需支持任务断点恢复：音频失败不应重新分析素材；渲染失败不应重新调用文案模型；质检发现字幕遮挡时可只重建 VideoSpec 后再次渲染。")
    add_text(doc, "质量检查", style="Heading 2")
    add_table(doc, ["检查维度", "检查内容"], [
        ("事实一致性", "价格、次数、门店名、地域、服务规则与用户输入一致。"),
        ("素材真实性", "门头、Logo、员工等门店特征来源正确；授权素材使用记录完整。"),
        ("视觉可读性", "字幕不溢出安全区，不遮挡主体；不存在黑帧、素材缺失和错误裁切。"),
        ("声音质量", "配音与字幕一致；BGM 在口播时自动压低；无削波或突兀静音。"),
        ("节奏与时长", "满足用户选定或系统推荐时长，不机械重复同一画面。")
    ], [2100, 7260])

    doc.add_heading("9. Remotion 与基础设施职责", level=1)
    add_text(doc, "Remotion 是确定性渲染层，不是创意层。它接收 VideoSpec 后完成素材截取、9:16 裁切、动态文字、字幕、配音、BGM、转场和 MP4 导出。")
    add_table(doc, ["层级", "职责"], [
        ("Web 应用", "上传素材、填写活动信息、选择时长、展示任务进度、下载成片。"),
        ("业务 API", "项目、活动事实、用户权限、配额、任务状态和成片元数据。"),
        ("Agent 编排 Worker", "调用素材理解、创意、视觉编导、音频和质检模块。"),
        ("媒体 Worker", "转码、抽帧、抽音频、TTS、字幕、BGM 混音、Remotion 渲染。"),
        ("对象存储", "原始用户素材、授权素材、代理文件、音频、成片和封面。"),
        ("数据库", "素材元数据、片段标签、CreativeSpec、VideoSpec、RenderJob、素材溯源。")
    ], [2100, 7260])

    doc.add_heading("10. 中转站通信协议集成", level=1)
    add_text(doc, "接入原则", style="Heading 2")
    add_text(doc, "所有需要 LLM 的模块（素材理解、创意导演、视觉编导和质检）均通过服务端的统一 RelayClient 访问中转站。浏览器只调用本系统的业务 API，不直接持有、展示或请求中转站 API Key。")
    add_flow(doc, ["浏览器", "业务 API", "Agent Worker", "RelayClient", "中转站 /v1/responses"])
    add_table(doc, ["层级", "职责与边界"], [
        ("浏览器", "上传素材、提交活动事实、查询任务进度与下载成片；不接触中转站凭据。"),
        ("业务 API", "验证用户输入、创建 RenderJob、签发任务；不将 API Key 返回给客户端。"),
        ("Agent Worker", "调用 RelayClient 完成素材理解、创意构思、视觉编导与质量检查。"),
        ("RelayClient", "唯一实现 Responses HTTP/SSE 协议的模块；负责地址规范化、身份 Header、流解析、脱敏日志和有限重试。"),
        ("中转站", "接收 POST /v1/responses，返回 text/event-stream；由 response.completed 确认成功。")
    ], [1900, 7460])
    add_text(doc, "RelayClient 协议要求", style="Heading 2")
    add_table(doc, ["项目", "实现要求"], [
        ("请求地址", "将配置的 Base URL 通过 URL 解析规范化为 /v1/responses；不得用字符串简单拼接。"),
        ("鉴权与身份", "使用 Bearer API Key；每次调用创建 session/thread/turn UUID；installation ID 在同一进程内稳定复用。"),
        ("请求体", "使用 Responses 格式：system prompt 放 instructions，业务输入放 input；固定 stream:true、store:false、tools:[]、tool_choice:auto。"),
        ("流式处理", "按 SSE 空行分帧，消费 data: 行；只拼接 response.output_text.delta 的 delta 字段。"),
        ("成功边界", "只有收到 response.completed 才标记模型调用成功；只有 [DONE] 或网络 EOF 均视为不完整失败。"),
        ("异常处理", "response.failed、error、非 2xx、非法 JSON、超时或中途断流必须形成明确失败状态。"),
        ("日志安全", "绝不记录 API Key、Bearer Token、Cookie、图片 data URL 或 reasoning.encrypted_content。")
    ], [1900, 7460])
    add_text(doc, "与 Agent 链的结合", style="Heading 2")
    add_table(doc, ["调用方", "经由中转站得到的结果", "输出约束"], [
        ("素材理解 Agent", "对视频抽帧和门店图片的视觉描述、素材标签、可用片段建议。", "输出 AssetManifest JSON；图片作为 input_image data URL，上传前限制 MIME、数量和体积。"),
        ("创意导演 Agent", "营销故事、口播、叙事任务与事实引用。", "输出 CreativeSpec JSON；不得生成未经用户确认的价格、门店或服务规则。"),
        ("视觉编导 Agent", "依据候选素材的描述和缩略图，决定片段、时长、裁切和字幕位置。", "输出 VideoSpec JSON；不直接生成 Remotion 代码。"),
        ("质量检查 Agent", "检查事实一致性、字幕安全区、素材来源和画面问题。", "输出结构化通过/失败/重规划建议。")
    ], [2050, 3620, 3690])
    add_callout(doc, "结构化输出", "RelayClient 只负责可靠取得 SSE 文本输出；各 Agent 再对该文本执行 JSON 解析与 Zod/Schema 校验。解析失败属于模型输出失败，不可被误判为渲染成功。", fill=PALE_BLUE)
    add_text(doc, "重试与取消策略", style="Heading 2")
    add_bullet(doc, "对用户取消、请求格式错误、模型不支持和结构化 JSON 不合法等确定性错误，不自动重试。")
    add_bullet(doc, "对 408、409、425、429、5xx 和明确的短暂网络故障，可使用次数有限、带退避且可取消的重试。")
    add_bullet(doc, "中转站不会因为 Responses 失败而自动切换到 Chat Completions；任何协议降级必须是明确的兼容策略。")

    doc.add_heading("11. MVP 交付与下一步", level=1)
    add_text(doc, "MVP 完整闭环", style="Heading 2")
    add_number(doc, "用户上传洗车门店素材，填写活动信息并选择时长。")
    add_number(doc, "系统分析用户素材，建立可用片段与素材覆盖清单。")
    add_number(doc, "LLM 自主构思内容；必要时检索已授权的通用洗车片段。")
    add_number(doc, "视觉编导 Agent 完成画面编排，输出 VideoSpec。")
    add_number(doc, "生成中文配音、同步字幕和已授权 BGM。")
    add_number(doc, "通过 Remotion 输出 9:16 MP4、封面、字幕文件和素材来源清单。")
    add_text(doc, "首轮验收标准", style="Heading 2")
    add_bullet(doc, "用户上传有限的门店素材后，能稳定得到一条 15–180 秒的完整洗车营销视频。")
    add_bullet(doc, "成片中门头、Logo、优惠和服务规则均与用户输入一致。")
    add_bullet(doc, "素材不足时可补充授权洗车通用镜头，但不伪造门店真实性。")
    add_bullet(doc, "视频包含可读字幕、清晰配音、合规 BGM 和完整来源记录。")
    add_bullet(doc, "用户不需要学习时间轴、转场或剪辑工具即可完成生产。")
    add_callout(doc, "最终产品判断", "用户看完成片后应明确感到：这是我家的门店与真实优惠，但比我自己剪得更专业、更适合投放。", fill=PALE_ORANGE, accent=ORANGE)

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build_document()
