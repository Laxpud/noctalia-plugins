# 当前定制与验证范围

## Udiskie 0.1.2（2026-11-01）

基于上游 0.1.1，保留 `aristides/udiskie`，原作者 aristides、MIT 许可证。运行文件从本机已部署定制版迁入，未改变设备操作逻辑。

- 根据设备能力显示安全移除；分区保留明确的卸载按钮。
- 先重新查询设备能力，再递归卸载；成功后才弹出或断电。
- 插件内设备变更串行执行，超时或失败后不自动重试；尽可能使用持久设备路径。
- 旧 eject/detach IPC 保留明确语义，增加能力检查和卸载前置步骤。
- 保留简体中文和西班牙文补充，以及错误页颜色修正。
- 通用修复见 [Issue #1247](https://github.com/noctalia-dev/community-plugins/issues/1247) 和 [Draft PR #1248](https://github.com/noctalia-dev/community-plugins/pull/1248)。上游 PR 的非英文改动已拆除，自用源仍保留。

现有翻译检查、Noctalia lint 和上游清单校验通过；此前已验证 Niri 上服务加载与面板打开。源码与迁移后的运行副本做一致性检查。未新增测试代码。

仍待真实设备验收：卸载与断电、多分区忙碌、LUKS、可弹出介质、无分区文件系统、长时间卸载、操作期间拔插。仓库迁移不触发设备操作，也不构成这些场景的验收。thumbnail.webp 沿用上游，尚未随新界面更新。

## 工具来源

`.github/workflows/scripts/` 下两个 Python 工具原样来自来源记录中的上游提交。`udiskie/tests/check_translations.py` 和插件 Makefile 是已有上游文件，未新增测试实现。新增 `scripts/` 仅负责同步准备及索引生成入口。
