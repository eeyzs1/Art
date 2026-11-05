"""运行 python extend_course.py 重建基础教材并扩展完整阶段路线。"""
from pathlib import Path
import json
import build_course as base
from course_extension_data import TAXONOMY, CONTENT, LEVELS
from knowledge_data import GLOSSARY, TIMELINE, MASTER_STARTS
from microlesson_data import MICRO

# 数据完整性：微课必须与分类分组一一对应，缺漏即刻报错。
_tax_groups={(d[0],g) for d in base.DATA for g in TAXONOMY[d[0]]}
assert set(MICRO)==_tax_groups,('micro-lessons must cover every taxonomy group exactly',set(MICRO)^_tax_groups)

R=Path(__file__).resolve().parent
write, esc, page=base.write,base.esc,base.page

# build_course 不再在导入时写盘：显式重建入门阶段与共享资源，作为扩展的第一步。
base.build_base()

NEW_SOURCES={
'00':('Met：艺术史研究文章','https://www.metmuseum.org/essays/timeline-of-art-history','选择与研究对象相关的署名文章，核对对象、地区与材料；本课的方法练习为原创编排。'),
'01':base.SOURCES['visual'],
'02':base.SOURCES['line'],
'03':base.SOURCES['space'],
'04':('MIT OCW：建筑课程入口','https://ocw.mit.edu/search/?d=Architecture','按问题寻找图纸阅读、设计或历史课程。本页只提供学习方案，不能作为施工文件。'),
'05':base.SOURCES['space'],
'06':('V&A：摄影馆藏','https://www.vam.ac.uk/collections/photographs','选择一组有机构记录的对象，核对作者、年代与图像说明；实践以自己的照片为主。'),
'07':('Purdue大学：文学写作与细读资源','https://owl.purdue.edu/owl/subject_specific_writing/writing_in_literature/index.html','进入诗歌细读、小说分析等专题；本课程不复制其正文，练习与例子为原创。'),
'08':('耶鲁公开课程：Listening to Music','https://online.yale.edu/courses/listening-music','作为分层聆听与曲式学习的系统延伸；该课主要讨论西方音乐，不能代表全部音乐传统。'),
'09':base.SOURCES['motion'],
'10':('V&A：戏剧与表演','https://www.vam.ac.uk/collections/theatre-performance','查看表演、舞台设计与档案；戏曲专门技法需另查相应剧种的实践者资料。'),
'11':base.SOURCES['sequence'],
'12':('V&A：游戏展览设计讨论','https://www.vam.ac.uk/articles/about-videogames-exhibition','从机构策展视角观察游戏设计与参与问题；系统练习并非该机构作业。'),
'13':('UNESCO：非遗领域','https://ich.unesco.org/en/intangible-heritage-domains-00052','理解生活实践可横跨多种领域；非遗不等同全部艺术，也不是只由可收藏物件组成。')}

PROTOCOLS={
1:('基础', '45–90分钟，允许分两次完成',[
'准备：从已有材料开始，写清今天只改变的一个变量和保持不变的条件；先完成一次不看提示的尝试。',
'比较：按作业要求保留两种以上结果，逐项记录差异。不要只保留最好的一份，否则无法判断变化原因。',
'核对：将观察与本课概念对照；在资料入口中找一个原作或示范，指出你的模型与原作经验的区别。',
'重做：选择一个具体偏差再做一次；一周后换对象重做，检验方法能否迁移。']),
2:('进阶','2–4小时，建议分两至三次完成',[
'定义问题：用一句话提出可被材料检验的问题，并列出已有判断及可能推翻它的证据。',
'建立对照：完成作业要求的不同版本；记录材料、条件、来源及每次选择，不用最后结果覆盖失败过程。',
'听取反馈：让一位读者或观众先描述实际体验，再透露你的意图。把描述原话与自己的解释分开记。',
'修订论证：回应一条与你原先看法不同的反馈；修改作品或分析，保留未解决的问题。']),
3:('高级','1–3周，按项目规模调整',[
'写项目书：明确对象、核心问题、成果形态、可用材料、时间和三个验收标准。缩小到能完成的范围。',
'做最小样本：先试做一段、一个小稿或一个原型。验证核心关系是否成立，再扩大体量。',
'组织评议：邀请实际读者、使用者或观众，记录任务、体验与疑问。不要引导他们说出你期待的答案。',
'完成与复盘：根据证据选择保留、删除与重做；提交成果、过程档案及下一轮的问题。']),
4:('独立创作与研究／大师研读','至少一个完整项目周期；通常需数周至数月',[
'定向研读：选有可靠出处的成熟作品与不同立场的对照材料，先直接分析，再阅读现成评论。注明版本和观看条件。',
'提取选择：写明作品的一项方法、两条证据、它牺牲或省略了什么，以及该方法在你的题材里可能失效的原因。',
'独立完成：先写个人项目的问题，再创作或研究；借鉴须标注。保存至少两轮实质修改，不把换封面算成一次修订。',
'公开于适当范围评议：自主邀请熟悉该领域的人反馈，回应最强异议并说明仍欠缺的经验；教材不会代你联系或发布。'])}

def level(n):return 1 if n<=5 else 2 if n<=7 else 3 if n==8 else 4

RUBRIC='''<table><tr><th>维度</th><th>需要重做</th><th>可以继续</th></tr><tr><td>问题与概念</td><td>只有宽泛主题或术语</td><td>能提出具体问题，并用概念解释细节</td></tr><tr><td>材料与证据</td><td>结论没有可定位的依据</td><td>至少三条可定位证据，来源与推断分开</td></tr><tr><td>实践与比较</td><td>只有最终成品，没有对照</td><td>保留版本，能解释选择和变化</td></tr><tr><td>反馈与修订</td><td>只收集称赞或回避反例</td><td>回应一条具体异议，说明如何修订</td></tr></table><p>四项均达到“可以继续”才建议进入下一阶段；这是一份学习检查表，不是专业资质或大师认证。无法找到评议者时，先做匿名化版本自查，并把外部反馈保留为未完成项。</p>'''

EXT_CSS='''\nfieldset{border:1px solid #c7ccbf;padding:20px;margin:15px 0}legend{padding:0 8px}input[type=checkbox]{width:20px;height:20px;vertical-align:middle}.search{width:100%;padding:14px;font:inherit;border:1px solid #8b9f94;background:#fff}.badge{font-size:13px;padding:3px 8px;background:#e7eadf;display:inline-block}.wide{overflow-x:auto}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.color-sample{padding:35px;display:flex;justify-content:center;align-items:center}.color-chip{width:65px;height:65px;background:#888}.runner{width:40px;height:40px;background:#b05e3f;border-radius:50%;position:relative}.track{padding:12px;border-bottom:1px solid #bbb;overflow:hidden;margin:12px 0}.live-text{padding:20px;border:1px solid #bbb;white-space:pre-wrap;background:#fff}.note-status{font-size:14px}table{table-layout:fixed;overflow-wrap:anywhere}td,th{vertical-align:top}summary{overflow-wrap:anywhere}@media(max-width:600px){.pair{grid-template-columns:1fr}}.checklist{list-style:none;padding:0;margin:0}.checklist li{border-bottom:1px solid #e3ddcf;padding:12px 0}.checklist label{display:flex;gap:12px;align-items:flex-start;margin:0}.checklist small{display:block;margin-top:4px}'''
write('assets/style.css',(R/'assets/style.css').read_text(encoding='utf-8')+EXT_CSS)
EXT_JS='''\nconst filter=document.querySelector('#taxonomy-filter');if(filter){filter.oninput=()=>{let q=filter.value.trim().toLowerCase(),count=0;document.querySelectorAll('[data-entry]').forEach(e=>{let visible=e.textContent.toLowerCase().includes(q);e.hidden=!visible;if(visible)count++});document.querySelector('#filter-count').textContent='符合条件：'+count+'个条目';};}document.querySelectorAll('[data-plan]').forEach(x=>{try{x.checked=localStorage.getItem('art-plan:'+x.dataset.plan)==='1'}catch{}x.onchange=()=>{try{localStorage.setItem('art-plan:'+x.dataset.plan,x.checked?'1':'0')}catch{}}});let bg=document.querySelector('#contrast');if(bg){bg.oninput=()=>{let v=+bg.value;document.querySelectorAll('.color-sample')[1].style.background='rgb('+v+','+v+','+v+')';document.querySelector('#contrast-result').textContent='右侧背景灰阶为 '+v+'；两块中心灰始终相同。请描述感知差异，而非修改事实。'};}let edit=document.querySelector('#rewrite');if(edit){edit.oninput=()=>{document.querySelector('#rewrite-result').textContent=edit.value||'请写一句话，并用换行制造停顿。';};}let animate=document.querySelector('#animate-time');if(animate){animate.onclick=()=>{let reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;document.querySelectorAll('.runner').forEach((r,i)=>{if(reduced){document.querySelector('#animation-result').textContent='你已选择减少动态效果：匀速在等时距内移动等距离；缓入缓出会先慢后快再慢。';return}let w=r.parentElement.clientWidth-70;r.animate([{transform:'translateX(0)'},{transform:'translateX('+w+'px)'}],{duration:1800,easing:i?'ease-in-out':'linear',iterations:1,fill:'none'})});};}let gen=document.querySelector('#generate');if(gen){function draw(){let seed=+document.querySelector('#seed').value>>>0,root=document.querySelector('#generated');root.replaceChildren();for(let i=0;i<12;i++){seed=(1664525*seed+1013904223)>>>0;let x=20+seed%540;seed=(1664525*seed+1013904223)>>>0;let y=20+seed%130;seed=(1664525*seed+1013904223)>>>0;let line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',x);line.setAttribute('y1',y);line.setAttribute('x2',x+(seed%61)-30);line.setAttribute('y2',y+25);line.setAttribute('stroke',i%2?'#b05e3f':'#25564c');line.setAttribute('stroke-width','4');root.append(line)}document.querySelector('#generate-result').textContent='固定种子与规则可重现本示例。伪随机只是组织结果的一种工具。'}gen.onclick=draw;draw();}let prog=document.querySelector('#checklist-progress');if(prog){let boxes=[...document.querySelectorAll('input[data-plan^="chk-"]')];function upd(){let n=boxes.filter(b=>b.checked).length;prog.textContent='已能复述并举例：'+n+' / '+boxes.length+' 课';}boxes.forEach(b=>b.addEventListener('change',upd));upd();}'''
write('assets/advanced.js',EXT_JS)

def enhanced_page(title,body,depth=0,sub='STUDY / PRACTICE',nav=''):
    doc=page(title,body,depth,sub,nav)
    return doc.replace('</head>',f'<script defer src="{"../"*depth}assets/advanced.js"></script></head>')

def anchor(word,url):
    """有链接则输出外链，无链接输出纯文本（时间线中个别机构不提供稳定直链）。"""
    return f'<a href="{url}" target="_blank" rel="noopener">{esc(word)}</a>' if url else esc(word)

def extra_lab(num,n):
    if n!=4:return ''
    if num in ('01','05','06'):
        return '''<section><h2>屏幕实验：同一块灰</h2><div class="pair"><div class="color-sample" style="background:#eee"><div class="color-chip"></div></div><div class="color-sample" style="background:#222"><div class="color-chip"></div></div></div><label>右侧背景明度<input id="contrast" type="range" min="0" max="255" value="34"></label><output id="contrast-result" aria-live="polite">中心两块灰的数值相同；背景不同可能改变观看感受。</output><p>先预测哪块显得更亮，再调整背景。这里演示邻接关系，不模拟颜料、曝光或真实材料。</p></section>'''
    if num in ('08','09','11'):
        return '''<section><h2>时间实验：相同起点与终点</h2><p>上方匀速，下方缓入缓出；时长和位移相同。点击后描述中途的不同，不把动画直接等同真实身体或乐句。</p><div class="track"><div class="runner" aria-label="匀速示意"></div></div><div class="track"><div class="runner" aria-label="缓入缓出示意"></div></div><button id="animate-time">播放一次对照</button><output id="animation-result" aria-live="polite">支持系统的减少动态效果偏好。</output></section>'''
    if num in ('07','10'):
        return '''<section><h2>语言实验：换行与停顿</h2><p>保持原有词句，只通过换行改变分组，再朗读两种版本。屏幕不自动判分，请听自己的录音。</p><label>输入短句<textarea id="rewrite" data-note="rewrite">你终于来了。\n我以为今天不会再有人敲门。</textarea></label><div id="rewrite-result" class="live-text" aria-live="polite">你终于来了。\n我以为今天不会再有人敲门。</div></section>'''
    if num=='12':
        return '''<section><h2>生成实验：规则与种子</h2><p>固定12条线，改变种子查看不同结果，再回到同一数字比较是否可重现。下方不调用AI或联网。</p><label>整数种子<input id="seed" type="number" min="0" max="999999" value="42"></label><button id="generate">按种子生成</button><svg viewBox="0 0 600 200" role="img" aria-label="由固定规则生成的线条构图"><g id="generated"></g></svg><output id="generate-result" aria-live="polite"></output><p>思考：如果只展示其中一张，观众会遗漏哪些系统信息？</p></section>'''
    return ''

outline=[];coverage=[];all_lessons=[];checklist=[]
for num,name,subs,goal,kind,original in base.DATA:
    folder=f'{num}-{name}';rows=[]
    for line in CONTENT[num].strip().splitlines():
        fields=line.split('｜');assert len(fields)==5,(num,fields)
        rows.append(fields)
    assert len(rows)==6,num
    local_list=[]
    for n,(title,concept,example,task,criterion) in enumerate(rows,4):
        lev=level(n);stage,duration,steps=PROTOCOLS[lev];source=NEW_SOURCES[num]
        nav=f'<a href="../index.html">{name}目录</a><a href="{n-1:02}.html">上一课</a>'
        nav+=f'<a href="{n+1:02}.html">下一课</a>' if n<9 else '<a href="../../reference/roadmap.html">阶段路线</a>'
        body=f'''<p class="lead">{stage} · 第{n}课 / 共9课<br>{duration}。先修：本门类前一课；基础概念不清楚时返回01–03课。</p><section><h2>本课要解决的问题</h2><p>{concept}</p><p>目标：完成“{title}”的具体练习，并能说明一种方法何时有用、何时不足。先用自己的话写一个预测，再开始操作或分析。</p></section><section><h2>示例：选择会产生什么后果</h2><p>{example}</p><p>以上是原创教学情境，不是历史事实引述。请分开记录三个层次：材料中实际出现了什么；你由此作出什么解释；还需要哪些资料才能进一步判断。</p></section>{extra_lab(num,n)}<section><h2>按步骤完成</h2><ol>{''.join('<li>'+s+'</li>' for s in steps)}</ol><h3>本课具体作业</h3><p>{task}</p><label>记录：问题、条件、观察和选择<textarea data-note="project" placeholder="我的问题与预测：\n保持不变的条件：\n观察到的差异：\n我如何选择：\n尚缺的证据："></textarea></label></section><section><h2>反馈：先完成，再展开</h2><details><summary>本课最关键的验收点</summary><p>{criterion}</p><p>若未达到，先缩小作业规模，再补一组对照。若已达到，换一件对象重复方法；结果不同不必视为错误，先检查背景与条件。</p></details><details><summary>常见误区与纠正</summary><p>误区一：只复述术语，未说明它如何对应作品。纠正：给每个术语配一条可定位的证据。</p><p>误区二：用作者意图覆盖实际效果。纠正：先记录观看或测试发生了什么，再解释差距。</p><p>误区三：一次成功就认为掌握。纠正：隔一周换对象再做，并保留失败结果。</p></details>{RUBRIC}</section><section><h2>提交一份可评议的档案</h2><ol><li>作品或分析的原稿、修订稿，附版本日期。</li><li>材料来源、原作名称与版本；无数据的地方写未知。</li><li>一条最有力的反对意见，以及你的回应。</li><li>下一次要检验的具体问题。</li></ol><label>反馈与修订<textarea data-note="revision" placeholder="对方的原话：\n我的判断：\n修改前后：\n我保留的分歧："></textarea></label><label><input type="checkbox" data-plan="{num}-{n}">我已完成作业，并按验收点复核（浏览器尽力保存）</label></section><section><h2>原作与进一步阅读</h2><p><a href="{source[1]}" target="_blank" rel="noopener">{source[0]}</a>：{source[2]}</p><p>资源入口支持查找原作和方法，不代表该页面为本课每个原创例子提供逐条背书。若资源是英文，可先看对象、图纸、时间线与机构说明，再逐段阅读。任何译文都应标明工具或译者。</p></section><section><h2>复习与讨论</h2><p>第二天闭卷复述一个方法和一个限制；第七天换对象再试。将课名、你的作业和最不确定的判断发给老师，可以继续获得逐项反馈。自检不会替代开放题的人工评议。</p></section><nav>{nav}</nav>'''
        if n==9:
            m=MASTER_STARTS[num]
            body+=f'<section><h2>本门研读起点（可替换）</h2><p>主对象：<b>{esc(m[0])}</b>（{esc(m[1])}）。入口：{esc(m[2])}。</p><p>对照对象：<b>{esc(m[3])}</b>（{esc(m[4])}）。研读问题：{esc(m[5])}</p><p>起点只是建议而非唯一选择；替换对象时，保持本课的证据、版本与反馈要求。<a href="../../reference/timeline.html">锚点时间线</a>提供更多候选。</p></section>'
        path=f'{folder}/lessons/{n:02}.html'
        write(path,enhanced_page(title,body,2,f'{stage} / {num}.{n:02}',nav))
        all_lessons.append({'id':f'{num}.{n:02}','title':title,'stage':stage,'path':path})
        local_list.append(f'<li><span class="badge">{stage}</span> <a href="lessons/{n:02}.html">{n:02} · {title}</a></li>')
    # 入门课03的导航已由 build_course 直接链接到04课，无需再对生成文件做字符串补丁。
    entries=[];micro_links=[]
    for group,terms in TAXONOMY[num].items():
        micro_path=f'{folder}/micro/{group}.html'
        m=MICRO[(num,group)]
        hooks=''.join(f'<li><b>{esc(t)}</b>：{esc(p)}</li>' for t,p in m[2])
        mbody=f'''<p class="lead">分组微课 · 约15分钟 · {group}<br>目标：把这组词条变成三条可用的观察要点和一次练习。</p><section><h2>01 · 为什么有这组词条</h2><p>{m[1]}</p><p class="muted">本课属于<a href="../index.html">{name}</a>的扩展层；方法基础见该门类01–03课。</p></section><section><h2>02 · 三个观察要点</h2><ul>{hooks}</ul><p class="muted">术语定义见<a href="../../reference/glossary.html">核心术语表</a>；真实作品入口见<a href="../../reference/timeline.html">锚点时间线</a>。</p></section><section><h2>03 · 做一次练习</h2><p>{m[3]}</p><label>记录你的观察<textarea data-note="micro" placeholder="我的答案、证据与未知……"></textarea></label></section><section><h2>04 · 验收</h2><details><summary>完成后展开：检查思路</summary><p>{m[4]}</p></details></section><section data-quiz data-feedback="{esc(m[8])}"><h2>05 · 快速自检</h2><p>{m[5]}</p><button type="button" data-correct="true">{esc(m[6])}</button><button type="button" data-correct="false">{esc(m[7])}</button><p class="feedback" aria-live="polite"></p></section><nav><a href="../index.html">{name}目录</a><a href="../../reference/coverage.html">覆盖表</a></nav>'''
        write(micro_path,enhanced_page(m[0],mbody,2,f'MICRO / {num} · {group}'))
        micro_links.append(f'<li><a href="micro/{group}.html">{esc(m[0])}</a>（{group}，约15分钟）</li>')
        items=terms.split('、')
        for term in items:coverage.append({'category':name,'group':group,'term':term,'shared_course':f'{folder}/index.html','dedicated_course':False,'group_microlesson':micro_path})
        entries.append('<h3>'+group+'</h3><p>'+terms+'</p>')
    original_links=''.join(f'<li><span class="badge">入门</span> <a href="lessons/{i:02}.html">{i:02} · {l[0]}</a></li>' for i,l in enumerate(original,1))
    body=f'''<p class="lead">{goal}。9课覆盖五个阶段：先入门，再做控制练习、专题项目与大师研读。每次升阶以成果和反馈判断，不按点击次数判断。</p><section><h2>五阶段课程</h2><ol>{original_links}{''.join(local_list)}</ol><p><a href="../reference/roadmap.html">每阶段的要求与长期学习办法</a> · <a href="../reference/coverage.html">子分支覆盖状态</a></p></section><section><h2>分组微课</h2><p>每个分类分组配一节约15分钟的微课，把词条接到具体方法与作品上；笔记保存在本页。</p><ul>{''.join(micro_links)}</ul></section><section><h2>本门类的分类索引</h2>{''.join(entries)}<p>这些条目分别来自媒介、形式、用途与研究维度，允许交叉。它们共享上述9课的方法训练，并有分组微课作为入口；目前没有为每一个条目分别写出专业全课程。</p></section><section><h2>如何选择自己的方向</h2><p>完成05课后，在索引选一个对象明确的子分支，把06–09课作业集中到同一方向。每轮应保留原作分析、个人尝试、外部反馈与实质修订。涉及专门身体技法、材料工艺或工程实现时，需相应条件和现场指导，本文侧重艺术通识、分析、低成本创作与研究。</p></section>'''
    write(f'{folder}/index.html',enhanced_page(name,body,1,'FIVE STAGES / NINE LESSONS'))
    outline.append(f'<article class="card"><p class="eyebrow">{num} / 9 LESSONS</p><h2><a href="{folder}/index.html">{name}</a></h2><p>{goal}</p><small>{subs}</small></article>')
    # 核心概念清单：01–03课取概念段首句，04–09课取人工编写的验收点。
    cl_items=[(i,l[0],l[1].split('。')[0]+'。','入门') for i,l in enumerate(original,1)]
    cl_items+=[(n,row[0],row[4],PROTOCOLS[level(n)][0]) for n,row in zip(range(4,10),rows)]
    checklist.append((num,name,cl_items))

count=len(coverage)
rows=''.join(f'<tr><td>{name}</td><td>{group}</td><td>{term}</td><td><a href="../{shared}">门类共同课</a><br><a href="../{micro}">分组微课</a><br>尚无独立专业全课程</td></tr>' for name,group,term,shared,micro in [(v['category'],v['group'],v['term'],v['shared_course'],v['group_microlesson']) for v in coverage])
write('reference/coverage.html',enhanced_page('分类与教材覆盖表',f'''<p class="lead">已编写14个单元、126课与{len(MICRO)}节分组微课；下表登记{count}个分类条目。条目数量不等于独立艺术门类数量，也不等于专业课程数量。</p><section><h2>如何读表</h2><p>“门类共同课”表示该条目可使用所属门类的基础方法与项目课；“分组微课”是该条目所属分组的15分钟专门课件；“尚无独立专业全课程”表示没有专讲其全部历史、技法、作品与专业训练的教材。此表不把索引自动算成课程完成。</p><p><a href="taxonomy.html">先了解分类维度与边界</a></p><label>按条目、分组或门类搜索<input id="taxonomy-filter" class="search" type="search" placeholder="例如：陶瓷、曲艺、保护、动画"></label><output id="filter-count" aria-live="polite">登记条目：{count}</output></section><div class="wide"><table><tr><th>门类</th><th>分组</th><th>条目</th><th>覆盖状态</th></tr>{rows.replace('<tr><td>','<tr data-entry><td>')}</table></div>''',1))

cl_sections=[]
for num,name,items in checklist:
    lis=''.join(f'<li><label><input type="checkbox" data-plan="chk-{num}-{n:02}"><span><span class="badge">{stage}</span> <b>{n:02} · {esc(title)}</b><br><small>{esc(tip)}</small></span></label></li>' for n,title,tip,stage in items)
    cl_sections.append(f'<section><h2>{num} · <a href="../{num}-{name}/index.html">{name}</a></h2><ul class="checklist">{lis}</ul></section>')
write('reference/checklist.html',enhanced_page('核心概念自检清单',f'''<p class="lead">126课的核心概念与验收点一览，按门类和五阶段排列。勾选规则比清单本身重要。</p><section><h2>怎么用这份清单</h2><ol><li>学完一课，先关掉页面复述概念，再回来勾选；每条小字是该课的关键句或验收点，是复述的最低线索。</li><li>第二天复述失败就取消勾选；第七天换一件新作品再验证一次。</li><li>09课在完成一轮完整项目、收到反馈并做出修订之后才勾选。</li><li>进度保存在当前浏览器，清理缓存会丢失；真正的掌握证据是你的作品与笔记，不是勾选本身。</li></ol><output id="checklist-progress" aria-live="polite">加载中…</output><p><a href="roadmap.html">五阶段路线</a> · <a href="glossary.html">核心术语表</a> · <a href="timeline.html">锚点时间线</a> · <a href="method.html">欣赏方法卡</a></p></section>{''.join(cl_sections)}<section><h2>勾完之后</h2><p>全部门类01–03课勾完后，做一次跨门类比较：两个门类如何处理同一个问题（节奏、空间或叙事）。任何一门勾到09课后，回到<a href="../index.html">首页</a>选择下一个小分支，或进入专长路线的长期项目。</p></section>''',1))

gl_terms=0;gl_sections=[]
for num,name,*_ in base.DATA:
    cards=''.join(f'<article class="card" data-entry><b>{esc(t)}</b><p>{esc(d)}</p><p><small><a href="../{num}-{name}/index.html">所属门类：{name}</a></small></p></article>' for t,d in GLOSSARY[num])
    gl_terms+=len(GLOSSARY[num]);gl_sections.append(f'<section><h2>{num} · <a href="../{num}-{name}/index.html">{name}</a></h2><div class="grid">{cards}</div></section>')
write('reference/glossary.html',enhanced_page('核心术语表',f'''<p class="lead">{gl_terms}个基础术语的一句话定义，作为阅读与复习的检索层；定义由本教材编写，供入门使用，不是学科定论。</p><section><h2>怎么用</h2><p>遇到课文中未展开的词先来这里查；每条定义只给最低限度的含义与一个观察线索，深入学习请回到对应门类课程与外部馆藏。</p><label>搜索术语或定义<input id="taxonomy-filter" class="search" type="search" placeholder="例如：皴法、行当、蒙太奇、陶瓷"></label><output id="filter-count" aria-live="polite">收录术语：{gl_terms}</output><p><a href="timeline.html">配套：锚点时间线</a> · <a href="checklist.html">核心概念自检清单</a></p></section>{''.join(gl_sections)}''',1))

tl_rows=0;tl_sections=[]
for num,name,*_ in base.DATA:
    rows=''.join(f'<tr><td>{esc(p)}</td><td><b>{anchor(w,u)}</b><br><small>{esc(h)}</small></td><td>{esc(why)}</td></tr>' for p,w,h,u,why in TIMELINE[num])
    tl_rows+=len(TIMELINE[num]);tl_sections.append(f'<section><h2>{num} · <a href="../{num}-{name}/index.html">{name}</a></h2><div class="wide"><table><tr><th>时期</th><th>作品与创作者</th><th>为何值得看</th></tr>{rows}</table></div></section>')
write('reference/timeline.html',enhanced_page('锚点时间线',f'''<p class="lead">{tl_rows}件真实作品的入口，中外并置；它们不是“最伟大作品”清单，而是把方法课接到真实材料上的起点。</p><section><h2>怎么用时间线</h2><ol><li>每个门类选一两件，先看图、听音频或读文本，再用方法课的观察框架记录三条证据。</li><li>注意同时性：同世纪的不同地区可能在解决完全不同的问题，不能按“谁更先进”排列。</li><li>馆藏链接指向机构官网或公版档案的入口页；作品信息以馆藏页为准，若与本页不一致，以馆藏为准并记录差异。</li><li>本页不是完整的艺术史叙事；系统学习历史请搭配一部中外艺术通史。</li></ol><p><a href="glossary.html">配套：核心术语表</a> · <a href="roadmap.html">五阶段路线</a> · <a href="checklist.html">核心概念自检清单</a></p></section>{''.join(tl_sections)}''',1))

tax_sections=[]
for num,name,*_ in base.DATA:
    groups=''.join(f'<h3>{esc(g)}</h3><p>{esc(t)}</p>' for g,t in TAXONOMY[num].items())
    tax_sections.append(f'<section><h2>{num} · <a href="../{num}-{name}/index.html">{name}</a></h2>{groups}</section>')
TAX_INTRO='''<section><h2>先回答：上一版列全了吗？</h2><p>没有。上一版覆盖了主要创作领域，却遗漏许多子分支，也把部分不同维度混在一起。本版扩大索引并明确边界，仍不声称穷尽全球所有地方传统、新媒介实践及其名称。</p><p>分类是为提问与检索服务的工具。按媒介、功能、地区、历史与研究对象，会得到不同且重叠的目录；不存在一棵既互斥又能穷尽全部艺术的固定树。</p></section><section><h2>六个维度不要混用</h2><table><tr><th>维度</th><th>例子与作用</th></tr><tr><td>媒介／形式</td><td>绘画、声音、身体、空间、计算；回答用什么组织经验。</td></tr><tr><td>题材／体裁／用途</td><td>肖像、史诗、喜剧、礼仪、广告；这些概念本身也有不同层次，需结合领域解释。</td></tr><tr><td>地区／社群传统</td><td>中国不同地区、欧洲、南亚、东南亚、西亚与北非、撒哈拉以南非洲、美洲、大洋洲及迁徙社群；每一项内部仍有大量差异。</td></tr><tr><td>历史／风格</td><td>特定时期与运动的名称应放回本地历史，不能把欧洲分期覆盖全球。</td></tr><tr><td>生产／传播</td><td>宫廷、宗教、社区、市场、公共机构、网络平台；同一作品可经历多种制度。</td></tr><tr><td>理论／专业分工</td><td>美学、史论、批评、教育、策展、保护、管理；研究领域与创作媒介不属于同一维度。</td></tr></table></section><section><h2>与官方目录的关系</h2><p>作为一种制度参照，教育部2022年研究生目录及其解读将艺术专业学位分为音乐、舞蹈、戏剧与影视、戏曲与曲艺、美术与书法、设计六类，并设置艺术学研究。该目录服务学位管理，不是全部人类艺术的分类。本教材采用广义人文视角，因此也纳入文学、建筑与景观等相关创作领域。</p><p>依据：<a href="https://www.moe.gov.cn/srcsite/A22/moe_833/202209/t20220914_660828.html">2022目录通知</a>、<a href="https://www.moe.gov.cn/fbh/live/2023/55658/dxjy/202312/t20231219_1095135.html">艺术教指委解读</a>。此处仅介绍该版本，不声称其等于截至今日所有动态调整的最新全集。</p><p>UNESCO非遗框架关注口述表达、表演、社会实践等相互交叉的领域，含许多艺术实践，也包含并非以艺术为主要性质的知识与活动；因此不能拿非遗名录代替艺术目录。见<a href="https://ich.unesco.org/en/intangible-heritage-domains-00052">官方领域说明</a>。</p></section>'''
write('reference/taxonomy.html',enhanced_page('艺术分类扩展索引',TAX_INTRO+''.join(tax_sections)+'''<section><h2>还有哪些边界领域？</h2><p>烹饪与食物、香与嗅觉、茶与花、身体装饰、园艺、仪式、电子游戏和生物媒介等，可以在特定语境中成为艺术实践，但并非所有相关活动自动都属于艺术。判断时记录具体实践、社群自述、呈现语境和提出的问题，不把生活行业一概算作新的主门类。</p><p>同一对象可有多重标签。例如皮影可同时归入造型、表演、声音、叙事与民间实践。它在本教材的主要入口是13，关联10、08、07与03。</p><p><a href="coverage.html">查看每个条目的教材覆盖状态 →</a></p></section>''',1))

level_table=''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in LEVELS)
write('reference/roadmap.html',enhanced_page('从入门走向独立创作与研究',f'''<p class="lead">五阶段路线已经配有正文、作业与反馈标准。“大师研读”指研究成熟作品的方法与长期独立实践，不是阅读后的身份授予。</p><section><h2>每门9课，五个阶段</h2><table><tr><th>阶段</th><th>课号</th><th>可观察的学习成果</th></tr>{level_table}</table><p>先修依次衔接。有经验者可以提交相应阶段成果自查，补足缺项后跳级；完全陌生的领域仍建议从01课开始。</p></section><section><h2>两条学习路线</h2><h3>人文素养路线</h3><p>先完成14门的01–03课建立全景，再选三门学至07课；高级阶段可选择作品分析、比较研究或策展项目，而非要求每门都成为职业创作者。</p><h3>专长路线</h3><p>选一个子分支，将04–09课集中于同一主题反复做项目。每完成一轮，再补该领域的历史、专业技法与原作阅读；与有经验的实践者建立定期反馈。教材不替代专业工作室、音乐或身体技术训练。</p></section><section><h2>为什么课表不等于大师训练完成？</h2><p>高级能力需要跨题材迁移、长期反复修订、同伴和导师批评，以及真实观看与使用经验。读完文字、答对选择题、按提示模仿，都不能单独证明独立判断能力。</p><p>每轮项目应交付四项：可评议的成果、可追溯的过程、最强异议及回应、下一轮要检验的问题。至少两轮在不同对象上成立后，再扩大范围。</p></section><section><h2>年度工作室：重复而不重复自己</h2><ol><li>第一轮：限制媒介和规模，完成一个小项目，找出最弱的能力。</li><li>第二轮：围绕该弱点补基础练习，再做不同对象的新项目。</li><li>第三轮：与不同传统或媒介对照，检验原方法的边界。</li><li>第四轮：整理作品集或研究档案，请熟悉领域的人批评，写出下一年度的问题。</li></ol><p>轮次不对应固定月份，按实际时间和反馈推进；没有证据的熟练不能自动升级为掌握。</p></section><section><h2>项目自评与外部反馈</h2>{RUBRIC}<p><a href="method.html">基础欣赏方法卡</a> · <a href="checklist.html">核心概念自检清单</a> · <a href="glossary.html">核心术语表</a> · <a href="timeline.html">锚点时间线</a> · <a href="coverage.html">课程覆盖边界</a></p><p>方法课需要真实材料支撑：术语表与时间线提供内容层入口；完整艺术史叙事请搭配一部中外通史。</p></section>''',1))

write('index.html',enhanced_page('从作品出发，走向独立判断',f'''<p class="lead">14个门类与基础单元，126节课。从入门观察到专题创作、研究与大师作品研读。每一级都以练习、证据和修订为核心。</p><section><h2>先选择你的入口</h2><nav><a href="00-艺术通识/lessons/01.html">从零开始</a><a href="reference/roadmap.html">五阶段学习路线</a><a href="reference/checklist.html">核心概念自检清单</a><a href="reference/glossary.html">核心术语表</a><a href="reference/timeline.html">锚点时间线</a><a href="reference/taxonomy.html">扩展分类索引</a><a href="reference/coverage.html">教材覆盖表</a></nav><p>分类索引登记{count}个条目，涵盖媒介、形式、材料、专业分工与研究领域，允许交叉。已完成的是门类共同课与{len(MICRO)}节分组微课；每个子分支的独立专业全课程尚未全部编写。</p></section><h2>每门都有完整阶段路线</h2><div class="grid">{''.join(outline)}</div><section><h2>如何开始而不被数量淹没</h2><p>先读通识01–03课，然后任选一门完成01–05课。每次留下具体作品观察、控制练习与修订记录；再决定是否深入06–09课。无需同时修满所有门类。</p><p>课程可离线阅读，互动示例不调用外部服务；机构原作、录音和外部阅读需联网。开放题需要你实际完成，教材不会自动评定艺术质量。</p></section>'''))

manifest={'units':14,'lessons':126,'taxonomy_entries':count,'dedicated_subbranch_courses':0,'group_microlessons':len(MICRO),'glossary_terms':gl_terms,'timeline_anchors':tl_rows,'added_lessons':all_lessons,'coverage':coverage}
write('course-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))

# Rewrite user-facing documentation to describe the final scope, not the previous version.
main_table='\n'.join(f'| {num} | [{name}](./{num}-{name}/index.html) | 01–03入门；04–05基础；06–07进阶；08高级；09独立项目与大师研读 |' for num,name,*_ in base.DATA)
taxonomy_md='\n\n'.join(f'### {num} · {name}\n\n'+'\n'.join(f'- **{group}**：{terms}。' for group,terms in TAXONOMY[num].items()) for num,name,*_ in base.DATA)
write('README.md',f'''# 艺术学习室

以增强艺术人文素养为目标，从观察、聆听与阅读出发，逐步训练比较、背景研究、创作与独立判断。

## 打开教材

双击 [index.html](./index.html)，无需安装依赖。先读[五阶段路线](./reference/roadmap.html)，也可直接进入[通识第一课](./00-艺术通识/lessons/01.html)。

## 对两个问题的准确回答

**上一版没有列出所有分类。** 它只有主要领域地图。现在扩展为14个教学单元和{count}个索引条目，涵盖材料、媒介、文类、专业分工与理论领域；它们彼此交叉，不能当作{count}个互斥门类。没有固定目录可以穷尽全球所有艺术传统和新实践。本页是广泛的学习索引，不是封闭全集或现行官方学科目录。

**已写好从入门到独立创作与研究的门类课程，尚未穷尽每个子分支的专业全教程。** 共126课，每门9课，五阶段均有具体正文、例子、作业与反馈标准；每个分类分组另配一节15分钟微课（共{len(MICRO)}节）。09课为大师作品研读与长期项目，不承诺读完即可成为大师。[覆盖表](./reference/coverage.html)逐项标明：子分支使用门类共同课与分组微课，目前未分别开设独立专业全课程。没有把索引、生成页数或项目模板冒充全部专业知识。

**方法与知识的分工。** 正文以方法训练为主；[核心术语表](./reference/glossary.html)（{gl_terms}个术语的一句话定义）、[锚点时间线](./reference/timeline.html)（{tl_rows}件真实作品的馆藏入口，中外并置）与{len(MICRO)}节分组微课提供内容层入口，09课均配有具体研读起点。它们不构成完整的艺术史叙事；系统学习历史请搭配一部中外艺术通史，并按方法课的要求核对每条陈述。

## 主分支与文件夹

这里采用广义艺术人文教育视角。00为理论基础；01–13为主要创作领域的教学分组。文学、建筑与景观等纳入此广义视角，未声称它们全部属于中国学位目录中的艺术学门类。

| 编号 | 门类与入口 | 课程阶段 |
|---|---|---|
{main_table}

## 分类应有多个维度

媒介与形式、题材和用途、地区与社群、历史与风格、生产传播制度、理论及职业分工是不同维度。同一作品可以落在多个位置，例如皮影同时连接造型、戏剧、声音、叙事与民间实践。地区、历史和风格不能只用欧洲分期代表全球；每种地区传统内部还需继续细分。

制度参照：[教育部2022年研究生目录](https://www.moe.gov.cn/srcsite/A22/moe_833/202209/t20220914_660828.html)及[艺术教指委解读](https://www.moe.gov.cn/fbh/live/2023/55658/dxjy/202312/t20231219_1095135.html)服务学位管理，不是全部人类艺术的唯一分类。[UNESCO非遗领域](https://ich.unesco.org/en/intangible-heritage-domains-00052)关注传承实践，也不能等同全部艺术。详见[分类说明](./reference/taxonomy.html)。

## 主要子分支扩展索引

下列是代表性分组，允许重叠；题材、技法、形式与研究方向不混称为同一级互斥门类。中国地方剧种、各地音乐舞蹈、特定工艺与新生实践未能逐个穷举。

{taxonomy_md}

## 如何学

1. 通识01–03课先建立证据意识；各门01–03课约15–25分钟一课。
2. 04–05课做控制练习，每课约45–90分钟；06–07课做分析与迭代，每课约2–4小时。均为建议，可拆开完成。
3. 08课完成专题，09课做大师研读与独立项目，需数周乃至数月，按成果和反馈推进。
4. 人文素养路线先广泛欣赏，再选三门深学；专长路线选一个子分支反复完成项目，并补对应的系统历史与专业技法。
5. 第二天闭卷复述，第七天换原作重做；每轮项目保存原稿、反馈、修订及未解决的问题。

专业身体技法、乐器训练、材料工艺与工程实现，需要对应条件及现场指导。本教材重点为通识、观察分析、低成本创作和研究方法，不是所有职业资质的训练替代品。

## 文件与重建

- `index.html`：总入口；各门类`index.html`与`lessons/01.html`至`09.html`：导学和课程。
- `reference/`：方法卡、五阶段路线、核心概念自检清单、核心术语表、锚点时间线、分类索引与覆盖表。
- `course-manifest.json`：可核对的课程与分类登记。
- `build_course.py`：入门阶段（01–03课）的数据与模板库，作为模块被调用，不单独生成站点；`course_extension_data.py`：扩展分类与84课的人工编写数据；`knowledge_data.py`：术语表、时间线锚点与09课研读起点的数据；`microlesson_data.py`：33个分类分组的微课数据；`extend_course.py`：完整站点的唯一入口生成器。
- **重建完整版本运行 `python extend_course.py`（会覆盖生成页面，手动改页面前请备份）。** 直接运行 `build_course.py` 会拒绝执行，避免误生成不完整的中间状态。
- `check_course.py`：开发检查脚本，需要Python Playwright；学习时不需要。
- `RESOURCES.md`、`MISSION.md`、`NOTES.md`及`_research/teach/`：来源、目标、偏好与教学skill快照。

正文、原创图形与本地实验可离线使用；外部馆藏需联网。笔记和勾选通过浏览器localStorage尽力保存，file协议和清理缓存可能影响留存；重要内容请另存。页面不会自动评定开放作业，也不会自动证明已掌握。未写入用户尚未完成的学习记录。
''')

resources=(R/'RESOURCES.md').read_text(encoding='utf-8')
resources+='\n\n## 本轮扩展的来源与覆盖边界\n\n'
for num,(title,url,note) in NEW_SOURCES.items():resources+=f'- {num} [{title}]({url})：{note}\n'
resources+='\n- [教育部2022目录通知](https://www.moe.gov.cn/srcsite/A22/moe_833/202209/t20220914_660828.html)与[艺术教指委解读](https://www.moe.gov.cn/fbh/live/2023/55658/dxjy/202312/t20231219_1095135.html)：对照学位目录与广义艺术学习的不同范围，仅陈述此版本。\n- [Met部门与保护研究](https://www.metmuseum.org/departments)：了解保护、材料研究与策展的职业分工。未将本地观察练习视作文物修复技术教程。\n\n## 知识层来源（术语表、时间线与09课研读起点）\n\n- 馆藏与机构入口：[故宫博物院](https://www.dpm.org.cn)、[台北故宫博物院](https://www.npm.gov.tw)、[中国国家博物馆](https://www.chnmuseum.cn)、[敦煌研究院](https://www.dha.ac.cn)、[秦始皇帝陵博物院](http://www.bmy.com.cn)、[大都会艺术博物馆](https://www.metmuseum.org/art/collection)、[MoMA](https://www.moma.org/collection/)、[V&A](https://www.vam.ac.uk/collections)、[乌菲兹美术馆](https://www.uffizi.it)、[荷兰国立博物馆](https://www.rijksmuseum.nl/en/collection)、[卢浮宫](https://www.louvre.fr/en)、[费城艺术博物馆](https://www.philamuseum.org)、[美国国会图书馆](https://www.loc.gov)、[纽约公共图书馆](https://www.nypl.org)、[英国皇家歌剧院](https://www.roh.org.uk)、[BFI](https://www.bfi.org.uk)、[史密森尼Folkways](https://folkways.si.edu)、[包豪斯德绍基金会](https://bauhaus-dessau.de)、[云门舞集](https://www.cloudgate.org.tw)、[玛莎·格雷厄姆舞蹈团](https://marthagraham.org)。\n- 公版与档案：[古腾堡计划](https://www.gutenberg.org)、[中国哲学书电子化计划](https://ctext.org)、[IMSLP](https://imslp.org)、[Internet Archive](https://archive.org)、[Rhizome](https://rhizome.org)、[玛格南图片社](https://www.magnumphotos.com)。\n- 名录制度：[UNESCO非遗名录](https://ich.unesco.org/en/lists)与[世界遗产名录](https://whc.unesco.org/en/list/)。\n\n以上入口页于2026-11-05人工核对可访问；链接指向机构入口页而非深层对象页。作品信息以各馆藏页为准，与本教材不一致时以馆藏为准并记录差异。\n\n本轮课程中的例子、练习、步骤与验收表由本教材原创编排；机构入口用于原作、资料和进一步学习，不声称每条主张均被入口页逐句验证。分类索引是教学用综合整理，并非上述任一机构发布的完整分类。专门子分支课程的缺口列在coverage.html和course-manifest.json中。\n'
write('RESOURCES.md',resources)
notes=(R/'NOTES.md').read_text(encoding='utf-8')+'\n用户追加希望贯通入门到高阶，并询问是否穷尽分类。本轮扩展五阶段门类课程与分类索引；未修改增强艺术人文素养的原始目标。高阶创作可按人文路线替换为作品分析或研究；不推定用户要同时职业精通所有领域。\n'
write('NOTES.md',notes)
print(f'Complete: 14 units, 126 lessons, {count} taxonomy entries. Specialized subbranch courses remain explicitly unfilled.')
