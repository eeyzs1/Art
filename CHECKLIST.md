# 仓库优化 Checklist

记录 2026-11-05 review 的结论与待办。验收标准写明"怎么算完成"，避免只勾选不生效。

## 已完成（commit 157cda3）

- [x] **提交完整仓库**。此前仅有一个占位 initial commit，145 个 HTML、3 个生成器、manifest 全部 untracked。
  验收：`git status` 干净；`git log --oneline` 可见完整历史。
- [x] **消除 `build_course.py` 破坏性单跑行为**。模块级写盘收进 `build_base()`；直接运行拒绝执行并提示入口是 `extend_course.py`。
  验收：`python build_course.py` 以非零退出且不写任何文件；`import build_course` 无副作用。
- [x] **`extend_course.py` 显式调用 `base.build_base()`**，移除对 03.html 的字符串补丁。
  验收：连跑两次输出逐字节一致（幂等，已实测）。
- [x] **修复 42 处"共3课"过时标签**（改为 `TOTAL_LESSONS=9` 数据驱动），第03课底部导航补"下一课→04课"。
  验收：`Select-String "共3课"` 命中 0。
- [x] **`check_course.py` 加 `python -O` 防护**（裸 `assert` 在 -O 下会全部失效）。
- [x] **新增 `.gitignore`**（`__pycache__/`、`_research/*.png`）**与 `requirements.txt`**（playwright）。
- [x] **全量验证通过**：145 个 HTML、本地链接 0 断链、0 重复 ID、桌面+移动布局、全部交互组件、无控制台报错。

## 待办

### 中优先级

- [ ] **CI workflow**：GitHub Actions 在 push 时安装 Playwright 并运行 `check_course.py`。
  验收：push 后 Actions 绿；故意改坏一个链接能红。
- [ ] **拆分检查脚本**：本地链接检查独立成纯 Python 脚本（无 Playwright 依赖，秒级可跑、可进 CI 快车道）；截图输出移到临时目录，不再写进 `_research/`。
  验收：`python check_links.py` 无需浏览器即可运行；`_research/` 不再出现新 PNG。
- [ ] **`check_course.py` 裸 `assert` 改为显式校验**（带文件名和原因的报错，`-O` 防护只是兜底）。
  验收：人为破坏一处页面后，报错信息能直接定位文件。

### 低优先级

- [ ] **meta description + favicon**：145/145 页缺失（已核实）。在 `page()` 模板加两行即可。
  验收：生成后 `Select-String 'meta name="description"'` 命中 145。
- [ ] **内容数据迁移**：`build_course.py` 的 8 元组与 `course_extension_data.py` 的 `｜` 分隔字符串迁到 JSON/YAML，加载时校验字段数与非法分隔符。
  验收：数据文件可被独立 lint；生成结果与迁移前逐字节一致（或 diff 仅限预期变化）。
- [ ] **打印样式**：`@media print` 隐藏交互实验、保留正文，落实 README"打印可获得静态讲义"的承诺。
- [ ] **无障碍增强**：quiz 按钮加 `aria-pressed`；加 skip-to-content 链接。
- [ ] **生成 HTML 格式化**：目前单行压缩、diff 不友好。权衡体积与可审阅性后决定；生成文件也可保持现状、靠生成器 diff 审阅。
- [ ] **外链监控**：13 个外部域名（已抽查 2 个易失效链接存活）。可在 CI 定期 `HEAD` 巡检。

### 维持现状（明确不做的决定）

- **不引入构建框架/依赖**：双击 `index.html` 即可用是核心特性。
- **中文目录名保留**：本地 `file://` 使用无问题；若将来部署 GitHub Pages 再评估 ASCII slug。
- **`_research/teach/` skill 快照保留入库**：README 引用它作溯源。

## 快速验证命令

```
python extend_course.py     # 重建（会覆盖生成页面）
python check_course.py      # 全量检查（需 playwright）
```
