from pathlib import Path
import html, json

ROOT=Path(__file__).resolve().parent
def write(name,text):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def esc(s):return html.escape(s)

# Each row is an authored teaching unit, not an outline placeholder.
DATA=[
('00','艺术通识','艺术史、美学、艺术批评、策展与博物馆研究','先观察，再解释','visual',[
('把感受变成证据','描述是可指出的位置、声音或动作；解释是对意义的推断；评价是依据标准作出的判断。三者可以相互支持，但不能混为一谈。说“画面令人孤独”还不够：请指出人物间距、视线方向或空白如何支持你的感觉。','一张椅子靠近画框边缘，周围留有大片空白。这是观察；“它暗示被排斥”是解释。也可能是为了突出空间尺度，解释需要保留其他可能。','观察身边一件物品，写三条描述、两种解释和一个待查问题。','有证据的解释是什么？','空白支持孤独感','作者必定很孤独','区分作品可见证据与作者心理；后者需要文献。'),
('把作品放回社会','艺术史不只是风格接力。材料、委托人、宗教、贸易、殖民和传播技术都会影响作品的生产与观看。年代相近的作品也可能服务于完全不同的生活。','比较一件礼仪器物和一张商业海报：它们都组织人的注意力，却面向不同场合与观众。不能仅按逼真程度排列高低。','找两件不同地区的作品，为每件记录年代、材料、用途、收藏机构，未知项明确写未知。','背景研究首先需要什么？','猜想创作者性格','核对材料与用途','先建立可查的资料卡，再讨论社会意义。'),
('写一段有分寸的评论','评论可以依次写：我的问题、作品中的证据、背景资料、另一种解释、暂时判断。审美趣味可以不同，论证仍能讨论。不要把一个地区的传统当作所有艺术的尺度。','“我偏爱安静的构图”是偏好；“重复排列使视线缓慢移动”是可讨论的形式分析。明确自己的标准，会让交流更有效。','写180字评论，并请一位朋友指出其中最缺证据的一句。','怎样改进一段评论？','补充另一种解释','删除所有的疑问','考虑竞争解释，能检验你的判断是否过强。')]),
('01','绘画与版画','素描、水墨、油画、水彩、壁画、版画、插画','看见构图与材料','visual',[
('视线如何移动','构图是画面元素的关系。大小、位置、明暗和重复会改变注意力。先把对象简化成块面，再描述观看顺序，比急着猜题材含义更可靠。','同一个红色圆点放在中央与边缘，会产生不同的平衡关系。中心构图并不自动庄严，效果取决于周围元素。','把一张照片画成三个明暗块；移动其中一块，比较第一眼落点。','最能检验构图的方法？','背诵画家的生日','移动形状作比较','只改变位置，才容易观察位置造成的差异。'),
('颜色与空间','色相区分颜色类别，明度区分亮暗，饱和度区分鲜艳程度。空间可由遮挡、大小、透视或层次表现；不能把单点透视视为唯一正确的空间方式。','一幅水墨山水可以通过山峦重叠和观看路径组织空间；这与固定视点的透视图提供不同体验。','用同一支笔画三层山：只改变遮挡和疏密，不借助颜色。','遮挡主要提供什么线索？','物体前后的关系','作者童年的经历','前景覆盖后景是空间线索，不直接说明作者生平。'),
('材料也在表达','颜料的覆盖性、纸的吸水性和版印的转印过程会留下不同痕迹。版画常通过版与纸的关系产生图像，不能简单理解为绘画复制品。','水彩的透明叠色与厚涂颜料的覆盖，处理修改时会遇到不同限制；限制也可能成为风格资源。','用铅笔侧锋、笔尖、纸片拓印各画一棵树，比较痕迹。','讨论材料应关注什么？','售价越高越优秀','痕迹如何被生成','材料分析关注过程与效果，价格不是艺术质量的充分依据。')]),
('02','书法与篆刻','篆书、隶书、楷书、行书、草书、硬笔、篆刻','从识字走向看线条','line',[
('线条有时间','书法除了文字内容，还可观察起收、转折、粗细与连断。线条是动作留下的痕迹，但仅凭线条无法精确还原书写者的情绪。','相同的“山”字，缓慢描边与一次书写会留下不同转折和节奏；整齐不是唯一评价标准。','用普通笔把山字写三次，分别控制快慢、轻重、大小，只改一个变量。','线条可以直接证明什么？','书写者当天心情','可见的粗细变化','心理推断需要旁证，粗细变化可直接观察。'),
('结体与章法','结体研究单字内部的组织，章法研究整幅作品中字、行、空白的关系。篆隶楷行草是常用书体分类，演变并非一条旧体完全被新体替代的直线。','对照故宫的赵孟頫行书资料，先看字间距离，再看整行重心，不必先认出每个字才开始欣赏。','将四个字排成疏、密两版，说明哪一版的观看节奏更慢。','章法主要关注什么？','整幅字行与空白','单个词语的翻译','章法看整体组织，结体看单字结构。'),
('印面中的正负形','篆刻涉及文字、刀法、材料和印面布局。朱文通常呈红字，白文通常呈白字；红白的组织与边框、残缺共同影响观看。','同一个方形中保留红色线条或去掉红色线条，会使字与底的关系反转。屏幕模拟不能代替真实钤印。','用纸绘制姓名缩写的红白两版印面，不使用刀具。','白文印通常呈现什么？','红字配白色底面','白字配红色底面','白文的字形通常以白色显现在红色印面中。')]),
('03','雕塑与装置','圆雕、浮雕、公共雕塑、现成品、场域装置、声音装置','用身体理解空间','space',[
('绕着作品看','雕塑具有体积，观看位置会改变轮廓、遮挡与重心感。浮雕依托底面，圆雕通常允许从多个方向观看，但实际展陈可能限制路线。','一把椅子正面显得对称，侧面却显出倾斜和支撑。三维作品的照片只提供一个视点。','把纸折成可站立的形体，从三个角度画轮廓。','理解体积更适合怎样做？','只看一张正面照','比较多个观察点','视点变化能揭示单张图片隐藏的关系。'),
('材料与尺度','石、木、金属、纤维或日常物品有不同重量、触感和制作条件。作品尺度与人的身体关系，也影响亲近、压迫或纪念感。','同样的几何体放在掌心与高于人的位置，会改变身体经验；宏大不自动等于深刻。','把纸模型放在杯子旁和玩具人物旁各拍一次，记录尺度感觉。','尺度分析需要比较什么？','作品与人体关系','作者的知名程度','身体提供尺度参照，名气不能说明空间经验。'),
('场地也是媒介','装置往往组织物件、空间、光线或声音的关系，观众路线可能成为作品经验的一部分。并非摆放多件东西就必然构成有效装置。','把椅子排成等候队列或围成讨论圆圈，物品没变，行为暗示改变了。此处是教学实验，不是历史作品。','用三件物品组织一个“等待”的空间，写出观众会如何进入。','场域分析应优先记录什么？','物品的购买价格','路线与环境关系','场地、路线与物件关系能支持意义分析。')]),
('04','建筑与景观','建筑、室内空间、园林、景观、城市空间、遗产保护','空间怎样安排生活','space',[
('读懂平面与动线','平面图像从上方切看空间；动线是人穿行的路线。入口、转折、开口与门槛影响使用，漂亮立面不能代替空间体验。','同样大小的房间，门设在中间或角落，会改变通行路径和家具安排。','画自家一间房的简图，标门窗和最常走的路线。','动线指的是什么？','人穿行空间路线','建筑外墙的颜色','动线关乎行动路径。'),
('光与结构','柱、墙、梁等构件可以承担荷载，也能组织空间节奏。自然光随时间变化，材料表面会改变光的反射与感受。这里只做欣赏，不作结构安全判断。','纸盒侧面开窗与顶部开孔，光的分布不同；这有助理解光如何塑造空间。','在纸盒开两个不同位置的孔，用手电比较照射范围。','研究空间光线应怎样做？','只记录门票价格','比较时段和开口','光的来源与时间变化是可观察变量。'),
('园林与公共生活','景观包含地形、水、植物、路径与人的活动。园林并非只有装饰，城市空间还涉及谁能进入、停留和使用。不同传统不可简单归成自然或人工两类。','一条无座椅的广场与有树荫座椅的广场，对停留行为可能有不同影响，需要实地观察核验。','走一条熟悉的公共路线，记三个可停留处及一个使用障碍。','评价公共空间还应关注什么？','不同人能否使用','照片是否足够贵气','可达性和使用经验也是评价维度。')]),
('05','工艺与设计','陶瓷、金工、漆艺、织绣、玻璃、家具、服装、平面、产品、交互设计','在使用中看形式','visual',[
('物品的形与用','工艺关注材料、技艺与制作传统；设计常处理特定情境中的使用和沟通问题。两者有大量交集，并非手工与机器的简单对立。','一只杯子的把手既影响握持，也影响外形。不能只凭装饰判断它是否好用。','选两个杯子，从握持、清洁、重量、外观各记一条差异。','设计评价需要什么？','先明确使用情境','只比较装饰多少','使用者与任务决定哪些标准相关。'),
('从材料到工序','成型、连接、烧制、染织等过程影响最终形式。观察接缝、纹理与重复痕迹，可以提出制作假设；确认工序仍要查询馆藏说明。','重复纹样可能来自模具或重复手工；肉眼观察不能总是断定生产方式。','找一件织物或陶器，画出接缝与纹理，并列出一个待核实的工序问题。','观察工序应避免什么？','记录接缝的位置','把推测当作事实','将可见痕迹与待查工艺分开记录。'),
('视觉层级与责任','字体大小、间距、对比与排列会引导阅读顺序。设计也要考虑可读性、维护、资源消耗和被排除的人群。','一张活动海报如果装饰抢过日期和地点，即使漂亮，也可能无法完成通知任务。','用纸做两版活动通知，邀请别人用五秒找出时间地点。','检验通知有效性可怎样做？','请人寻找关键信息','只统计用了几种色','任务测试直接检验沟通是否成功。')]),
('06','摄影','纪实、肖像、风光、静物、观念、实验摄影','看见取景的选择','visual',[
('画框内外','摄影的取景选择包含什么、排除什么。图像记录来自现实的光，但选时、视点和传播语境也参与意义形成。','同一张桌子，裁掉杂物后可能显得极简；这不是现场全部事实。','用手机对同一场景拍宽、中、近三张，写出各自遗漏了什么。','照片的画框意味着什么？','完整包含现场事实','选择呈现部分现场','照片的证据价值应结合取景与背景。'),
('时间与光','快门时间影响运动痕迹；光的方向影响阴影和质感。曝光效果还与光圈、感光度和场景有关，不能把单个参数当作万能风格公式。','侧光常使表面起伏更明显，正面光可能减弱阴影差异；具体效果需在同一物体上比较。','用窗光拍同一个杯子，转动杯子或改变相机位置，比较阴影。','比较光线最好控制什么？','保持同一拍摄对象','不断更换所有条件','尽量控制其他条件，才能识别光的作用。'),
('图注与伦理','图注交代人物、地点、时间与拍摄背景，帮助限制误读。拍摄与展示涉及同意、隐私与权力；纪实照片不应把未知故事编成事实。','一个低头的人可能在悲伤，也可能在读手机；“低头”可观察，“绝望”需要更多依据。','给一张自己的照片写一条事实图注，再另写你的解释。','事实图注应如何处理未知？','编出动人的故事','明确哪些尚未核实','清楚标明未知，保留图像分析的可信度。')]),
('07','文学与叙事','诗歌、小说、散文、戏剧文学、口述文学、儿童文学','从语言走向经验','text',[
('意象与节奏','意象通过具体感官细节唤起经验；节奏来自声音、句长、停顿和重复。文学不只是在句子里隐藏一个可翻译的道理。','“窗台上的杯子冷了”比“时间过去了”提供更多感官线索。两句都可有效，选择取决于写作目的。','把“我很想家”改成三个不直接写情绪的具体细节。','哪种分析更贴近语言？','指出重复与停顿','只猜作者的星座','文本分析先寻找词句中的证据。'),
('谁在讲故事','叙述者是讲故事的声音，不等同于作者本人。视角决定读者能知道什么；第一人称可能真诚，也可能误解事件。','“我看见他把信收起”提供动作，却不能证明对方心里在想什么。有限信息会产生悬念。','用旁观者和当事人各写80字同一场告别，标出信息差。','第一人称叙述者必定是谁？','小说作者的本人','作品内讲述的声音','作者创造叙述者，二者不能自动等同。'),
('细读与比较','细读从字词、句式和结构出发，比较则明确共同问题。译文包含译者的选择，跨语言比较要注明版本，避免把译句直接当成原文声音。','比较两首写雨的诗，可看雨是背景、行动阻力还是情绪触发，而非只比哪首更美。','选一首熟悉的古诗，圈出动词，解释换掉其中一个会失去什么。','比较作品前应先明确什么？','比较所依据的问题','哪位作者更有名气','共同问题能让比较有可讨论的依据。')]),
('08','音乐与声音艺术','声乐、器乐、作曲、民间音乐、古典、爵士、流行、电子、实验声音','学会有目的地听','rhythm',[
('节拍与节奏','稳定拍点像时间参照，节奏是声音与停顿的长短组织。速度影响拍点间隔；节奏型可以在不同速度下保持相同关系。','连续拍四下手，再把第二下换成停顿：参照拍点仍可持续，实际声音排列已改变。','按页面拍点练习，先每拍一下，再隔拍一下；口中持续数拍。','速度变化首先改变什么？','拍点之间的间隔','乐器本身的材料','速度改变时间间隔，不会改变乐器材料。'),
('旋律与音色','旋律可观察音高走向、重复和句尾；音色帮助区分发声特点。先画旋律轮廓，不识谱也能开展聆听。声音大小与音高不是同一维度。','同一旋律由人声与笛子演奏，轮廓可以相似，发声质感却不同。','哼一段熟悉旋律，用上升下降线条画轮廓，再改变哼唱音色。','音高与响度的关系是什么？','高音必定声音更大','两个可分辨的维度','高低与大小应分别聆听。'),
('重复、变化与聆听语境','结构可以通过重复、对比和回归被听见。标记A、B只是分析工具，不是所有音乐都必须符合的模板。音乐在仪式、舞蹈与录音播放中的功能也不同。','一个片段再次出现时，可以保持旋律却改变配器；听到回归不代表所有细节相同。','选一首熟悉歌曲，画出段落时间线，标记重复处和一次变化。','判断段落回归应怎样做？','比较相似与变化处','只凭歌曲标题判断','回归需要聆听材料之间的关系。')]),
('09','舞蹈与身体艺术','古典、民族民间、芭蕾、现代、当代、街舞、舞蹈编创','动作如何成为表达','motion',[
('身体、空间与时间','舞蹈可从身体部位、动作、空间、时间和力度观察。先记录发生了什么，再讨论情绪；一个动作没有在所有文化中固定相同的含义。','伸手可以是邀请、阻挡或寻找；方向、速度及与他人的距离会改变理解。','坐着用手做伸出与收回，分别缓慢和突然，记录感受差异。','分析舞蹈应先记录什么？','舞者必定有多悲伤','动作方向速度力度','先观察动作，再提出情绪解释。'),
('动作关系与编排','齐舞、轮流、重复和对比形成群体关系。舞蹈技巧与表达相关，但高难度动作不是唯一价值标准。','两人先同步举手，再错开一拍，视觉关系会从一致转向呼应。','用两个手指扮演两位舞者，做同步与轮流两版短句。','轮流动作最直接改变什么？','动作之间时间关系','表演服装制作材料','编排改变动作的先后与呼应。'),
('文化与观看','舞蹈可能参与礼仪、社交、舞台演出或身份表达。欣赏不同传统应查询表演者与社群的说明，避免把陌生动作当作猎奇符号。','同一舞步在社区庆典与剧院舞台中，参与方式和观看距离可能不同。','观看一段正规机构发布的舞蹈，记录场合、参与者和三个动作证据。','跨文化欣赏应怎样做？','先了解社群与场合','直接按熟悉程度排位','背景有助理解动作在当地的意义。')]),
('10','戏剧戏曲与现场表演','话剧、戏曲、歌剧、音乐剧、木偶、曲艺、杂技、表演艺术','看懂行动与约定','text',[
('人物想做什么','戏剧行动可以从人物目标、阻力和策略观察。台词之外，停顿、走位与回应也在传递关系。人物不是只有一种性格标签。','“留下来”可以是请求，也可以是命令；对方的反应使关系更清楚。','把“把门打开”分别作为请求、威胁、试探说出，比较停顿。','分析行动可先问什么？','人物此刻想达成什么','演员生活中喜欢什么','目标和阻力是分析舞台行动的有效入口。'),
('舞台的共同约定','表演与观众依靠约定理解虚构。戏曲的程式、虚拟动作和角色行当有各自传统，不能以是否模仿日常生活作为唯一标准。','没有真马，演员仍能通过动作让观众理解骑马；理解来自表演符号与观看经验。','用空手表现端一碗很满的水，请别人猜，并讨论哪些动作有帮助。','理解虚拟表演需要什么？','只看道具是否昂贵','理解动作符号约定','表演可以通过约定传达并未实物呈现的情境。'),
('舞台是协作艺术','导演、演员、舞美、灯光、服装与声音共同组织观看。剧本文字与具体演出不是同一个对象，比较演出应记录制作版本。','一句台词前的灯光变暗与长停顿，可能改变观众的期待，但意义还要看前后情境。','为两句对话写两版灯光、走位说明，解释你想改变的关系。','比较演出需要注明什么？','具体演出的制作版本','只注明故事里的地点','制作版本能帮助区分不同舞台处理。')]),
('11','电影动画与视听','剧情、纪录、实验电影、动画、影视、短片、视频艺术','看懂镜头怎样连接','sequence',[
('镜头选择信息','景别控制人物与环境的比例；角度与运动改变观看位置。镜头是选择信息的单位，不能只用“好看”概括它的功能。','远景可让我们看见人物与环境关系，近景可强调面部或物件；它们没有固定情绪效果。','用手机拍同一杯子的远景与近景，说明两张各提供什么信息。','景别变化直接影响什么？','画面包含的信息范围','导演必定持有的观点','景别改变信息范围，意义仍依赖语境。'),
('剪辑制造关系','剪辑通过先后、时长与并置组织理解。相同表情接不同物件，可能引导不同推断；观众推断不等于人物真实心理。','“脸—食物”与“脸—空椅子”可能让同一个表情被理解得不同。这是教学示意。','用页面交换镜头顺序，写一句故事，再说出它依赖的推断。','镜头顺序可以改变什么？','观众对关系的推断','素材文件原始的尺寸','剪辑组织意义，不自动改变原始素材。'),
('声音与动画时间','画内声有画面中的可见声源，画外声的声源未在画面中显现；还要区分叙事世界内外的声音。动画通过连续图像的时间组织产生运动体验。','一幅空走廊配脚步声，会让观众期待有人靠近。声音可以提供画面没有展示的信息。','给一段十秒静态场景设计两种声音方案；说明各让人期待什么。','声音分析还需要关注什么？','声源与叙事世界关系','只关注画面颜色数量','声源是否可见、是否属于故事世界，是不同问题。')]),
('12','数字媒介与游戏艺术','交互艺术、生成艺术、网络艺术、游戏、虚拟现实、增强现实、AI艺术','规则也能成为媒介','interactive',[
('交互改变什么','交互作品接收参与者输入，并以规则产生反馈。按钮本身不是艺术意义；关键是输入、规则与体验之间如何联系。','本页的滑块改变形状间距，参与者会感到疏密变化。它演示规则，不代表成熟艺术作品。','设计一个只用一个按钮的作品：写出输入、规则、反馈与主题。','交互分析的重点是什么？','输入规则反馈的关系','按钮使用了几种颜色','交互的意义来自行动与反馈之间的联系。'),
('游戏的规则与选择','游戏用规则、目标、资源与反馈塑造行动。叙事既可来自文字影像，也可来自玩家的选择和系统后果。','若每次帮助别人都会消耗自己的时间，玩家面对的取舍能成为体验的一部分；还需看规则是否真的允许选择。','设计一个三回合纸上游戏，规定一种资源和两种用途，试玩后修改。','检验选择是否有意义看什么？','后果是否有所差别','菜单文字是否足够长','不同选择需要在体验或结果中形成可感知差异。'),
('生成系统与作者责任','生成艺术用规则产生多种结果。使用AI时，要记录工具、输入、筛选与修改，并讨论来源、权利和数据中的偏向。随机不等于没有作者选择。','设定颜色范围、数量与淘汰标准，已经在塑造生成结果。不能仅凭图像外观确认其数据来源。','写一个用骰子决定线条方向的规则，做三次结果，记录你保留哪张及原因。','讨论生成作品应记录什么？','规则筛选与修改过程','只看最终图片的大小','过程记录有助分析作者选择与系统作用。')]),
('13','民间艺术与跨媒介','剪纸、年画、皮影、民间叙事、节庆艺术、行为艺术、跨媒介实践','在生活关系中理解艺术','visual',[
('作品与生活场合','民间艺术常与地方生活、节令、信仰、家庭或行业相连。民间不等于匿名、古老或不变化；应留意具体制作者与社群。','同一种剪纸在窗户、礼俗物品与美术馆中，面对不同观众，功能也可能改变。','向家人询问一种节庆物品的使用方式，区分亲历与听说。','记录民间艺术应重视什么？','具体社群与使用场合','直接称为永恒的传统','具体时间地点与使用者能避免空泛概括。'),
('剪影、叙事与协作','皮影等形式可以结合造型、操纵、音乐与讲述。按材料分类很方便，却可能切断作品实际的跨媒介经验。','纸片形状只是影戏的一部分；操纵的节奏和讲述会影响角色是否鲜活。','用纸剪一个简单轮廓，在手电前移动，配两句旁白。','理解影戏还要观察什么？','操纵声音与叙事关系','只数纸片用了几种色','多种媒介共同形成表演经验。'),
('跨界与有根据的判断','行为与跨媒介艺术可能把身体、事件、文本或制度本身作为材料。判断不能只停在“这也算艺术吗”，可追问规则、语境、观众经验与作品提出的问题。','把日常排队改成一段被组织、被说明的事件，会改变观看框架；是否有价值仍需具体分析。','设计一个不打扰他人的一分钟“等待”作品，写明规则与希望观众思考的问题。','批评跨媒介作品可怎样开始？','先核对其规则与语境','仅凭陌生感直接否定','理解作品如何运行，才能提出具体批评。')])]

SOURCES={
'visual':('Getty：形式分析','https://www.getty.edu/education/teachers/building_lessons/formal_analysis.html','查看线条、形体、空间、色彩的定义与馆藏示例。'),
'line':('故宫：赵孟頫行书洛神赋卷','https://intl.dpm.org.cn/Calligraphy_collection/63948.html','结合馆方对结体、点画和布局的说明观看。'),
'space':('V&A：馆藏检索','https://www.vam.ac.uk/collections','检索 sculpture、architecture 或 furniture，选择有材料、尺寸资料的对象。'),
'text':('V&A：馆藏与主题','https://www.vam.ac.uk/collections','检索 theatre，观察表演相关的设计文献；文学课主要使用你手头可核对版本的原作。'),
'rhythm':('Carnegie Hall：音乐教学工具箱','https://www.carnegiehall.org/Education/Programs/Music-Educators-Toolbox','选择 Rhythm & Meter 或 Singing，跟随原机构的练习。'),
'motion':('BC课程：舞蹈元素','https://curriculum.gov.bc.ca/content/ccdance-foundationsgrade-11elements-de-la-danse','核对身体、空间、时间与力度的观察维度。'),
'sequence':('BFI：阅读短片或场景','https://ugc.futurelearn.com/uploads/files/d3/95/d395220f-bbb0-4e76-810f-e3caca25727b/Reading_a_short_film_or_scene.pdf','使用BFI的问题表观察镜头、剪辑与声音。'),
'interactive':('V&A：馆藏检索','https://www.vam.ac.uk/collections','检索 digital design 或 video games，结合对象记录研究媒介。')}

CSS='''*{box-sizing:border-box}body{margin:0;background:#f5f1e9;color:#263b38;font:18px/1.85 system-ui,"Microsoft YaHei",sans-serif}header,main,footer{max-width:1050px;margin:auto;padding:32px}header{padding-top:65px}h1{font-family:Georgia,"Microsoft YaHei",serif;font-size:clamp(32px,5vw,58px);line-height:1.25;font-weight:500;margin:20px 0}h2{font-size:26px}h3{font-size:21px}a{color:#176458;text-underline-offset:5px}nav{display:flex;gap:20px;flex-wrap:wrap}.eyebrow{font-size:13px;letter-spacing:3px;color:#9b5839}.lead{font-size:21px;max-width:780px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:20px}.card,section{background:#fffdf8;border:1px solid #ddd7c9;padding:26px;margin:22px 0;border-radius:6px}.card{margin:0}.muted,small{color:#61706b}button,select{font:inherit;padding:10px 18px;background:#25564c;color:white;border:0;border-radius:4px;cursor:pointer;margin:5px}button:hover{background:#163f36}button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid #b85a30;outline-offset:4px}textarea{width:100%;min-height:140px;font:inherit;padding:12px;border:1px solid #9baba3;background:white}label{display:block;margin:12px 0}input[type=range]{width:100%}.lab{background:#e9eee5;padding:25px}.stage{height:170px;display:flex;align-items:center;justify-content:center;gap:25px;overflow:hidden}.shape{width:70px;height:90px;background:#b05e3f;border-radius:50% 50% 4px 4px;transition:transform .4s,margin .4s}.shape:nth-child(2){background:#345e61}.shape:nth-child(3){background:#c6a654}output{display:block;font-size:15px}details{margin:15px 0;border-left:3px solid #b88864;padding-left:16px}summary{cursor:pointer;font-weight:600}.feedback{min-height:2em;color:#23594c}.tag{font-size:14px;border-bottom:1px solid #c9bca5;padding:4px}footer{font-size:14px}.progress{font-size:14px}svg{width:100%;max-height:190px}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:12px;border-bottom:1px solid #ddd}@media(max-width:600px){header,main,footer{padding:22px}section{padding:18px}}@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}@media print{body{background:white;font-size:12pt}header,main,footer{padding:8px}button,textarea,.lab,.progress{display:none}section{break-inside:avoid}details> *{display:block}a{color:black}}'''
JS='''document.querySelectorAll('[data-quiz]').forEach(q=>{q.querySelectorAll('button').forEach(b=>b.onclick=()=>{q.querySelector('.feedback').textContent=(b.dataset.correct==='true'?'回答正确。':'请再想一想。')+q.dataset.feedback;});});document.querySelectorAll('textarea[data-note]').forEach(t=>{try{t.value=localStorage.getItem(location.pathname+t.dataset.note)||''}catch{}t.addEventListener('input',()=>{try{localStorage.setItem(location.pathname+t.dataset.note,t.value)}catch{}})});document.querySelectorAll('[data-complete]').forEach(b=>{b.onclick=()=>{b.textContent='已完成本课（请在明天闭卷复述）';try{localStorage.setItem(location.pathname+'done','1')}catch{}}});let r=document.querySelector('#variable');if(r){const stage=document.querySelector('.stage');const out=document.querySelector('#lab-result');function update(){let v=+r.value,kind=stage.dataset.kind;stage.style.gap=(v/2)+'px';stage.querySelectorAll('.shape').forEach((x,i)=>{x.style.transform=kind==='motion'?'translateY('+((i-1)*v/3)+'px) rotate('+(v-50)+'deg)':kind==='line'?'scaleX('+(0.3+v/60)+')':kind==='space'?'perspective(400px) rotateY('+v+'deg)':'translateY(0)';});out.textContent='当前变量：'+v+'。请比较疏密、重心或轮廓；意义解释需要你另外提出证据。'}r.oninput=update;update()}let swap=document.querySelector('#swap');if(swap)swap.onclick=()=>{let s=document.querySelector('#shots');s.append(s.firstElementChild);document.querySelector('#shot-result').textContent='顺序已改变。写下你推断的故事，并区分画面事实与联想。'};let play=document.querySelector('#beat');let timer=null,ctx=null,count=0;function stop(){clearInterval(timer);timer=null;if(play)play.textContent='开始四拍循环';}if(play){play.onclick=()=>{if(timer){stop();return}try{ctx=ctx||new(window.AudioContext||window.webkitAudioContext)();ctx.resume();function tick(){let o=ctx.createOscillator(),g=ctx.createGain();o.connect(g);g.connect(ctx.destination);o.frequency.value=count%4===0?660:440;g.gain.setValueAtTime(.08,ctx.currentTime);g.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+.08);o.start();o.stop(ctx.currentTime+.09);document.querySelector('#beat-result').textContent='第 '+(count%4+1)+' 拍';count++}tick();timer=setInterval(tick,60000/+document.querySelector('#tempo').value);play.textContent='停止声音'}catch{document.querySelector('#beat-result').textContent='浏览器不支持声音，请自行匀速数四拍。'}};document.querySelector('#tempo').oninput=stop;document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()})}'''
write('assets/style.css',CSS);write('assets/course.js',JS)

def page(title,body,depth=0,sub='ART / HUMANITIES',nav=''):
    pre='../'*depth
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · 艺术学习室</title><link rel="stylesheet" href="{pre}assets/style.css"><script defer src="{pre}assets/course.js"></script></head><body><header><nav><a href="{pre}index.html">艺术学习室</a><a href="{pre}reference/method.html">欣赏方法卡</a>{nav}</nav><p class="eyebrow">{sub}</p><h1>{esc(title)}</h1></header><main>{body}</main><footer>个人艺术通识教材 · 2026-11-01 · 本站示意图为原创教学模型，不是历史作品。正文与练习可离线使用，外部馆藏需联网。<br>遇到不清楚的概念，把课名、你的答案和疑问发给老师继续讨论。</footer></body></html>'''

def lab(kind):
    if kind=='rhythm':return '''<div class="lab"><h3>听见拍点</h3><p>先开声音数四拍，再只在第1、3拍拍手；高音只是标记第一拍。停止后尝试自行保持拍点。</p><label>速度（每分钟拍数）<input id="tempo" type="range" min="40" max="160" value="80"></label><button id="beat">开始四拍循环</button><output id="beat-result" aria-live="polite">等待开始</output></div>'''
    if kind=='sequence':return '''<div class="lab"><h3>镜头顺序实验</h3><div id="shots" class="grid"><div class="card">① 面孔：一个人望向画外</div><div class="card">② 物件：桌上未动的饭</div><div class="card">③ 空间：一把空椅子</div></div><button id="swap">轮换镜头顺序</button><output id="shot-result" aria-live="polite">哪些是你看见的，哪些是你推断的？</output></div>'''
    if kind=='text':return '''<div class="lab"><h3>同一句话，两个版本</h3><p>原创示例：“你终于来了。”</p><details><summary>版本一：在门口等候，迅速迎上</summary><p>动作可支持期待或欢迎的解释，但还要核对前后文。</p></details><details><summary>版本二：背向门口，停顿后低声说</summary><p>同一句话可能被读作失望、怀疑或克制。请指出动作证据，保留其他解释。</p></details><p>试着只改变一个动词或停顿，预测理解如何变化。</p></div>'''
    return f'''<div class="lab"><h3>观察实验：只改一个变量</h3><p>拖动后先描述形状关系，再提出解释。这是简化示意，不能代替真实材料或作品。</p><div class="stage" data-kind="{kind}" role="img" aria-label="三个可调间距的形状"><div class="shape"></div><div class="shape"></div><div class="shape"></div></div><label>调整{'线条宽度与间距' if kind=='line' else '视角与间距' if kind=='space' else '动作幅度与间距' if kind=='motion' else '形状间距'}<input id="variable" type="range" min="0" max="100" value="40"></label><output id="lab-result" aria-live="polite"></output></div>'''

TOTAL_LESSONS=9  # 每门最终9课：01–03课由本文件生成，04–09课由 extend_course.py 追加。

def build_base():
    """生成入门阶段（每门01–03课）、共享资源与中间页面；完整站点的唯一入口是 extend_course.py。"""
    cards=[];readme=[]
    for num,name,subs,goal,kind,lessons in DATA:
        folder=f'{num}-{name}'
        source=SOURCES[kind]
        if num in ['05','13']:source=SOURCES['space']
        if num=='07':source=('亚里士多德《诗学》英译本','https://www.gutenberg.org/ebooks/1974','选读关于诗与行动的段落；这是一个历史理论视角，不代表所有文学传统。本课细读仍以你手头注明版本的原作为准。')
        if num=='10':source=('V&A：戏剧与表演馆藏','https://www.vam.ac.uk/collections/theatre-performance','从服装、舞台设计与表演档案观察协作过程；其英国馆藏不能代替中国戏曲的专门资料。')
        if num=='12':source=('V&A：游戏展览的设计问题','https://www.vam.ac.uk/articles/about-videogames-exhibition','观察游戏从设计到参与的讨论；本课的纸上游戏是原创练习。')
        route=''.join(f'<li>{esc(x)}：先找一件可靠原作，记录材料或媒介；用本门类的观察方法写100字分析，再做一次小练习。</li>' for x in subs.split('、'))
        lessonlinks=''.join(f'<li><a href="lessons/{i:02}.html">第{i}课 · {l[0]}</a>（15–25分钟）</li>' for i,l in enumerate(lessons,1))
        write(f'{folder}/index.html',page(name,f'<p class="lead">{goal}。本单元先训练三项可迁移的欣赏能力，再沿子分支深入。</p><section><h2>现在开始学</h2><ol>{lessonlinks}</ol><p>先修：<a href="../00-艺术通识/index.html">艺术通识</a>；无需绘画或乐理基础。</p></section><section><h2>子分支地图</h2><p>以下是后续学习路线，不代表这些子领域已各有完整专门课程；类别之间允许重叠。</p><ul>{route}</ul></section><section><h2>结课作品</h2><p>选择本门类的一件原作或一次现场经验，提交一张资料卡、三条形式证据、一个背景问题和180字评论。用<a href="../reference/method.html">方法卡</a>自评。</p></section>',1,nav=''))
        for i,(title,concept,example,task,question,correct,wrong,feedback) in enumerate(lessons,1):
            choices=[(correct,True),(wrong,False)] if i%2 else [(wrong,False),(correct,True)]
            buttons=''.join(f'<button type="button" data-correct="{str(v).lower()}">{esc(t)}</button>' for t,v in choices)
            links=f'<a href="../index.html">{name}目录</a>'
            if i>1:links+=f'<a href="{i-1:02}.html">上一课</a>'
            if i<TOTAL_LESSONS:links+=f'<a href="{i+1:02}.html">下一课</a>'
            body=f'''<p class="lead">第{i}课 / 共{TOTAL_LESSONS}课 · 15–25分钟<br>本课目标：用“{title}”的方法，增加一条有证据的作品观察。</p><section><h2>01 · 理解一个概念</h2><p>{concept}</p><p class="muted">阅读锚点：<a href="{source[1]}" target="_blank" rel="noopener">{source[0]}</a>。{source[2]}下文的生活例子和练习为原创教学设计，并非该机构的原文或权威结论。</p></section><section><h2>02 · 看一个例子</h2><p>{example}</p>{lab(kind) if i==1 else '<p>回顾第一课的实验：本课概念能否解释其中某一处变化？说出证据与推断之间的差别。</p>'}</section><section><h2>03 · 做一次练习</h2><p>{task}</p><label>先写下答案，再看参考思路<textarea data-note="practice" placeholder="我的观察……我的解释……我尚不知道……"></textarea></label><details><summary>完成后展开：检查思路</summary><p>检查三点：是否完成了指定比较；是否指出具体的形状、动作、词句或声音；是否将事实与解释分开。答案不必与示例感受相同，只要能给出依据。</p><p>本课特别检查：{feedback}</p></details></section><section data-quiz data-feedback="{esc(feedback)}"><h2>04 · 快速自检</h2><p>{question}</p>{buttons}<p class="feedback" aria-live="polite"></p></section><section><h2>05 · 把知识留下来</h2><p>关掉本页，用自己的话解释今天的概念。明天用另一件作品再练一次，七天后把它与另一门类比较。能说术语只是起点，能换作品举证才算迁移。</p><button data-complete>标记本课完成</button><p><small>笔记尽量保存在当前浏览器；本地文件权限或清理缓存可能导致丢失，重要记录请复制到自己的文档。页面不会自动评价开放题。</small></p></section><nav>{links}</nav>'''
            write(f'{folder}/lessons/{i:02}.html',page(title,body,2,f'LESSON {num}.{i:02}',links))
        cards.append(f'<article class="card"><span class="eyebrow">{num} / 3 LESSONS</span><h2><a href="{folder}/index.html">{name}</a></h2><p>{goal}</p><small>{subs}</small></article>')
        readme.append(f'| {num} | [{name}](./{folder}/index.html) | {subs} |')

    write('index.html',page('从作品出发，认识艺术与人',f'''<p class="lead">一套面向零基础的艺术人文自学教材。先学会观察、比较和提问，再逐渐理解作品与它所处的世界。</p><section><h2>第一站：不用先背艺术史</h2><p>从<a href="00-艺术通识/lessons/01.html">通识第一课：把感受变成证据</a>开始。每课15–25分钟，完成一个概念、一个例子、一次练习和一道自检。</p><p>第一轮：每周任选一个门类，学三课，收集一件作品。14周遍览全图；第二轮只选最感兴趣的两个子分支深学。时间安排是建议，可按你的节奏调整。</p><p><a href="reference/method.html">随身方法卡与自评标准 →</a></p></section><h2>十四个学习单元</h2><p>含1个跨门类基础单元、13个创作领域单元。它们是一张学习地图，不是唯一的艺术分类；中国与世界艺术贯穿其中，历史、美学和批评也贯穿各门。</p><div class="grid">{''.join(cards)}</div><section><h2>怎样避免“看完就忘”</h2><ol><li>当天：完成练习，留下一段自己的观察。</li><li>隔天：不看教材，复述概念并换作品举例。</li><li>第七天：比较两个不同门类如何处理相同问题，例如节奏、空间或叙事。</li><li>每四周：回看自己的评论，删掉一句无依据的判断，补上一条具体证据。</li></ol></section>'''))
    write('reference/method.html',page('作品欣赏方法卡','''<section><h2>五步，随时可用</h2><ol><li>资料：名称、创作者或社群、年代、媒介、尺寸或时长、用途、资料来源。未知就写未知。</li><li>观察：我具体看见、听见或经历了什么？先列三条证据。</li><li>关系：重复、对比、重心、节奏、叙述顺序或参与规则如何组织经验？</li><li>背景：谁制作、资助、使用与观看？我还有什么需要核实？</li><li>判断：我的标准是什么？还有哪一种合理解释？</li></ol></section><section><h2>四项自评，每项0–2分</h2><table><tr><th>项目</th><th>0分</th><th>1分</th><th>2分</th></tr><tr><td>证据</td><td>只有感想</td><td>有一条细节</td><td>至少三条具体细节</td></tr><tr><td>概念</td><td>只用好看难看</td><td>能说出术语</td><td>能用术语解释细节</td></tr><tr><td>背景</td><td>凭空推测</td><td>有资料未区分</td><td>注明来源与未知</td></tr><tr><td>判断</td><td>绝对化结论</td><td>提出一种解释</td><td>说明标准及替代解释</td></tr></table><p>总分只帮助发现下一步，不是艺术品味的排名。低于6分时，优先补最弱的一项。</p></section><section><h2>六个常用词</h2><p>媒介：表达所依托的材料、技术或形式。构图：元素在画面中的组织。节奏：事件在时间或空间中的重复与变化。语境：制作、使用、传播与观看的具体背景。形式：作品可感知的组织方式。批评：以证据和标准讨论作品，而非单纯挑错。</p></section>''',1))
    write('README.md','# 艺术学习室\n\n为了增强艺术人文素养：从观察作品出发，学习描述、比较、背景研究与有依据的评论。\n\n## 打开教材\n\n双击根目录 `index.html`，推荐先学“艺术通识”。HTML正文、原创图形实验、自检和练习可离线使用；外部馆藏资料需要联网。无需安装依赖或启动服务。\n\n## 分类原则与主要分支\n\n艺术不存在全球统一、边界互斥的“所有主分支”清单。下表采用广义人文教育视角，覆盖视觉、空间、语言、声音、表演、视听、数字交互及民间跨媒介领域；不是教育部学科目录，也不是固定的“七大艺术”。每行对应一个文件夹，门类有交集，例如歌剧同时联系音乐与戏剧，书法也属于视觉艺术，民间艺术贯穿多个媒介。00为理论基础，其余为主要创作领域的教学分组。\n\n| 编号 | 学习单元及入口 | 主要子分支（代表性地图，非穷举） |\n|---|---|---|\n'+'\n'.join(readme)+'\n\n## 教材范围\n\n已提供14个单元、42节完整入门小课，每课含概念讲解、原创例子、练习、参考思路、自检反馈与复习提示。各目录列出子分支进阶路线。当前是覆盖主要门类的入门教材，并非每个子分支的专业全课程；学完后应按个人兴趣扩展作品专题和历史专题。艺术史、美学、批评、策展与博物馆研究作为贯穿各门的理论研究领域，不与创作媒介混为同一级互斥分类。\n\n## 建议路线\n\n1. 第1周完成通识；之后每周选一个门类，三次各学一课。\n2. 每课15–25分钟；第二天闭卷复述，第7天换原作练习。\n3. 每周留一张作品资料卡和180字评论；每四周比较两门如何处理空间、节奏或叙事。\n4. 第一轮14周完成全景浏览，第二轮选两个子分支深入。时间为建议。\n\n## 文件说明\n\n- `index.html`：总入口；各门类 `index.html`：导学与子分支路线；`lessons/`：三节具体课程。\n- `reference/method.html`：方法、术语与自评卡。\n- `MISSION.md`、`NOTES.md`：目标与教学假设。\n- `RESOURCES.md`：教学方法、机构来源与资料缺口。\n- `_research/teach/`：本次读取的教学skill快照，供溯源；不是全局安装。\n- `build_course.py`：生成教材的源文件；修改此文件后运行 `python build_course.py` 可重建页面（会覆盖已生成教材，请先备份手动修改）。\n\n笔记使用浏览器localStorage尽力保存，file协议的实现因浏览器而异；重要答案请另存。完成标记只作当前页提示，不代表已掌握，不自动生成学习记录。未采集个人数据，也无外部脚本。打印可获得静态讲义，互动实验需在屏幕操作。\n')
    write('MISSION.md','# Mission: 艺术人文素养\n\n## Why\n学习艺术各主要分支，增强艺术人文素养，让日常观看、阅读、聆听和观演成为可以分析与讨论的经验。\n\n## Success looks like\n- 对陌生作品给出三条具体观察，区分事实、解释和评价。\n- 理解主要门类及其子分支，选择自己愿意深学的方向。\n- 能结合可核对的背景写180字评论，并承认资料空缺。\n\n## Constraints\n- 使用中文，优先HTML，可用图形、声音与交互讲解。\n- 暂按零基础设计；时间安排为建议，用户尚未指定。\n\n## Out of scope\n用户未明确排除任何领域；本轮交付范围为通识入门，不推定有专业应试或职业训练需求。\n')
    write('NOTES.md','# 教学偏好与假设\n\n已确认：增强艺术人文素养；希望README列出主分支、每门独立目录、教材优先HTML；先寻找教学skill。\n\n暂定：零基础、中文、欣赏优先且配轻量实践；可后续根据练习调整。未评估实际起点，未声称用户已掌握任何内容。\n\n学习记录应在用户提交练习并得到反馈之后创建，不提前伪造。\n')
    resources='# 艺术学习资源\n\n## Knowledge\n\n'
    for title,url,note in dict((v[1],v) for v in SOURCES.values()).values():resources+=f'- [{title}]({url})：{note}\n'
    resources+='- [Met艺术史时间线](https://www.metmuseum.org/essays/timeline-of-art-history)：按地区、年代和主题查证背景；避免只按西方风格史串联全部艺术。\n- [教育部书法教育指导纲要](https://www.moe.gov.cn/srcsite/A26/s8001/201301/t20130125_147389.html)：书体与碑帖欣赏的学习参照。\n\n## 教学方法来源\n\n- 使用find-skills流程查找，skills.sh排行榜发现[Matt Pocock teach](https://skills.sh/mattpocock/skills/teach)，读取[原始SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)及格式文件；快照位于`_research/teach/`。查询时排行榜显示896.3K安装，GitHub API显示仓库308462星（2026-11-01查询结果，数量会变化；不把热度视为教学质量保证）。\n- 采用任务导向、小课、即时自检、检索练习、间隔复习和独立参考卡。按用户指定将课程放在各门类文件夹，而非根目录统一lessons。目标已由用户说明，无需再次访谈。\n- [Getty教材设计指南](https://www.getty.edu/education/teachers/building_lessons/)：视觉分析与活动设计入口。\n\n## Wisdom (Communities)\n\n优先在本地公共博物馆的官方教育活动、图书馆读书会或正规剧院导赏中，与讲解员和其他观众讨论一份自己的观察记录。未查询用户城市，不编造具体活动或开放时间；参与是可选的。\n\n## Gaps与使用边界\n\n本次查读了机构页面及检索摘要；并非每条外链都包含本课程全部论点。V&A收藏总入口是延伸检索，不充当文学叙事理论或游戏机制的逐条证据。文学、戏曲、游戏与民间艺术目前侧重原创观察练习，后续深入应补具体原作版本、社群自述与专题资料。音乐、舞蹈及电影分别有机构课程或分析问题表；不把视觉形式分析直接当作所有艺术的通用权威。所有模拟仅解释关系，不复刻真实历史作品。\n'
    write('RESOURCES.md',resources)
    print('Generated 14 units / 42 lessons; entry:',ROOT/'index.html')

if __name__=='__main__':
    raise SystemExit('build_course.py 是数据与入门阶段模板库，单独运行只会生成不完整的中间状态。请运行 python extend_course.py 重建完整教材。')
