# xiaomabufei.github.io

MSL 的个人学术主页，使用原生 HTML、CSS 和 JavaScript 构建，可直接部署到 GitHub Pages。

## 本地预览

在项目目录执行：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000`。

## 后续需要替换的内容

主要编辑 `index.html`：

- 替换个人介绍中的占位文字。
- 更新“最新动态”的日期和内容。
- 替换三篇代表论文的标题、作者、简介和链接。
- 用论文图片替换 `.paper-visual` 占位色块。
- 更新教育与工作经历。
- 根据需要修改页面标题和 SEO 描述。

视觉样式集中在 `style.css`，轻量滚动动画位于 `script.js`。

## Google Scholar 引用数

`scripts/update_scholar.py` 会读取 Google Scholar 主页上的总引用数，并更新
`index.html` 中的 `scholar-citations`。`.github/workflows/update-scholar.yml`
每天运行一次该脚本，并在引用数变化时自动提交更新。

也可以在本地手动运行：

```bash
python3 -m pip install requests beautifulsoup4
python3 scripts/update_scholar.py
```
