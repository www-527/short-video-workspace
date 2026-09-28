# 现有 15 段素材复核与测试覆盖

复核日期：2026-09-01  
结论：已有 Pexels 素材足够制作本轮测试包，不需要再次下载网络视频；5 段 Coverr 素材不纳入测试包。

## Coverr 素材（排除）

| 文件 | 可覆盖画面 | 可映射作用 | 本轮决定 |
| --- | --- | --- | --- |
| 01_高压水枪洗车.mp4 | 高压冲洗 | process / hook | 排除 |
| 02_自助洗车操作.mp4 | 人工洗车 | service / process | 排除 |
| 03_车主到店开场.mp4 | 到店 | hook / cta | 排除 |
| 04_洗车场人物互动.mp4 | 人物氛围 | transition / cta | 排除 |
| 05_高压水枪氛围镜头.mp4 | 水花氛围 | hook / transition | 排除 |

排除原因：2026-09-01 复核的 Coverr License 禁止把视频用于 AI 训练、模型开发或作为数据集。本任务虽是内部模型评测而非训练，但会形成可重复投喂模型的测试数据集，边界不够清楚，因此采取保守策略全部排除。官方许可页 PDF 已保存在 `sources/license-evidence/coverr-license-excluded.pdf`。

## Pexels 素材（复用）

| 文件 | 画面类别 | 可映射作用 | 本轮用途 |
| --- | --- | --- | --- |
| 06_内饰吸尘清洁_Pexels.mp4 | 内饰吸尘 | detail | 主包内饰；音画冲突异常 |
| 07_白车机械抛光_Pexels.mp4 | 白车抛光 | result / offer | 主包优惠背景 |
| 08_黑车专业抛光_Pexels.mp4 | 黑车漆面抛光 | result / cta | 主包效果、CTA 背景 |
| 09_自动洗车机_Pexels.mp4 | 自动洗车机 | service / process | 未使用；标识和车辆品牌明显 |
| 10_泡沫冲洗_Pexels.mp4 | 车身泡沫覆盖 | process | 主包泡沫；重复/长口播异常 |
| 11_竖屏_泡沫喷洗_Pexels.mp4 | 工位喷洒水雾 | hook / process | 主包钩子；弱音异常 |
| 12_竖屏_车内洗车视角_Pexels.mp4 | 挡风玻璃水流 POV | transition | 主包转场；静音异常 |
| 13_竖屏_白车高压冲洗_Pexels.mp4 | 专业工位冲洗 | service / process | 主包服务与冲洗 |
| 14_竖屏_玻璃精细擦拭_Pexels.mp4 | 玻璃擦拭 | detail | 已复核，作为备用 |
| 15_竖屏_轮毂刷洗_Pexels.mp4 | 轮毂刷洗 | problem / detail | 主包问题与轮毂细节 |

九类作用覆盖结果：`hook`、`problem`、`service`、`process`、`detail`、`result`、`offer`、`cta`、`transition` 均至少一段。

## 权利边界

- 10 个 Pexels 原文件 SHA-256 与项目原记录全部一致；本测试包实际复制并使用 9 个，自动洗车机素材不参与。
- 当前 Pexels 许可允许免费使用和修改，但不等于人物、车牌、车辆品牌、产品设计或场地权利均已清理。
- 泡沫横版素材的主包裁切会显示车牌与品牌，已在清单中标记 `containsPlate: true`、`containsTrademark: true`。
- 所有文件均为 `testOnly: true`、`publishable: false`，不得公开发布或投放。
