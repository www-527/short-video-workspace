# 真实 AI 链路与异常包验收报告

日期：2026-09-01  
测试包：`D:\短视频\素材\真实AI链路测试包_v1`  
程序：`D:\短视频\washcut-agent-demo`  
模型：`gpt-5.6-terra`  
转写：`Qwen/Qwen3-ASR-1.7B` + `Qwen/Qwen3-ForcedAligner-0.6B`

## 1. 最终结论

本轮真实应用测试已经执行完毕，结论为 **有条件通过**：

- 主包真实链路通过：11 条素材全部完成媒体检测、Qwen3-ASR、视觉理解、全量编排、时间线、Caption JSON、WebVTT、无字幕成片和带字幕成片。
- `finalClipOrder` 含 11 个且仅含本项目的 11 个程序 `assetId`，每个恰好出现一次，`excludedAssets` 为空。
- 五个可处理异常项目全部生成完成；10 个普通/字幕 MP4 均完成全量音视频解码检查。
- 损坏媒体在上传探测阶段被拒绝，项目保持 0 条素材，没有留下半批已提交素材。
- 六类异常场景中，静音、音画冲突、低音量、重复素材 4 类通过；长口播字幕、损坏文件错误合同 2 类部分通过。

本报告只证明内部测试链路；全部素材仍为 `testOnly: true`、`publishable: false`，不得据此公开发布或投放。

## 2. 主包验收

项目：`测试`  
项目 ID：`project_9e34e8c8-f770-43f5-862c-8a47b73dbc54`  
版本 ID：`generation_42dc9eb0-e1f3-40fd-897b-58f1e71ee9a3`  
终态：`completed` / 输出 `ready`

### 2.1 测试包文件到程序素材 ID 的映射

| 测试文件 | 程序 assetId |
| --- | --- |
| `wc-main-01-hook.mp4` | `asset_53b1b6e9-730b-47b6-a60c-b4fb7876f953` |
| `wc-main-02-problem.mp4` | `asset_744ea131-3811-4c4b-acd9-c8cb09d1c281` |
| `wc-main-03-service.mp4` | `asset_53467b57-4a35-4bf3-9973-e40e8451eafb` |
| `wc-main-04-foam.mp4` | `asset_41900fb9-e634-44eb-8005-070c817bda52` |
| `wc-main-05-rinse.mp4` | `asset_f04568ac-afbc-41de-b388-6abe1d5d23ba` |
| `wc-main-06-wheel.mp4` | `asset_e358d588-1361-41b7-ad98-46de366a626c` |
| `wc-main-07-interior.mp4` | `asset_d4501a4b-eee7-4a00-805c-593237071a80` |
| `wc-main-08-result.mp4` | `asset_05c51be7-df32-4f49-9abb-74dde7c6ae4b` |
| `wc-main-09-transition.mp4` | `asset_f60d8b94-8ce3-4325-95b5-a2d75014bca7` |
| `wc-main-10-offer.mp4` | `asset_94c0f879-fde8-4bf6-bbae-57908f03eb06` |
| `wc-main-11-cta.mp4` | `asset_ad20997f-94bb-461f-8ff5-a7a8d4291c03` |

### 2.2 实际 finalClipOrder

1. `wc-main-09-transition.mp4`
2. `wc-main-01-hook.mp4`
3. `wc-main-04-foam.mp4`
4. `wc-main-03-service.mp4`
5. `wc-main-05-rinse.mp4`
6. `wc-main-02-problem.mp4`
7. `wc-main-06-wheel.mp4`
8. `wc-main-07-interior.mp4`
9. `wc-main-10-offer.mp4`
10. `wc-main-08-result.mp4`
11. `wc-main-11-cta.mp4`

集合、唯一性与项目隔离检查：通过。时间线片段数为 11，时长 `52,732ms`；输出媒体时长约 `52,800ms`。

### 2.3 ASR、视觉和字幕

- Qwen3-ASR 11/11 返回转写，预期关键词 11/11 命中。
- 13/13 次模型对话完成：11 次联系表视觉总结、1 次视觉精查、1 次全量编排；均为一次尝试并返回可解析 JSON。
- 每段都有可读画面说明与九类枚举中的有效作用。
- 实际模型作用分布为 `process × 8`、`problem × 1`、`offer × 1`、`transition × 1`，没有复现测试包预期的九类语义分布。程序合同有效，但营销作用语义仍需后续评测优化。
- 首次成片出现句尾孤字；修复分段算法后，当前 Caption JSON/WebVTT 已重新生成，字幕由 33 段变为 28 段，1～2 字孤立字幕为 0，并重新渲染字幕成片。

主包输出目录：

`D:\短视频\washcut-agent-demo\data\auto-video\projects\project_9e34e8c8-f770-43f5-862c-8a47b73dbc54\generations\generation_42dc9eb0-e1f3-40fd-897b-58f1e71ee9a3`

当前输出 SHA-256：

- `output.mp4`：`38B4D814C61F579D8782145DA76B1786E0A23B2807D04160A10EA429DEB61D8E`
- `output-captioned.mp4`：`62C05997DF3E4282F37BA62E3913457AB3982B0DE1E6961D41792249C4FBF4A4`

## 3. 异常包验收

| 场景 | 项目 / 版本 | 实际结果 | 结论 |
| --- | --- | --- | --- |
| 静音 | `project_1f3580b2-310d-45b8-a4bf-430718d2f9c2` / `generation_4537fbd4-bdeb-4141-aca0-6a15e401a7c3` | 媒体确认 `hasAudio: false`；Qwen 返回空文本、0 words、0 segments；视觉仍生成挡风玻璃水流说明和 `problem`；排序含唯一素材；空 Caption JSON/VTT 合法；双成片完成 | 通过 |
| 音画冲突 | `project_10228b13-059b-42f9-9674-7aa0f1848024` / `generation_0baccbcc-407b-4741-bae1-24aae03b5fec` | ASR 为“高压水流冲净泡沫”；画面总结为“车内吸尘”；编排结果以车内吸尘为准，未被口播带偏；双成片完成 | 通过；联合理解架构见第 4 节 |
| 低音量 | `project_238e21e3-fb7c-4188-bcda-1999964ae5b8` / `generation_e94a4a96-1c2f-447d-81a7-60601490df8f` | Qwen 成功识别“你的车多久没有彻底洗过了？”；视觉、排序和双成片完成 | 通过；字幕字级对齐漏掉句尾“了”，见第 5 节 |
| 重复素材 | `project_ff0f942f-c6c7-4219-9e67-9075ec253038` / `generation_43461af9-ac8c-4b28-b2f8-900d09aa3fb9` | 两个输入 SHA-256 相同，但生成两个不同 `assetId`；`finalClipOrder` 含两个且各一次；`excludedAssets` 为空；时间线含 2 条；双成片完成 | 通过；分析结果未填写 `duplicateWithAssetIds`，但未违反全量使用不变量 |
| 长口播 | `project_47aa4442-5922-4a87-8691-26c46239e60f` / `generation_f828ae23-11e5-4662-8ec6-1be6fc822703` | 36 个字级时间项、6 条字幕、无时间倒序、重叠或 1～2 字孤立字幕；双成片完成 | 部分通过：仍出现“冲 / 净残留”“内 / 饰细节”等语义断开 |
| 损坏媒体 | 项目 `异常验收`，0 条素材、0 个版本 | 上传阶段 `ffprobe` 报 `error reading header` / `Invalid data found when processing input`，文件未进入项目 | 部分通过：原子拒绝正确，但错误合同和展示仍有缺口 |

五个生成版本共 11 次模型对话，全部 `completed`、`attempts: 1`。五个版本的无字幕和带字幕成片共 10 个 MP4，均使用 FFmpeg 从头到尾解码通过。

## 4. 音画冲突的实际模型输入链路

用户观察“语音转文字没有和图像一起传入模型”是准确的，但只描述了第一阶段。当前实现是分阶段融合：

1. `auto-video.asset-visual-summary`：模型收到联系表 JPEG、媒体元数据和用户要求，**没有收到 ASR 文本**。提示词还明确要求不能让转写改变画面判断。
2. `asset_understanding`：当前连接模式没有再次调用模型，而是程序把视觉 JSON 与 ASR 组合成 `audioSummary`、`visualSummary` 和 `combinedSummary`。
3. `auto-video.edit-planning`：编排模型没有收到原始图片，但收到了上一步的视觉总结和 ASR 文本，并被要求按“画面行为 > OCR > 转写”处理冲突。

本次真实请求中，编排模型实际收到：

- `audioSummary`：`再用高压水流冲净泡沫，减少泥沙残留。`
- `visualSummary`：`近距离展示工作人员戴手套使用吸尘设备清洁汽车内部……`
- `combinedSummary`：同时包含上述两者，并把语音标记为“仅辅助”。

模型最终按吸尘画面生成编排理由，因此本场景的“画面优先”验收通过。

但当前没有任何一次模型调用同时看到“原始联系表图片 + ASR 文本”。如果产品要求模型显式做逐片音画一致性判断、输出冲突类型或更精细的联合摘要，应另行设计第二阶段联合理解调用；本轮未修改该业务行为。

## 5. 未完全通过项与建议优先级

### P1：Caption 字级对齐与语义边界仍不完整

- 长口播无单字孤立，但出现“再用高压水流冲 / 净残留”“轮毂玻璃和内 / 饰细节”。
- 低音量项目 ASR 文本含句尾“了”，Caption 由字级对齐结果生成时遗漏该字。
- 重复素材 ASR 文本含“表面的灰尘”，Caption 显示为“表面灰尘”。

建议后续把“Caption 拼接文本与规范化 ASR 文本一致”加入自动测试，并在分段时引入中文短语/标点边界，而不仅按字符数和时长平衡。

### P1：损坏媒体错误合同仅部分满足要求

截图保留了以下字段：

- `type: request.failed`
- `eventId: evt_afab03f3-4f0c-47b2-aa35-4474ad129a26`
- `occurredAt: 2026-09-01T07:02:32.120Z`
- `traceId: trc_441f7eac-b447-4bcc-bd57-efdbbdd970c6`
- `jobId: job_362366fb-14f6-4bb1-b76a-85e4ff25c99b`
- `code: request_failed`
- `stage: business_api`
- `retryable: false`
- `message: 请求处理失败，文件未进入项目。`
- `details` 中保留 `ffprobe.exe_failed`、`error reading header` 和 `Invalid data found when processing input`

正确之处是文件未进入项目、没有半批提交，并保留了 traceId、可重试语义和 FFprobe 原始 stderr。缺口是顶层 `code/message` 仍是泛化包装、截图未显示 HTTP 状态，界面把整段事件 JSON 直接展示为红色长条。建议后续把媒体错误自身的 code/message 作为主错误，并把阶段、traceId、retryable 作为附加字段，用结构化错误卡片展示。

### P2：完成状态存在内部不一致

五个异常生成版本的数据库主状态均为 `completed`，输出也为 `ready`，审计日志记录 `auto-video.generation.completed`；但版本载荷仍显示 `progress: 91`，`steps.render.status: running`、`progress: 5`。这没有阻止成片生成，但会影响恢复、监控和后续排障，应单独修复终态持久化。

### P2：营销作用语义覆盖不足

主包设计覆盖九种作用，但实际视觉模型大多按可见清洗动作标为 `process`。所有值都通过枚举校验，不影响排序完整性；如果产品要求模型可靠区分 `hook/service/detail/result/cta`，需要新增带人工真值的作用分类评测并调整定义或融合策略。

## 6. 验证证据

- SQLite：`D:\短视频\washcut-agent-demo\data\washcut.sqlite`
- 主包和异常生成目录：`D:\短视频\washcut-agent-demo\data\auto-video\projects`
- 异常错误截图：用户提供的 `codex-clipboard-97f7ec65-bd68-461a-90b2-a98f3a126f1a.png`
- 长口播字幕抽帧联系表：`D:\短视频\washcut-agent-demo\data\tmp\edge-long-captioned-contact-sheet.png`
- 测试包离线校验：`reports/package-validation.json`，结果 `passed`

## 7. 收口判定

素材制作、主包真实链路、六类异常场景执行和测试记录均已完成。当前可以关闭“测试执行”任务，但不能把结果写成“全部无缺陷通过”。若要进入下一轮产品修复，建议顺序为：

1. 修复 Caption 文本完整性与中文语义分段。
2. 修复生成版本终态的 `progress/steps.render` 持久化一致性。
3. 修复上传媒体错误的原始 code/message 透传和界面展示。
4. 决定是否新增“盲视觉锚定后，再把图片与 ASR 一起交给模型”的联合理解阶段。
