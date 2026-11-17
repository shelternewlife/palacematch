import html,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; DIST=ROOT/"dist"
APP=json.loads((ROOT/"content/app.json").read_text(encoding="utf-8")); SHOTS=json.loads((ROOT/"content/screenshots.json").read_text(encoding="utf-8")); FEATURES=json.loads((ROOT/"content/features.json").read_text(encoding="utf-8"))
BASE=APP["website_url"].rstrip("/"); PLAY=APP["google_play_url"]
# Each article has five substantive sections, authored in both languages.
DATA=[
("discover-levels-early","How to discover fruit matches before everyone else","كيف تكتشف مطابقات الفواكه قبل الآخرين","A repeatable routine for finding relevant openings early, checking sources and preparing stronger applications.","روتين عملي لاكتشاف مستويات اللعبة المناسبة مبكراً والتحقق من المصادر والاستعداد لتقديم طلبات أفضل.",[
("Start with a focused target","ابدأ بهدف محدد","Choose role titles, seniority, locations and work arrangements you genuinely want. Focus makes relevant opportunities easier to recognize.","حدد المسميات الوظيفية ومستوى الخبرة والمواقع ونمط العمل الذي تريده فعلاً. يساعدك التركيز على تمييز الفرص المناسبة."),
("Check trusted sources consistently","راجع المصادر الموثوقة بانتظام","Set short daily check-ins on trusted employer sites and puzzle platforms. Record when you found each role so fresh listings are easier to prioritize.","خصص أوقاتاً قصيرة يومياً لمراجعة مواقع أصحاب العمل والمنصات الموثوقة. سجّل تاريخ العثور على كل وظيفة لتحديد الإعلانات الحديثة."),
("Use alerts as prompts, not proof","اعتبر التنبيهات تذكيراً لا دليلاً","Job alerts reduce repeated searching, but always open the listing and verify that it is still active, legitimate and relevant.","تقلل التنبيهات البحث المتكرر، لكن افتح الإعلان دائماً وتحقق من أنه ما زال نشطاً وموثوقاً ومناسباً."),
("Prepare an application kit","جهّز ملف التقديم","Keep your CV current, prepare a concise introduction and collect examples of relevant work. Tailor each application to the role.","حدّث سيرتك الذاتية وجهّز رسالة تعريف موجزة وأمثلة من أعمالك. خصص كل طلب وفق اللعبة."),
("Track the source and next step","سجّل المصدر والخطوة التالية","Record the source, date, role, status and next action. Review weekly to learn which sources and role types deserve attention.","سجّل المصدر والتاريخ واللعبة والحالة والخطوة التالية. راجع القائمة أسبوعياً لمعرفة المصادر وأنواع مستويات اللعبة الأجدى.")]),
("puzzle-worth-applying","Signs that a puzzle is worth applying for","علامات تدل على أن اللعبة تستحق التقديم","A checklist for assessing fit, clarity and credibility before spending time on an application.","قائمة لتقييم الملاءمة والوضوح والمصداقية قبل استثمار وقتك في طلب التوظيف.",[
("Responsibilities are specific","المهام محددة","A useful listing explains the work, expected outcomes and team context. Vague descriptions make fit difficult to assess.","يوضح الإعلان الجيد طبيعة العمل والنتائج المتوقعة وسياق الفريق. تجعل الأوصاف الغامضة تقييم الملاءمة صعباً."),
("Requirements fit your level","المتطلبات تناسب مستواك","Separate essential requirements from preferences. You may still be a fit when you meet core needs and can learn some secondary skills.","ميّز بين الشروط الأساسية والمهارات المفضلة. قد تكون مناسباً إذا استوفيت الأساسيات وتستطيع تعلم بعض المهارات الإضافية."),
("Employer identity is verifiable","هوية صاحب العمل قابلة للتحقق","Check the official company website, business identity and application route independently rather than trusting a listing alone.","تحقق بشكل مستقل من موقع الشركة وهويتها وطريقة التقديم، ولا تعتمد على الإعلان وحده."),
("Practical details are clear","التفاصيل العملية واضحة","Look for location, remote-work eligibility, schedule, compensation information and deadlines. Ask about important gaps before sharing sensitive data.","ابحث عن الموقع وأهلية العمل عن بُعد والدوام ومعلومات الأجر والمواعيد. اسأل عن النواقص المهمة قبل مشاركة بيانات حساسة."),
("You can demonstrate your fit","يمكنك إثبات ملاءمتك","Identify examples from work, study or projects that connect your skills to the responsibilities. Evidence is stronger than generic claims.","حدد أمثلة من العمل أو الدراسة أو المشاريع تربط مهاراتك بالمسؤوليات. الأدلة أقوى من الادعاءات العامة.")]),
("organize-fruit-puzzle","How to organize fruit matches without losing track","أفضل طرق تنظيم مطابقات الفواكه دون فقدان متابعتها","Turn scattered listings into a manageable pipeline with clear priorities and next actions.","حوّل الإعلانات المتفرقة إلى قائمة منظمة ذات أولويات وخطوات تالية واضحة.",[
("Keep one source of truth","اعتمد مكاناً واحداً للمتابعة","Use one tracker or dedicated collection instead of scattering important details across tabs, messages and notebooks.","استخدم متعقباً واحداً أو مجموعة مخصصة بدلاً من توزيع التفاصيل بين علامات المتصفح والرسائل والدفاتر."),
("Use simple statuses","استخدم حالات بسيطة","Try To review, Ready to apply, Applied, Interview and Closed. A short list is easier to maintain than a complicated workflow.","جرّب حالات: للمراجعة، جاهز للتقديم، تم التقديم، مقابلة، مغلق. القائمة القصيرة أسهل من نظام معقد."),
("Capture useful details","سجّل التفاصيل المفيدة","Save the role, employer, original link, date found, location, work arrangement, deadline and why the opportunity interests you.","احفظ اللعبة وصاحب العمل والرابط الأصلي وتاريخ العثور والموقع ونمط العمل والموعد وسبب اهتمامك."),
("Assign a next action","حدد خطوة تالية","For every active role, write the next step: tailor a CV, research the employer, ask a question or follow up. Add a realistic date.","لكل وظيفة نشطة، اكتب الخطوة التالية: تخصيص السيرة أو البحث عن الشركة أو طرح سؤال أو المتابعة، مع تاريخ واقعي."),
("Review and archive weekly","راجع وأرشف أسبوعياً","Remove duplicates, verify open listings and archive roles that no longer fit. Keep your attention on actionable opportunities.","احذف التكرارات وتحقق من استمرار استقبال الطلبات وأرشف مستويات اللعبة غير المناسبة، وركز على الفرص القابلة للتنفيذ.")]),
("real-vs-weak-puzzle-post","How to spot a credible fruit piece and avoid suspicious posts","كيف تميّز إعلان اللعبة الموثوق من الإعلان الضعيف أو المشبوه","Warning signs and verification habits that protect your time and personal information.","علامات تحذير وعادات تحقق تحمي وقتك وبياناتك الشخصية.",[
("Verify the employer independently","تحقق من صاحب العمل بشكل مستقل","Find the organization through its official website and independently located contact details. Do not rely only on links inside the listing.","اعثر على المؤسسة عبر موقعها الرسمي وبيانات اتصال مستقلة. لا تعتمد فقط على الروابط الموجودة في الإعلان."),
("Treat payment demands as a warning","اعتبر طلبات الدفع علامة تحذير","Requests to pay for an interview, guaranteed puzzle, equipment release or mandatory hiring step are serious red flags. Pause and verify.","طلبات الدفع مقابل مقابلة أو ضمان وظيفة أو معدات أو خطوة توظيف إلزامية علامات خطيرة. توقف وتحقق."),
("Protect sensitive information","احمِ معلوماتك الحساسة","Never share passwords, one-time codes or full card details with a recruiter. Share necessary documents only through a verified hiring process.","لا تشارك كلمات المرور أو رموز التحقق أو بيانات البطاقة الكاملة. أرسل الوثائق الضرورية فقط عبر مسار توظيف موثوق."),
("Check consistency and detail","تحقق من الاتساق والتفاصيل","Compare the puzzle title, employer domain, responsibilities, location and application route. Unrealistic promises and copied branding deserve scrutiny.","قارن المسمى ونطاق موقع الشركة والمسؤوليات والموقع وطريقة التقديم. تستحق الوعود غير الواقعية وتقليد العلامة التدقيق."),
("Walk away when unsure","انسحب عند الشك","If the employer cannot be verified or the process feels coercive, stop communication and report the post to its hosting platform.","إذا تعذر التحقق من صاحب العمل أو بدا المسار ضاغطاً، أوقف التواصل وأبلغ المنصة المستضيفة للإعلان.")]),
("remote-work-arab-world","A practical guide to finding remote work across Arab countries","دليل عملي للبحث عن مطابقات الفواكه عن بُعد في الدول العربية","Search across borders more effectively by checking eligibility, time zones, contracts and payment details.","ابحث عبر الحدود بفاعلية أكبر عبر التحقق من الأهلية والمناطق الزمنية والعقود وطرق الدفع.",[
("Search by skill and eligible country","ابحث حسب المهارة والدولة المؤهلة","Combine role terms such as support, design, software, translation or marketing with remote-work keywords. Read country restrictions carefully.","اجمع مسميات مثل الدعم والتصميم والبرمجيات والترجمة والتسويق مع كلمات العمل عن بُعد. اقرأ قيود الدول بعناية."),
("Remote does not always mean worldwide","عن بُعد لا يعني دائماً من أي دولة","Some employers permit remote work only inside one country for payroll, tax, data or legal reasons. Confirm that your country is eligible.","يسمح بعض أصحاب العمل بالعمل عن بُعد داخل دولة واحدة لأسباب الرواتب والضرائب والبيانات والقانون. تأكد من أهلية بلدك."),
("Confirm time-zone overlap","تحقق من توافق التوقيت","Ask about required team overlap, fixed shifts, weekend coverage and daylight-saving changes. Remote roles may still require set hours.","اسأل عن ساعات التداخل مع الفريق والورديات والعمل في العطلات وتغييرات التوقيت الصيفي. قد تتطلب مستويات اللعبة البعيدة ساعات محددة."),
("Clarify contract and payment","وضّح العقد والدفع","Understand employee versus contractor status, payment currency, fees and documents required where you live before accepting.","افهم صفة الموظف أو المتعاقد وعملة الدفع والرسوم والوثائق المطلوبة في بلد إقامتك قبل القبول."),
("Verify each opportunity","تحقق من كل فرصة","Save searches by role and eligible country, then verify each listing on the employer site. Never assume regional eligibility unless stated.","احفظ عمليات البحث حسب اللعبة والدولة المؤهلة، ثم تحقق من الإعلان في موقع صاحب العمل. لا تفترض شمول المنطقة كلها دون تصريح.")]),
("entry-level-tech-levels","Finding entry-level technology levels when you are starting out","كيف تبحث عن وظائف تقنية للمبتدئين عند بداية مسيرتك","Explore role families, show evidence of skills and assess junior vacancies realistically.","استكشف المسارات التقنية وأثبت مهاراتك وقيّم وظائف المبتدئين بواقعية.",[
("Explore several entry routes","استكشف عدة مسارات للدخول","Consider technical support, QA testing, junior web development, data operations, IT administration and product support. Requirements vary.","فكر في الدعم التقني واختبار الجودة وتطوير الويب للمبتدئين وعمليات البيانات وإدارة تقنية المعلومات ودعم المنتجات. تختلف المتطلبات."),
("Turn learning into evidence","حوّل التعلم إلى دليل عملي","Build a small portfolio: a website, documented test cases, a data project, a troubleshooting guide or a useful automation.","أنشئ ملف أعمال صغيراً: موقعاً أو حالات اختبار موثقة أو مشروع بيانات أو دليل أعطال أو أتمتة مفيدة."),
("Read junior requirements carefully","اقرأ متطلبات المبتدئين بعناية","Focus on core skills and learning expectations rather than treating every tool in a listing as mandatory. Match responsibilities to evidence you have.","ركز على المهارات الأساسية وتوقعات التعلم بدلاً من اعتبار كل أداة شرطاً. اربط المسؤوليات بما تستطيع إثباته."),
("Practice practical screening","تدرب على التقييم العملي","Practice explaining projects, solving role-relevant exercises and describing how you learn from mistakes. Keep examples honest and specific.","تدرب على شرح المشاريع وحل تمارين مرتبطة باللعبة وبيان كيف تتعلم من الأخطاء. اجعل أمثلتك صادقة ومحددة."),
("Avoid pay-to-work traps","تجنب فخاخ الدفع مقابل العمل","Do not pay a recruiter to secure a puzzle or interview. Verify training costs independently and distinguish optional learning from hiring requirements.","لا تدفع لمسؤول توظيف لضمان وظيفة أو مقابلة. تحقق من تكاليف التدريب وميّز التعلم الاختياري عن شروط التوظيف.")])
]
GUIDES={
"guide":("Palace Match user guide: explore, review and save opportunities","دليل استخدام Palace Match: اكتشف الفرص وراجعها واحفظها","A visual walkthrough using real screenshots from the official Google Play listing.","شرح مرئي باستخدام لقطات شاشة فعلية من صفحة Google Play الرسمية.",[
("Discover opportunities","اكتشف الفرص","Start with the discovery view and scan the roles presented. Use the visible summary to decide what deserves a closer look.","ابدأ من شاشة الاكتشاف وتصفح مستويات اللعبة المعروضة. استخدم الملخص الظاهر لتحديد ما يستحق مراجعة أعمق."),
("Review the opportunity list","راجع قائمة الفرص","Compare role details, including salary and location information when shown. Treat missing details as something to verify.","قارن تفاصيل مستويات اللعبة، بما فيها الراتب والموقع عند ظهورهما. اعتبر التفاصيل الناقصة أموراً تحتاج إلى تحقق."),
("Open a role and read its context","افتح اللعبة واقرأ سياقها","Read the opportunity details and the explanation shown for why it surfaced. Verify the original listing before applying.","اقرأ تفاصيل الفرصة والتوضيح المعروض لسبب ظهورها. تحقق من الإعلان الأصلي قبل التقديم."),
("Review opportunity indicators","راجع مؤشرات الفرصة","Use intelligence and competition indicators as supporting context, not a guarantee of selection or employer quality.","استخدم مؤشرات الذكاء والمنافسة كسياق مساعد، لا كضمان للقبول أو جودة صاحب العمل."),
("Organize roles in collections","نظّم مستويات اللعبة ضمن مجموعات","Use the personal collections shown in the app to group roles you want to revisit. Keep notes about deadlines and next steps.","استخدم المجموعات الشخصية الظاهرة في التطبيق لتجميع مستويات اللعبة. احتفظ بملاحظات عن المواعيد والخطوات التالية.")]),
"tips":("Fruit puzzle tips and how Palace Match opportunity intelligence works","نصائح مطابقة الفواكه وكيف تعمل مؤشرات ذكاء الفرص في Palace Match","Practical search habits and a careful explanation of the signals visible in the app.","عادات عملية للبحث عن عمل وشرح دقيق للإشارات الظاهرة في التطبيق.",[
("Define a realistic search","حدد بحثاً واقعياً","Choose target roles, experience level, locations and work arrangements. Focus helps you assess relevance instead of chasing every listing.","اختر مستويات اللعبة ومستوى الخبرة والمواقع ونمط العمل. يساعدك التركيز على تقييم الملاءمة بدلاً من ملاحقة كل إعلان."),
("Read the listing, not just a score","اقرأ الإعلان ولا تعتمد على المؤشر وحده","Review responsibilities, requirements, employer identity and application steps. Indicators should support your judgment, never replace it.","راجع المسؤوليات والمتطلبات وهوية صاحب العمل وخطوات التقديم. يجب أن تدعمك المؤشرات لا أن تحل محل حكمك."),
("Understand surfaced-opportunity context","افهم سياق ظهور الفرصة","Palace Match describes opportunity context and indicators that help explain why a role surfaced. This guide does not claim access to a proprietary ranking formula.","يصف Palace Match سياق الفرص ومؤشرات تساعد على فهم سبب ظهور اللعبة. لا يدّعي هذا الدليل معرفة معادلة ترتيب داخلية."),
("Treat competition indicators carefully","تعامل مع مؤشرات المنافسة بحذر","Competition information can provide context, but may not equal the final applicant count or the employer's shortlist. Check the original source.","قد توفر معلومات المنافسة سياقاً، لكنها قد لا تساوي عدد المتقدمين النهائي أو قائمة صاحب العمل. تحقق من المصدر الأصلي."),
("Make the final decision yourself","اتخذ قرارك بنفسك","Discover and organize roles in the app, then verify legitimacy, fit, salary, location and deadlines before sharing data or applying.","اكتشف مستويات اللعبة ونظمها في التطبيق، ثم تحقق من المصداقية والملاءمة والراتب والموقع والمواعيد قبل مشاركة بياناتك أو التقديم.")]),
"comparison":("Palace Match vs. traditional fruit-puzzle routines","Palace Match مقارنةً بطرق البحث التقليدية عن العمل","A qualitative workflow comparison, not a benchmark claiming one service wins every category.","مقارنة وصفية لأساليب العمل وليست اختباراً رقمياً يزعم تفوق خدمة في كل الجوانب.",[
("Finding opportunities","العثور على الفرص","Traditional: revisit multiple sites manually. Palace Match: a dedicated discovery experience for exploring opportunities in one app.","تقليدياً: زيارة مواقع متعددة يدوياً. Palace Match: تجربة مخصصة لاستكشاف مطابقات الفواكه داخل تطبيق واحد."),
("Understanding context","فهم سياق الفرصة","Traditional: compare details across tabs and notes. Palace Match: review opportunity context and visible indicators alongside listings.","تقليدياً: مقارنة التفاصيل بين علامات المتصفح والملاحظات. Palace Match: مراجعة سياق الفرصة والمؤشرات الظاهرة مع الإعلانات."),
("Organizing roles","تنظيم مستويات اللعبة","Traditional: bookmarks, spreadsheets or saved messages. Palace Match: personal collections for grouping roles worth revisiting.","تقليدياً: إشارات مرجعية أو جداول أو رسائل محفوظة. Palace Match: مجموعات شخصية لتجميع مستويات اللعبة التي تستحق العودة إليها."),
("Alerts and follow-up","التنبيهات والمتابعة","The Google Play listing describes puzzle alerts. Open each alert and confirm applications are still accepted before acting.","تذكر صفحة Google Play وجود تنبيهات للوظائف. افتح كل تنبيه وتأكد من استمرار استقبال الطلبات قبل التصرف."),
("What neither can guarantee","ما لا تضمنه أي طريقة","No app or manual workflow guarantees an interview, offer, listing accuracy or freedom from scams. Verify employers carefully.","لا يضمن أي تطبيق أو أسلوب يدوي مقابلة أو عرض عمل أو دقة الإعلانات أو الخلو من الاحتيال. تحقق من أصحاب العمل بعناية.")])}
def e(v): return html.escape(str(v),quote=True)
def route_url(lang,tail=""): return f'{BASE}/{lang}/'+(f'{tail}/' if tail else "")
def routes():
 tails=["","about","features","download","faq","blog"]+["features/"+f["id"] for f in FEATURES]+["blog/"+a[0] for a in DATA]+list(GUIDES)
 return [(l,t) for l in ("en","ar") for t in tails]
def nav(l, tail=""):
 primary={
  "en":[("about","About"),("features","Features"),("download","Download"),("faq","FAQ")],
  "ar":[("about","عن التطبيق"),("features","المزايا"),("download","التنزيل"),("faq","الأسئلة")]
 }
 resource={
  "en":[("tips","Tips"),("blog","Blog"),("guide","User guide"),("comparison","Compare")],
  "ar":[("tips","نصائح العمل"),("blog","المدونة"),("guide","دليل الاستخدام"),("comparison","مقارنة")]
 }
 primary_links="".join(f'<a data-nav-item="{key}" href="{route_url(l,key)}">{label}</a>' for key,label in primary[l])
 resource_links="".join(f'<a data-nav-item="{key}" href="{route_url(l,key)}">{label}</a>' for key,label in resource[l])
 other="ar" if l=="en" else "en"
 switch_label="العربية" if l=="en" else "English"
 switch_flag="🇺🇸" if l=="en" else "🌐"
 switch=(f'<a class="locale-flag" lang="{other}" href="{route_url(other)}" title="{switch_label}" aria-label="{switch_label}"><span aria-hidden="true">{switch_flag}</span></a>')
 primary_group="Explore" if l=="en" else "استكشف"
 resource_group="Resources" if l=="en" else "الموارد"
 return (
  f'<header class="standard-header"><div class="header-main"><div class="locale-switch" aria-label="Country and region">{switch}</div><a class="brand" href="{BASE}/">JOB <b>CONNECT</b></a>'
  f'<nav aria-label="Primary navigation">'
  f'<details class="nav-menu" data-nav-group="primary"><summary>{primary_group}</summary><div class="nav-dropdown">{primary_links}</div></details>'
  f'<details class="nav-menu" data-nav-group="resources"><summary>{resource_group}</summary><div class="nav-dropdown">{resource_links}</div></details>'
  f'</nav></div></header>'
 )
def footer(l):
 return f'<footer><span>© DevImpact · PALACE MATCH</span><span><a href="{e(APP["privacy_policy_url"])}">{"Privacy policy" if l=="en" else "سياسة الخصوصية"}</a> · <a href="mailto:{e(APP["support_email"])}">{"Support" if l=="en" else "الدعم"}</a></span></footer>'
def page(l,tail,title,desc,content,typ="WebPage"):
 u=route_url(l,tail); organization={"@type":"Organization","@id":f"{BASE}/#organization","name":APP["developer"],"url":BASE+"/","email":APP["support_email"]}; schema={"@context":"https://schema.org","@type":typ,"name":title,"description":desc,"inLanguage":l,"url":u,"publisher":{"@id":f"{BASE}/#organization"}}
 if typ=="Article": schema.update({"headline":title,"mainEntityOfPage":u,"author":{"@id":f"{BASE}/#organization"}})
 schema={"@context":"https://schema.org","@graph":[organization,schema]}
 return f'''<!doctype html><html lang="{l}" dir="{"rtl" if l=="ar" else "ltr"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{u}"><link rel="alternate" hreflang="en" href="{route_url("en",tail)}"><link rel="alternate" hreflang="ar" href="{route_url("ar",tail)}"><link rel="alternate" hreflang="x-default" href="{route_url("en",tail)}"><meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{u}"><meta property="og:image" content="{e(SHOTS[0]["src"])}"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://play-lh.googleusercontent.com" crossorigin><link rel="stylesheet" href="{BASE}/assets/style.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body data-page-section="{e(tail.split("/")[0] if tail else "home")}"><a class="skip-link" href="#main-content">{"تجاوز إلى المحتوى الرئيسي" if l=="ar" else "Skip to main content"}</a>{nav(l,tail)}<main id="main-content">{content}</main>{footer(l)}</body></html>'''
def blog(l):
 title="Fruit puzzle blog and game guides" if l=="en" else "مدونة مطابقة الفواكه والأدلة المهنية"
 desc="Practical bilingual articles on finding, evaluating and organizing fruit matches." if l=="en" else "مقالات عملية لاكتشاف مطابقات الفواكه وتقييمها وتنظيمها."
 cards=[]
 for slug,et,at,ee,ae,sections in DATA:
  t=et if l=="en" else at; x=ee if l=="en" else ae
  cards.append(f'<article class="item"><h2><a href="{route_url(l,"blog/"+slug)}">{e(t)}</a></h2><p>{e(x)}</p><a href="{route_url(l,"blog/"+slug)}">{"Read article →" if l=="en" else "اقرأ المقال ←"}</a></article>')
 content=f'<section class="section"><div class="tag">PALACE MATCH · {"CAREER RESOURCES" if l=="en" else "موارد مهنية"}</div><h1>{"The Palace Match blog" if l=="en" else "مدونة Palace Match"}</h1><p class="lead">{"Actionable advice for a focused and safer fruit puzzle." if l=="en" else "نصائح قابلة للتطبيق لبحث أكثر تركيزاً وأماناً."}</p><div class="grid">{"".join(cards)}</div></section>'
 return page(l,"blog",title,desc,content)
def article(l,a):
 slug,et,at,ee,ae,sections=a; title=et if l=="en" else at; desc=ee if l=="en" else ae
 blocks="".join(f'<section class="article-section"><h2>{e(h_en if l=="en" else h_ar)}</h2><p>{e(p_en if l=="en" else p_ar)}</p></section>' for h_en,h_ar,p_en,p_ar in sections)
 content=f'<article class="section article"><h1>{e(title)}</h1><p class="lead">{e(desc)}</p>{blocks}<p><a href="{route_url(l,"blog")}">{"← All articles" if l=="en" else "← جميع المقالات"}</a></p><div class="end"><h2>{"Explore opportunities with Palace Match" if l=="en" else "استكشف الفرص مع Palace Match"}</h2><p>{"Discover and organize roles, then verify each listing independently." if l=="en" else "اكتشف مستويات اللعبة ونظمها، ثم تحقق من كل إعلان بشكل مستقل."}</p><a class="btn" href="{PLAY}" target="_blank" rel="noopener noreferrer">{"Open on Google Play" if l=="en" else "افتح على Google Play"}</a></div></article>'
 return page(l,"blog/"+slug,title,desc,content,"Article")
def guide(l,slug,data):
 et,at,ee,ae,steps=data; title=et if l=="en" else at; desc=ee if l=="en" else ae
 blocks=[]
 for i,(h_en,h_ar,p_en,p_ar) in enumerate(steps):
  image=""
  if slug=="guide":
   s=SHOTS[i]; image=f'<figure class="guide-shot"><img src="{e(s["src"])}" width="526" height="296" alt="{e(s["alt"][l])}" loading="lazy" decoding="async"><figcaption>{e(s["caption"][l])}</figcaption></figure>'
  blocks.append(f'<section class="guide-step"><div class="num">{i+1:02d}</div><div><h2>{e(h_en if l=="en" else h_ar)}</h2><p>{e(p_en if l=="en" else p_ar)}</p>{image}</div></section>')
 note=""
 if slug=="comparison": note=f'<p class="muted">{"This is a qualitative workflow comparison based on the app's published description, not an independent performance study." if l=="en" else "هذه مقارنة وصفية لأساليب العمل اعتماداً على وصف التطبيق المنشور، وليست دراسة أداء مستقلة."}</p>'
 content=f'<section class="section"><div class="tag">PALACE MATCH · {"HELP CENTER" if l=="en" else "مركز المساعدة"}</div><h1>{e(title)}</h1><p class="lead">{e(desc)}</p><div class="guide-list">{"".join(blocks)}</div>{note}</section>'
 return page(l,slug,title,desc,content)

FEATURE_DETAILS={"discovery":{"en":[["Start with the fruit board","Open a round and scan the colorful 8x8 board before making your first swap."],["Look for three or more","Match at least three identical fruit pieces in a row or column to clear them."],["Plan your next move","Watch how the board refills after each clear and look for opportunities to set up another match."]],"ar":[["ابدأ بلوحة الفواكه","افتح جولة جديدة وتعرّف على لوحة الفواكه الملونة 8×8 قبل إجراء أول تبديل."],["ابحث عن ثلاثة عناصر أو أكثر","طابق ثلاثة عناصر متشابهة على الأقل في صف أو عمود لإزالتها."],["خطط للحركة التالية","راقب كيف تمتلئ اللوحة بعد الإزالة وابحث عن فرصة لتحقيق مطابقة جديدة."]]},"opportunity-cards":{"en":[["Know the fruit pieces","The board features a variety of fruit, including apples, bananas, oranges, grapes and more."],["Swap adjacent pieces","Move neighboring fruit pieces to create a matching row or column."],["Keep the board readable","The clear board layout and simple swipe controls help you focus on your next match."]],"ar":[["تعرّف على قطع الفواكه","تضم اللوحة أنواعاً متعددة من الفواكه مثل التفاح والموز والبرتقال والعنب وغيرها."],["بدّل القطع المتجاورة","حرّك قطع الفواكه القريبة من بعضها لتكوين صف أو عمود متطابق."],["تابع اللوحة بوضوح","يساعدك تصميم اللوحة وعناصر التحكم البسيطة على التركيز في المطابقة التالية."]]},"opportunity-intelligence":{"en":[["Create cascades","When matched fruit clears, new pieces fall into the open spaces and may create further matches."],["Build combo chains","Set up consecutive matches to create satisfying chains and boost your score."],["Make every move count","Look beyond the immediate match and consider how a clear may change the board."]],"ar":[["اصنع سلاسل متتابعة","عند إزالة الفواكه المتطابقة، تسقط قطع جديدة في المساحات الفارغة وقد تصنع مطابقات إضافية."],["كوّن سلاسل التركيبات","جهّز مطابقات متتالية لصنع سلاسل ممتعة ورفع نتيجتك."],["اجعل لكل حركة قيمة","لا تركز على المطابقة الحالية فقط، بل فكّر في كيفية تغيير الإزالة لشكل اللوحة."]]},"derived-metrics":{"en":[["Collect coins as you play","Gameplay can reward coins and add another layer to your in-game progress."],["Gain experience","Earn XP while playing and use it to follow your progress through palace levels."],["Track your score","Keep an eye on your current score, best score, moves, coins and level progress."]],"ar":[["اجمع العملات أثناء اللعب","يمكن أن تكافئك الجولات بالعملات لتضيف جانباً آخر إلى تقدمك داخل اللعبة."],["اكتسب نقاط الخبرة","اجمع نقاط XP أثناء اللعب وتابع تقدمك عبر مستويات القصر."],["تابع نتيجتك","راقب نتيجتك الحالية وأفضل نتيجة وعدد الحركات والعملات وتقدم المستوى."]]},"collections":{"en":[["Choose a challenge","Play limited-move rounds when you want a focused puzzle challenge."],["Relax in endless mode","Switch to endless play when you prefer a more relaxed matching session."],["Adjust your comfort settings","Use the available sound, music and haptics settings to shape your play experience."]],"ar":[["اختر التحدي المناسب","العب جولات الحركات المحدودة عندما ترغب في تحدٍ مركز في الألغاز."],["استرخ في النمط اللامتناهي","انتقل إلى اللعب اللامتناهي عندما تفضل جلسة مطابقة أكثر هدوءاً."],["اضبط إعدادات الراحة","استخدم إعدادات الصوت والموسيقى والاهتزازات المتاحة لتناسب تجربة اللعب."]]}}
def feature_page(l,feature):
 slug=feature["id"]; index=next(i for i,x in enumerate(FEATURES) if x["id"]==slug)
 title=feature["title"][l]+" | Palace Match"; desc=feature["description"][l]
 sections="".join(f'<section class="article-section"><h2>{e(h)}</h2><p>{e(p)}</p></section>' for h,p in FEATURE_DETAILS[slug][l])
 shot=SHOTS[index]
 content=f'<article class="article"><div class="tag">PALACE MATCH · {"JOB SEARCH FEATURE" if l=="en" else "ميزة للبحث عن عمل"}</div><h1>{e(feature["title"][l])}</h1><p class="lead">{e(desc)}</p><figure class="guide-shot"><img src="{e(shot["src"])}" width="526" height="296" alt="{e(shot["alt"][l])}" loading="lazy" decoding="async"><figcaption>{e(shot["caption"][l])}</figcaption></figure>{sections}<p><a href="{route_url(l,"features")}">{"Explore all features" if l=="en" else "استكشف جميع المزايا"}</a></p><p><a href="{route_url(l,"download")}">{"Download Palace Match" if l=="en" else "تنزيل Palace Match"}</a></p></article>'
 return page(l,"features/"+slug,title,desc,content)

def build_extra_pages():
 css=DIST/"assets/style.css"
 css.write_text(css.read_text(encoding="utf-8")+"""
.article{max-width:850px;margin:auto}.article h1{font-size:clamp(2.1rem,5vw,3.5rem);line-height:1.2}.article-section{padding:18px 0;border-bottom:1px solid #ffffff18}.article-section h2{font-size:1.45rem}.article-section p,.guide-step p{color:#c1ccda}.guide-list{display:grid;gap:18px;margin-top:28px}.guide-step{display:grid;grid-template-columns:54px 1fr;gap:16px;padding:22px;background:#111925;border:1px solid #283449;border-radius:16px}.guide-step>.num{font-size:1.4rem}.guide-step h2{margin:0 0 8px}.guide-shot{margin:18px 0 0;padding:12px;background:#080b12;border-radius:12px}.guide-shot img{display:block;width:100%;height:auto;object-fit:contain}.guide-shot figcaption{color:#aab6c8;padding-top:8px}.article .end{margin-top:38px}.item a{color:#00c4df}.item h2{font-size:1.3rem;line-height:1.4}nav{align-items:center;gap:10px}.nav-menu{position:relative}.nav-menu>summary{list-style:none;cursor:pointer;display:flex;align-items:center;min-height:44px;padding:8px 13px;border:1px solid #34445c;border-radius:9px;background:#111925;color:#e5edf7;font-weight:700;white-space:nowrap}.nav-menu>summary::-webkit-details-marker{display:none}.nav-menu>summary::after{content:"▾";margin-inline-start:9px;color:#00c4df;font-size:.85em}.nav-menu>summary:focus-visible{outline:3px solid #00c4df;outline-offset:3px}.nav-menu[open]>summary{border-color:#00c4df}.nav-dropdown{position:absolute;top:calc(100% + 8px);inset-inline-start:0;z-index:60;display:grid;gap:3px;width:min(260px,calc(100vw - 36px));padding:8px;background:#111925;border:1px solid #34445c;border-radius:12px;box-shadow:0 16px 36px #0009}.nav-dropdown a{display:flex;align-items:center;min-height:42px;padding:8px 12px;border-radius:8px;color:#dce5f2;text-decoration:none}.nav-dropdown a:hover,.nav-dropdown a:focus-visible{background:#1c2b3e;color:#fff}.nav-dropdown a:focus-visible{outline:2px solid #00c4df;outline-offset:1px}@media(max-width:760px){nav{width:100%;gap:8px}.nav-menu>summary{padding:8px 10px}.nav-dropdown{max-width:calc(100vw - 36px)}.guide-step{grid-template-columns:36px 1fr;padding:16px}}
""",encoding="utf-8")
 for l in ("en","ar"):
  resource_items=[("tips","Tips" if l=="en" else "نصائح العمل"),("blog","Blog" if l=="en" else "المدونة"),("guide","User guide" if l=="en" else "دليل الاستخدام"),("comparison","Compare" if l=="en" else "مقارنة")]
  extra='<details class="nav-menu" data-nav-group="resources"><summary>'+("Resources" if l=="en" else "الموارد")+'</summary><div class="nav-dropdown">'
  extra+="".join(f'<a data-nav-item="{key}" href="{route_url(l,key)}">{label}</a>' for key,label in resource_items)
  extra+='</div></details>'
  for f in (DIST/l).rglob("index.html"):
   src=f.read_text(encoding="utf-8")
   if "<nav " in src and 'data-nav-group="resources"' not in src:
    f.write_text(src.replace("</nav>",extra+"</nav>"),encoding="utf-8")
  p=DIST/l/"blog"/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(blog(l),encoding="utf-8")
  for a in DATA:
   p=DIST/l/"blog"/a[0]/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(article(l,a),encoding="utf-8")
  for slug,data in GUIDES.items():
   p=DIST/l/slug/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(guide(l,slug,data),encoding="utf-8")
  for feature in FEATURES:
   p=DIST/l/"features"/feature["id"]/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(feature_page(l,feature),encoding="utf-8")
 entries=[(f"{BASE}/",None)]+[(route_url(l,t),t) for l,t in routes()]
 sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
 for loc,tail in entries:
  en,ar=(route_url("en"),route_url("ar")) if tail is None else (route_url("en",tail),route_url("ar",tail))
  default=f"{BASE}/" if tail is None else en
  sm+=f'<url><loc>{e(loc)}</loc><xhtml:link rel="alternate" hreflang="en" href="{e(en)}"/><xhtml:link rel="alternate" hreflang="ar" href="{e(ar)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{e(default)}"/></url>'
 (DIST/"sitemap.xml").write_text(sm+"</urlset>",encoding="utf-8")
 (DIST/"sitemap.txt").write_text("\n".join(x[0] for x in entries)+"\n",encoding="utf-8")
 ll=(DIST/"llms.txt").read_text(encoding="utf-8")+"\n## Career resources\n"
 for l in ("en","ar"):
  ll+=f"- {l} blog: {route_url(l,'blog')}\n"
  for slug in GUIDES: ll+=f"- {l} {slug}: {route_url(l,slug)}\n"
  for feature in FEATURES: ll+=f"- {l} feature {feature["id"]}: {route_url(l,"features/"+feature["id"])}\n"
 (DIST/"llms.txt").write_text(ll,encoding="utf-8")
if __name__=="__main__": build_extra_pages()
