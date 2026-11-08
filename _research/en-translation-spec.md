# English Edition Translation Spec (en-translation-spec)

Authoritative style + terminology guide for translating the Art Study Room (艺术学习室) course library into English. Read this file completely before translating anything. Deviate only when a rule conflicts with source meaning; when in doubt, keep the source's semantic precision.

## 1. Project context

The library is a self-study art-humanities course site generated from Python data modules. We are creating English **mirror modules** (`*_en.py`) that generate a parallel English site under `en/`. Translation quality goal: professional art-education / art-historical English of the kind used by museums (Getty, Met, V&A, MoMA) and university humanities courses — not machine-translationese.

## 2. Language & style rules

1. **American English** spelling (color, organize, theater→ but see proper nouns: "theatre" only inside proper names like V&A Theatre and Performance collection).
2. **Register**: precise, plain, pedagogical. Short declarative sentences. Prefer concrete verbs. No marketing tone, no exclamation marks.
3. **Sentence case** for headings inside body text; **title case** only for short lesson titles (they double as page titles).
4. **Punctuation**: convert all full-width punctuation（，。；：？！“”‘’（）、）to Western punctuation. Use double quotes for quoted words; curly quotes optional but be consistent (prefer straight quotes in code contexts). Use en dashes for ranges (15–25 minutes).
5. **Do not translate**: URLs, file paths, HTML attribute names, `data-*` attributes, ids/classes, localStorage key names (`practice`, `project`, `revision`, `micro`, `rewrite`, `art-plan:`), variable names, `kind` keys (`visual`, `line`, `space`, `text`, `rhythm`, `motion`, `sequence`, `interactive`), the field separator `｜` (U+FF5C) used in data rows.
6. **Separators**: the Chinese modules join term lists with `、`. In English use comma+space `, `. Any code that splits `subs`/terms must split on `, ` accordingly (the English generator code already does this — data authors must simply never emit `、`).
7. **Numbers/durations**: "Lesson 1 of 9", "15–25 minutes", "2–4 hours", "45–90 minutes".
8. **Chinese-culture terms**: on first occurrence give pinyin (no tone marks) + English gloss in parentheses, then use the English word alone: e.g. "cunfa (texture strokes)", "shanshui (landscape) painting", "Kunqu opera", "quyi (narrative telling and singing)". For concepts with established English names, use the English name alone: literati painting, blue-and-green landscape, Peking opera, ukiyo-e, readymade, contact improvisation.
9. **Artist/artwork names**: standard pinyin (Wang Xizhi, Zhao Mengfu, Guo Xi, Wu Zhen) + accepted English title of the work, e.g. "the Lanting xu (Orchid Pavilion Preface)". Western names as commonly written (Monet, Duchamp, Dürer).
10. **Institutions**: official English names — The Palace Museum (Beijing), National Palace Museum (Taipei), The British Museum, The Metropolitan Museum of Art, MoMA, V&A, Musée du Louvre, Rijksmuseum, etc.
11. **Keep semantic hedges**: the source repeatedly marks limits ("这是教学示意，不是历史作品", "不能等同于", "尚无"). Preserve every such caveat — do not strengthen claims.
12. Keep HTML structure inside strings identical (same tags, same `target="_blank" rel="noopener"`, same `<br>`, `<b>`, `<details>`, `<summary>`).

## 3. Fixed site chrome translations

| zh | en |
|---|---|
| 艺术学习室 | Art Study Room |
| 个人艺术通识教材 | A personal art-fundamentals course |
| 欣赏方法卡（导航）/ 作品欣赏方法卡（页题） | Method Card (nav) / How to Look: A Method Card (page title) |
| 五阶段路线（从入门走向独立创作与研究） | From Beginner to Independent Practice and Research |
| 核心概念自检清单 | Core Concepts Self-Check List |
| 核心术语表 | Core Glossary |
| 锚点时间线 | Anchor Timeline |
| 艺术分类扩展索引 | Expanded Index of Art Categories |
| 分类与教材覆盖表 | Taxonomy and Course Coverage Chart |
| 五步，随时可用 | Five steps, usable anywhere |
| 门类目录 / {name}目录 | {name} index |
| 下一课 / 上一课 | Next lesson / Previous lesson |
| 阶段路线 | Stage roadmap |
| 阶段 | Stage |
| 入门 | Introductory |
| 基础 | Foundational |
| 进阶 | Intermediate |
| 高级 | Advanced |
| 独立项目与大师研读 / 独立创作与研究／大师研读 | Independent project and masterwork study |
| 大师研读 | masterwork study |
| 分组微课 | group micro-lesson |
| 阅读锚点 | Reading anchor |
| 观察实验：只改一个变量 | Observation lab: change one variable |
| 快速自检 | Quick self-check |
| 做一次练习 | Do one exercise |
| 看一个例子 | Study one example |
| 理解一个概念 | Understand one concept |
| 把知识留下来 | Keep the knowledge |
| 已完成本课（请在明天闭卷复述） | Lesson completed (recite it from memory tomorrow) |
| 回答正确。 | Correct. |
| 请再想一想。 | Think again. |

## 4. The 14 units: names (exact), folder slugs (exact)

| # | zh name | en DATA name | folder slug |
|---|---|---|---|
| 00 | 艺术通识 | Art Fundamentals | 00-art-fundamentals |
| 01 | 绘画与版画 | Painting and Printmaking | 01-painting-and-printmaking |
| 02 | 书法与篆刻 | Calligraphy and Seal Carving | 02-calligraphy-and-seal-carving |
| 03 | 雕塑与装置 | Sculpture and Installation | 03-sculpture-and-installation |
| 04 | 建筑与景观 | Architecture and Landscape | 04-architecture-and-landscape |
| 05 | 工艺与设计 | Craft and Design | 05-craft-and-design |
| 06 | 摄影 | Photography | 06-photography |
| 07 | 文学与叙事 | Literature and Narrative | 07-literature-and-narrative |
| 08 | 音乐与声音艺术 | Music and Sound Art | 08-music-and-sound-art |
| 09 | 舞蹈与身体艺术 | Dance and Body-Based Art | 09-dance-and-body-based-art |
| 10 | 戏剧戏曲与现场表演 | Theatre, Chinese Opera and Live Performance | 10-theatre-chinese-opera-and-live-performance |
| 11 | 电影动画与视听 | Film, Animation and Audiovisual Arts | 11-film-animation-and-audiovisual-arts |
| 12 | 数字媒介与游戏艺术 | Digital Media and Game Art | 12-digital-media-and-game-art |
| 13 | 民间艺术与跨媒介 | Folk Art and Intermedia | 13-folk-art-and-intermedia |

## 5. The 33 group names (exact — these are dict keys and must match everywhere)

- 00: 历史与理论→History and Theory; 人与制度→People and Institutions; 收藏与保护→Collecting and Conservation
- 01: 材料与技法→Materials and Techniques; 版画与出版→Printmaking and Publishing; 画面问题→Pictorial Questions
- 02: 书体→Script Styles; 研究与实践→Research and Practice
- 03: 形制与媒材→Forms and Media; 空间与事件→Space and Events
- 04: 空间尺度→Spatial Scales; 观察维度→Dimensions of Observation
- 05: 工艺材料→Craft Materials; 设计领域→Design Fields
- 06: 类型与用途→Genres and Uses; 技术与呈现→Technology and Presentation
- 07: 文类→Literary Genres; 叙事与语言→Narrative and Language
- 08: 创作与实践→Creation and Practice; 学习维度→Dimensions of Study; 传统与类型→Traditions and Genres
- 09: 实践与传统→Practices and Traditions; 创作与研究→Creation and Research
- 10: 戏剧与综合舞台→Theatre and the Integrated Stage; 戏曲与曲艺→Xiqu and Quyi; 现场及协作→Live Performance and Collaboration
- 11: 视听形式→Audiovisual Forms; 动画→Animation; 制作与研究→Production and Research
- 12: 交互与计算→Interaction and Computation; 游戏与沉浸→Games and Immersion
- 13: 生活中的艺术→Art in Everyday Life; 跨媒介实践→Intermedia Practices

## 6. Core domain terminology (zh → en). Use exactly; stay consistent.

**Foundations / method**
- 形式分析 formal analysis; 描述/解释/评价 description / interpretation / evaluation; 证据 evidence; 推断 inference; 观察 observation
- 构图 composition; 明度 value; 色相 hue; 饱和度 saturation; 互补色 complementary colors; 冷暖 warm and cool colors; 邻色 neighboring colors
- 图像学 iconography (Panofsky's three steps: pre-iconographic description, iconographic analysis, iconological interpretation)
- 美学 aesthetics; 艺术史学史 historiography of art history; 视觉文化 visual culture; 比较艺术学 comparative art studies
- 赞助制度 patronage; 艺术市场 art market; 策展 curating; 博物馆学 museology; 收藏史 history of collecting
- 来源研究 provenance research; 文物保护/预防性保护 conservation / preventive conservation; 数字保存 digital preservation
- 模仿论 theory of imitation (mimesis); 表现论 expression theory; 形式主义 formalism; 制度理论 institutional theory of art
- 谢赫“传移模写” Xie He's sixth principle, "transmission by copying" (transcribe-and-copy); 言志／缘情 "poetry articulates intent" (shi yan zhi) / "follows from feeling" (yuan qing)

**Painting / printmaking**
- 素描 drawing; 速写 sketching; 水墨 ink painting; 油画 oil painting; 水彩 watercolor; 水粉 gouache; 丙烯 acrylic; 蛋彩 egg tempera; 粉彩 pastel; 壁画 mural
- 山水 shanshui (landscape); 风景 landscape; 青绿山水 blue-and-green landscape; 花鸟 bird-and-flower; 静物 still life; 历史画 history painting; 文人画 literati painting
- 皴法 cunfa (texture strokes); 披麻皴 hemp-fiber strokes (pima cun); 斧劈皴 axe-cut strokes (fupi cun); 三远 three distances (high, deep, level); 郭熙《林泉高致》 Guo Xi's Linquan gaozhi (The Lofty Message of Forests and Streams)
- 题跋 colophon; 印章 seal; 书画同源 calligraphy and painting share one source
- 线性透视 linear perspective; 固定视点 fixed viewpoint; 散点/移动视点 moving viewpoint
- 木版 woodcut; 铜版 intaglio engraving/etching; 石版 lithography; 丝网 screenprint; 套色 multi-block color printing; 《十竹斋书画谱》 Ten Bamboo Studio Manual of Calligraphy and Painting; 艺术家书 artists' books; 版数 edition number; 损版 plate wear
- 印象派 Impressionism; 现代主义 modernism

**Calligraphy / seals**
- 篆书 seal script; 隶书 clerical script; 楷书 regular script; 行书 running script; 草书 cursive script; 五体 the five script styles
- 隶变 the clerical transformation (libian); 波磔／蚕头燕尾 the wavelike flaring stroke ("silkworm head, swallow tail")
- 笔法 brushwork; 结体 character structure; 章法 overall composition; 行气 flow through a column; 中锋／侧锋 centered tip / inclined tip
- 碑学 stele studies (beixue); 帖学 modelbook studies (tiexue); 碑帖 steles and modelbooks; 拓本 ink rubbing; 摹本 tracing copy; 刻本 carved edition
- 《兰亭序》 Lanting xu (Orchid Pavilion Preface); 神龙本 the Shenlong copy
- 篆刻 seal carving; 朱文 zhuwen (relief, red characters); 白文 baiwen (intaglio, white characters); 印泥 seal paste; 钤印 stamping a seal; 印学 seal studies; 篆法 seal-script lettering

**Sculpture / installation**
- 圆雕 sculpture in the round; 浮雕 relief (high/low relief 高浮雕/薄浮雕); 透雕 openwork; 负空间 negative space
- 现成品 readymade; 装置 installation; 场域特定艺术 site-specific art; 声音装置 sound installation; 公共艺术 public art; 大地艺术 land art; 纪念性艺术 monumental art; 社会参与式艺术 socially engaged art

**Architecture / landscape**
- 动线 circulation; 平面 plan; 剖面 section; 立面 elevation; 梁柱框架 column-and-beam frame; 墙体承重 load-bearing wall; 拱券 arch; 穹顶 dome; 桁架 truss; 悬索 suspension cables
- 园林 garden; 景观 landscape; 城市设计 urban design; 公共空间 public space; 乡土建筑 vernacular architecture; 适应性再利用 adaptive reuse; 遗产保护 heritage conservation; 无障碍 accessibility

**Craft / design**
- 陶瓷 ceramics; 金工 metalwork; 首饰 jewelry; 珐琅 enamel; 漆艺 lacquer; 玻璃 glass; 织造 weaving; 染色 dyeing; 刺绣 embroidery; 装帧 bookbinding
- 平面设计 graphic design; 视觉传达 visual communication; 字体 typography; 信息设计 information design; 包装 packaging; 交互设计 interaction design; 服务设计 service design; 推测设计 speculative design; 社会创新 social innovation; 视觉层级 visual hierarchy

**Photography**
- 纪实 documentary; 新闻 photojournalism; 街头 street photography; 风光 landscape; 观念 conceptual; 摆拍 staged photography; 科学影像 scientific imaging
- 模拟摄影 analog photography; 暗房 darkroom; 无相机摄影 cameraless photography; 摄影书 photobook; 快门 shutter; 光圈 aperture; 感光度 ISO/sensitivity; 景深 depth of field; 焦距 focal length; 广角 wide-angle; 长焦 telephoto; 图注 caption

**Literature**
- 意象 imagery; 节奏 rhythm; 叙述者 narrator; 视角 point of view; 细读 close reading; 修辞 rhetoric; 韵律 meter/prosody; 抒情 lyric; 报告文学 reportage; 口述文学 oral literature; 寓言 fable; 散文随笔 essay; 回忆录 memoir; 图像叙事 visual narrative; 跨媒介叙事 transmedia storytelling

**Music / sound**
- 节拍 meter (steady beat = steady pulse); 节奏 rhythm; 旋律 melody; 音色 timbre; 音高 pitch; 响度 loudness; 音程 interval; 调式 mode; 和声 harmony; 复调 polyphony; 曲式 musical form; 配器 orchestration; 民族音乐学 ethnomusicology
- 声乐 vocal music; 器乐 instrumental; 合唱 chorus; 指挥 conducting; 编曲 arranging; 即兴 improvisation; 电声 electroacoustic; 声音设计 sound design; 声音艺术 sound art; 音景 soundscape; 中国传统音乐 Chinese traditional music; 西方艺术音乐 Western art music

**Dance / body**
- 编舞 choreography; 舞谱 dance notation; 舞蹈影像 dance film/video; 舞蹈剧场 dance theatre (Tanztheater); 接触即兴 contact improvisation; 力度 effort/dynamics; 中国古典舞 Chinese classical dance; 民族民间舞 folk and ethnic dance; 街舞 street dance; 仪式舞蹈 ritual dance

**Theatre / performance**
- 话剧 spoken drama; 戏曲 xiqu (Chinese opera); 京剧 Peking opera; 昆曲 Kunqu opera; 行当 role categories; 程式 conventions (conventionalized forms); 虚拟动作 stylized/imaginary action
- 曲艺 quyi (narrative telling and singing); 相声 crosstalk (xiangsheng); 评书 pingshu storytelling; 鼓曲 drum songs; 弹词 tanci ballads
- 偶戏 puppetry; 物件剧场 object theatre; 肢体剧场 physical theatre; 沉浸式戏剧 immersive theatre; 应用戏剧 applied theatre; 舞美 stage design; 舞台管理 stage management; 音乐剧 musical theatre; 舞剧 dance drama

**Film / AV**
- 景别 shot scale; 远景 long shot; 近景 close shot; 推拉摇移跟 zoom, dolly, pan, tracking, following; 剪辑 editing; 蒙太奇 montage; 分镜 storyboard; 调色 color grading; 视效 visual effects; 散文电影 essay film; 视频艺术 video art; 定格动画 stop motion; 剪纸动画 paper-cut animation; 沙动画 sand animation
- 画内声／画外声 onscreen (diegetic) sound / offscreen sound; 叙事世界 story world (diegesis); 声源 sound source; 配乐 score

**Digital / games**
- 生成艺术 generative art; 算法艺术 algorithmic art; 创意编程 creative coding; 数据艺术 data art; 网络艺术 net art; 软件艺术 software art; 机器人艺术 robotic art; AI艺术 AI art
- 严肃游戏 serious games; 关卡 level design; 游戏叙事 game narrative; 虚拟现实 virtual reality; 增强现实 augmented reality; 混合现实 mixed reality; 沉浸体验 immersive experience

**Folk / intermedia**
- 剪纸 paper cutting; 年画 New Year prints (nianhua); 皮影 shadow puppetry; 灯彩 lanterns; 风筝 kites; 面具 masks; 节庆造型 festive forms
- 行为艺术 performance art; 观念艺术 conceptual art; 生态艺术 ecological art; 参与式艺术 participatory art; 食物艺术 food art; 嗅觉艺术 olfactory art; 生物艺术 bio art; 跨感官 cross-sensory

## 7. Common pedagogical phrases

- 有证据的观察 an evidence-based observation; 可定位的证据 locatable evidence; 待查问题 a question to verify later; 未知写未知 write "unknown" where unknown
- 闭卷复述 recite from memory (book closed); 换对象重做 redo with a different object; 控制练习 controlled exercise; 对照版本 comparison versions
- 验收点 acceptance check; 反馈标准 feedback criteria; 常见误区与纠正 common pitfalls and corrections
- 覆盖表 coverage chart; 门类共同课 shared category course; 尚无独立专业全课程 no dedicated full specialty course yet
- 请分开记录事实与解释 keep facts and interpretations separate
- 这是简化示意，不能代替真实材料或作品 This is a simplified demonstration, not a substitute for real materials or artworks.
- 教学示意／原创教学设计 original teaching design / for-teaching illustration (never claim to quote institutions)
