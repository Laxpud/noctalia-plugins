# Laxpud 的 Noctalia 插件

这是自用的精简插件源，当前收录 [Udiskie Manager](udiskie/README.md) 定制版。基于 Noctalia v5.4.1 / plugin API 43，保留原作者 aristides、MIT 许可证及 `aristides/udiskie` ID。

## 安装和更新

```sh
noctalia msg plugins source add laxpud git https://github.com/Laxpud/noctalia-plugins
noctalia msg plugins enable aristides/udiskie
noctalia msg plugins update laxpud
```

在 Settings → Plugins 中保留自动更新 All sources（`[plugins].auto_update = "all"`）。官方源和社区源仍启用，自用源排在它们后面。同一 ID 由后面的源覆盖，只运行一份；现有状态栏、设置和 IPC 地址继续有效。源跟随仓库默认分支 `main`，标签用于追踪版本。

自动更新拉取的是本仓库已发布的内容，不会自动把社区上游合并进来。上游同步由维护者审阅后发布。停用自用源可能退回社区版。

## 维护

- [AGENTS.md](AGENTS.md)：分支、提交、发布、注释、验证和翻译规则。
- [来源记录](maintenance/upstream.toml)：已合入的上游完整 SHA 与版本。
- [定制记录](maintenance/changes.md)：保留内容、上游 PR、验证范围。

```sh
# 默认只抓取上游并显示本插件差异，不修改工作文件。
python3 scripts/sync-upstream.py udiskie
# 工作区干净且位于 main 时，建立 codex 分支并三方应用。
python3 scripts/sync-upstream.py udiskie --apply
```

脚本利用已记录基线、当前定制和最新上游生成三方合并。它不会自动提交、推送、更新来源基线或发布。发生冲突后使用 `git status` 查看，逐项解决并 `git add`；应用失败时也要检查工作区，不要直接重跑。审阅完成后手动把本次输出的目标 SHA 和上游版本写入来源记录，再运行现有检查、递增自用版本并发布。

```sh
make -C udiskie test
# 提交插件版本改动后生成索引，并将索引作为后续提交纳入发布。
python3 scripts/update-catalog.py
git diff -- catalog.toml
```

CI 运行已有翻译检查和上游清单校验，并确认索引可重现；本地还需运行 Noctalia lint 和必要的真实场景验收。CI 不自动推送、发布或合并。

开发可临时添加排在最后的 `path` 源，完成后移除它以恢复 Git 源：

```sh
noctalia msg plugins source add laxpud-dev path /home/laxpud/workspace/noctalia-plugins
noctalia msg plugins source remove laxpud-dev
```

上游贡献仍通过 [community-plugins fork](https://github.com/Laxpud/community-plugins)；上游只提交英文翻译源，其他语言由 [Noctalia Translate](https://i18n.noctalia.dev) 维护。本仓库保留自用语言覆盖。
