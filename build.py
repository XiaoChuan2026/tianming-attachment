# -*- coding: utf-8 -*-
"""生成「依恋类型」测试：data.json（供校验）+ 单文件 index.html"""
import json, os

OUT = "/root/.codebuddy/artifact/tianming-attachment"
os.makedirs(OUT, exist_ok=True)

# ====== 题目 ======
# 权重键：ax=焦虑, av=回避; 细分键 sw/sl(安全·温暖/松弛) ao/at(焦虑·粘人/试探) ad/ac(回避·疏离/高冷) fs/ff(恐惧·纠结/逃离)
# 结构：
#  set1 (6题): 安全 / 焦虑(ax2) / 恐惧冲突(ax2,av1)
#  set2 (6题): 安全 / 回避(av2) / 恐惧冲突(ax1,av2)
#  pure_anx (2题): 安全 / 焦虑(ax2) / 焦虑轻(ax1)   -> 推高焦虑轴
#  pure_avo (2题): 安全 / 回避(av2) / 回避轻(av1)   -> 推高回避轴
#  tiebreak (8题): 象限内细分二选一
QUESTIONS = [
    # ---- set1: 安全 / 焦虑 / 恐惧冲突 ----
    {"q":"你发消息后对方一直没回，你通常：",
     "opts":[
        {"t":"开始胡思乱想：他是不是不在乎我了","w":{"ax":2}},
        {"t":"没啥感觉，他可能在忙，我先干别的","w":{}},
        {"t":"一边慌一边赌气，故意也慢回他","w":{"ax":2,"av":1}},
     ]},
    {"q":"他说“我们慢慢来，别急”，你心里：",
     "opts":[
        {"t":"有点慌：他是不是想淡了","w":{"ax":2}},
        {"t":"挺好，顺其自然","w":{}},
        {"t":"表面答应，心里却更怕失去，反而更黏","w":{"ax":2,"av":1}},
     ]},
    {"q":"你更容易因为哪种事不安：",
     "opts":[
        {"t":"怕被丢下、怕他不爱了","w":{"ax":2}},
        {"t":"都还好，比较淡定","w":{}},
        {"t":"既怕丢下、又怕靠太近，自己都矛盾","w":{"ax":2,"av":1}},
     ]},
    {"q":"对方晚归没提前说，你的反应：",
     "opts":[
        {"t":"立刻电话、连环问“你在哪”","w":{"ax":2}},
        {"t":"他解释了我就信","w":{}},
        {"t":"一边查岗一边告诉自己别管，内心拉扯","w":{"ax":2,"av":1}},
     ]},
    {"q":"你表达爱意的方式更偏向：",
     "opts":[
        {"t":"黏着、确认、总说“想你”","w":{"ax":2}},
        {"t":"自然地关心和分享","w":{}},
        {"t":"想靠近又怕太黏，话到嘴边又憋回去","w":{"ax":2,"av":1}},
     ]},
    {"q":"前任或朋友常评价你是：",
     "opts":[
        {"t":"太粘人、太敏感","w":{"ax":2}},
        {"t":"挺好相处、好沟通","w":{}},
        {"t":"忽冷忽热，让人猜不透","w":{"ax":2,"av":1}},
     ]},
    # ---- set2: 安全 / 回避 / 恐惧冲突 ----
    {"q":"伴侣想每天视频、黏在一起，你的感受：",
     "opts":[
        {"t":"挺好，适度就好","w":{}},
        {"t":"太近了，我需要个人空间","w":{"av":2}},
        {"t":"既享受又怕被绑住，忽冷忽热","w":{"ax":1,"av":2}},
     ]},
    {"q":"吵架之后，你的第一反应：",
     "opts":[
        {"t":"冷静一会儿，再好好谈","w":{}},
        {"t":"不想说话，自己待着消化","w":{"av":2}},
        {"t":"想沟通又怕被缠，先躲开半步","w":{"ax":1,"av":2}},
     ]},
    {"q":"你怎么看“在关系里需要对方”：",
     "opts":[
        {"t":"互相需要，也互相独立","w":{}},
        {"t":"尽量不依赖，靠自己最稳","w":{"av":2}},
        {"t":"想依赖，又怕依赖会弄丢自己","w":{"ax":1,"av":2}},
     ]},
    {"q":"对方情绪崩溃找你，你一般：",
     "opts":[
        {"t":"稳稳陪着，听他说","w":{}},
        {"t":"不太会接，想躲开一点","w":{"av":2}},
        {"t":"想安慰，又怕被他的情绪淹没，退半步","w":{"ax":1,"av":2}},
     ]},
    {"q":"关系稳定下来之后，你会：",
     "opts":[
        {"t":"一如既往，状态稳定","w":{}},
        {"t":"反而想往后退一点","w":{"av":2}},
        {"t":"更安心了，却莫名其妙想逃","w":{"ax":1,"av":2}},
     ]},
    {"q":"你对身体接触、亲密举动的需求：",
     "opts":[
        {"t":"看心情，不勉强","w":{}},
        {"t":"比较少，太近会不自在","w":{"av":2}},
        {"t":"想要，又怕太近不自在","w":{"ax":1,"av":2}},
     ]},
    # ---- pure_anx ----
    {"q":"你独自一个人的时候，感觉：",
     "opts":[
        {"t":"有点空，想有人陪","w":{"ax":2}},
        {"t":"挺自在，独处相处都行","w":{}},
        {"t":"更想陪他，又怕打扰","w":{"ax":1}},
     ]},
    {"q":"你觉得自己“值得被爱”吗：",
     "opts":[
        {"t":"有点不确定，总怕自己不够好","w":{"ax":2}},
        {"t":"确定，我本身就值得","w":{}},
        {"t":"总想证明自己够好给他看","w":{"ax":1}},
     ]},
    # ---- pure_avo ----
    {"q":"对方突然对你特别热情，你会：",
     "opts":[
        {"t":"开心地加倍回应","w":{}},
        {"t":"有点警惕，怕他“有求于我”","w":{"av":2}},
        {"t":"享受，但保持一点距离","w":{"av":1}},
     ]},
    {"q":"你常被认为是一个：",
     "opts":[
        {"t":"好沟通、好相处的人","w":{}},
        {"t":"太冷淡、太独立的人","w":{"av":2}},
        {"t":"有点距离感的人","w":{"av":1}},
     ]},
    # ---- tiebreak 安全 ----
    {"q":"你在关系里更常被身边人说：",
     "opts":[
        {"t":"温暖主动，爱把爱说出口","w":{"sw":1}},
        {"t":"松弛淡定，不黏人","w":{"sl":1}},
     ]},
    {"q":"你更享受关系的哪一面：",
     "opts":[
        {"t":"互相分享琐事、主动照顾对方","w":{"sw":1}},
        {"t":"各自舒服，不必时刻黏着","w":{"sl":1}},
     ]},
    # ---- tiebreak 焦虑 ----
    {"q":"你不安全感发作的时候，更常：",
     "opts":[
        {"t":"直接黏上去要确认、要抱抱","w":{"ao":1}},
        {"t":"嘴上说没事，用冷淡试探他在不在乎","w":{"at":1}},
     ]},
    {"q":"对方回消息变慢，你更可能：",
     "opts":[
        {"t":"直接发“你在干嘛，想你了”","w":{"ao":1}},
        {"t":"故意晚回、发朋友圈气他，看他急不急","w":{"at":1}},
     ]},
    # ---- tiebreak 回避 ----
    {"q":"你需要空间的时候，你会：",
     "opts":[
        {"t":"说“我想静静”，但待会儿会回来","w":{"ad":1}},
        {"t":"直接消失，不解释","w":{"ac":1}},
     ]},
    {"q":"对方想深聊感受，你通常：",
     "opts":[
        {"t":"不太擅长，但愿意听","w":{"ad":1}},
        {"t":"转移话题、冷处理","w":{"ac":1}},
     ]},
    # ---- tiebreak 恐惧 ----
    {"q":"你推开对方之后，通常：",
     "opts":[
        {"t":"又忍不住回头找他","w":{"fs":1}},
        {"t":"彻底断联，先跑为敬","w":{"ff":1}},
     ]},
    {"q":"深夜情绪上头时，你更常：",
     "opts":[
        {"t":"发一堆真心话又删，反复拉扯","w":{"fs":1}},
        {"t":"直接冷暴力、拉黑，眼不见为净","w":{"ff":1}},
     ]},
]

# ====== 8 个类型结果 ======
TYPES = {
 "t1":{
   "name":"安全自在型","cat":"安全型",
   "oneliner":"你自带安全感，爱得从容，也放得下。",
   "chips":["松弛","信任","边界"],
   "combo":[
     {"word":"松弛","desc":"你不把关系当救生圈。对方忙、回得慢、暂时不在，你都不会炸，因为你的安稳来自自己，不来自别人的秒回。"},
     {"word":"信任","desc":"你默认“他是爱我的”，除非有证据才怀疑。这让你省下大量内耗，也给了伴侣极大的呼吸感。"},
     {"word":"边界","desc":"你分得清“我需要你”和“我失去你就不行”。能亲密，也能各自安好——这是健康依恋最贵的能力。"},
   ],
   "show":{
     "亲密关系":"既能热烈相拥，也能各自安好；有矛盾愿意说开，不冷战不消失。",
     "日常相处":"不查岗、不pua、不阴阳怪气；把依赖和独立平衡得很好。",
     "发消息时":"想发就发，不回就先忙自己的，不会脑补“他不在乎我”。",
   },
   "mono":"我值得被爱，也不怕失去爱。",
   "impact":{"good":"和你在一起像回到家，对方能彻底放松，不必小心翼翼。","bad":"偶尔你太“淡定”，会让需要热乎劲的人觉得你不够上心。"},
   "mine":"别因为太松弛显得冷漠；也别总说“我都行”，把自己的真实需求藏没了。",
   "fix":"你已经很好。只需偶尔主动说一句“我很在乎你”，给伴侣一点确定感，关系会更暖。",
   "week":"今天主动给对方发一条“想到你了”的消息，不带任何请求、不期待回复。",
   "match":"和谁都合得来，尤其能稳住焦虑型和恐惧型。",
 },
 "t2":{
   "name":"温暖滋养型","cat":"安全型",
   "oneliner":"你是关系里的小太阳，擅长把爱说出口。",
   "chips":["主动","共情","稳定"],
   "combo":[
     {"word":"主动","desc":"你不等对方猜，爱就表达、想就发声。主动分享、主动照顾，让关系一直有温度。"},
     {"word":"共情","desc":"对方低落时你第一个靠近，能接住情绪。你的稳定是身边人最大的安全感来源。"},
     {"word":"稳定","desc":"你情绪起伏不大，吵架先伸手，不玩消失。这种可预测性，是亲密关系里极稀缺的温柔。"},
   ],
   "show":{
     "亲密关系":"主动表达、记得小事；对方脆弱你第一个接住，把“我们”放在“我”前面。",
     "日常相处":"情绪稳定，有矛盾先沟通；愿意为关系花心思，而不是等对方来。",
     "发消息时":"爱发语音、表情包、琐碎日常，分享欲旺盛，黏但不让人窒息。",
   },
   "mono":"我想让你知道，你对我很重要。",
   "impact":{"good":"被你爱很幸福，对方会被稳稳托住。","bad":"分享太多、付出太多，可能压到需要空间的人，或被当成“理所当然”。"},
   "mine":"别用付出来“换”对方的同等回应；也别把对方的情绪全揽到自己身上。",
   "fix":"留一点空间让对方主动，也允许自己偶尔被照顾。爱别人之前，先把自己喂饱。",
   "week":"今天忍住一次“秒回”，看看对方会不会主动来找你——信任他也会想你。",
   "match":"最配回避型（你慢慢融化他）和安全型。",
 },
 "t3":{
   "name":"焦虑粘人型","cat":"焦虑型",
   "oneliner":"你爱得用力，越在乎越怕抓不住。",
   "chips":["焦虑","索取确认","敏感"],
   "combo":[
     {"word":"焦虑","desc":"你的安全感开关在对方手里。他一冷，你就慌；他一热，你才踏实。这不是作，是怕被丢下。"},
     {"word":"索取确认","desc":"你需要反复听到“我爱你”“我在乎你”才安心。确认感像充电，充一次管不了多久。"},
     {"word":"敏感","desc":"对方一个语气、一个省略号，你都能读出潜台词。感受力很强，但也更容易受伤。"},
   ],
   "show":{
     "亲密关系":"需要高频确认；对方稍冷你就慌、容易吃醋；把对方当情绪重心。",
     "日常相处":"他一句话能让你上天堂下地狱；很黏，也很怕失去。",
     "发消息时":"已读不回=世界末日；反复看聊天记录找“他是不是变了”的证据。",
   },
   "mono":"别走，证明你不会丢下我。",
   "impact":{"good":"被你需要很甜，对方能感受到自己被深深在乎。","bad":"持续索取确认会让对方窒息、想逃，反而把你最怕的“失去”逼近。"},
   "mine":"别连环夺命call；别用“分手”试探爱；别偷看对方手机。",
   "fix":"把确认感从“他给”转到“我给自己”：焦虑来袭先深呼吸，做件让自己踏实的事，再决定要不要问。",
   "week":"下次想问“你爱我吗”之前，先写下3件“他爱我的证据”，往往就不必问了。",
   "match":"配安全型最稳；两个焦虑型会互相耗尽。",
 },
 "t4":{
   "name":"试探博弈型","cat":"焦虑型",
   "oneliner":"你不敢直接要爱，于是用“推开”来测试爱。",
   "chips":["试探","内耗","患得患失"],
   "combo":[
     {"word":"试探","desc":"你不直接说“我想你”，而是用冷淡、忽冷忽热看对方在不在乎。想被追，又不好意思承认。"},
     {"word":"内耗","desc":"嘴上说“随便你”，心里记小本本。反复推拉，最后累的是自己，对方还一头雾水。"},
     {"word":"患得患失","desc":"他靠近你退，他退你追。你不是不爱，是不敢信“他真的会留下”。"},
   ],
   "show":{
     "亲密关系":"嘴上说随便，心里记账；用冷淡试探对方是否在乎，越被爱越想验证。",
     "日常相处":"对方越靠近你越想逃，对方一退你又追，自己先累瘫。",
     "发消息时":"故意晚回、回了又撤回、发“在忙”其实在等他，看他会不会急。",
   },
   "mono":"如果你真的爱我，就该看穿我的嘴硬。",
   "impact":{"good":"一旦真正接纳你，对方会得到很深的你。","bad":"猜不透让你的人心累，容易误判你“根本不在乎”。"},
   "mine":"别用沉默当武器；别让人靠“猜”来爱你——没人能一直猜对。",
   "fix":"练习“直接说需求”：把“你都不来找我”换成“我想你了，可以聊会儿吗”。",
   "week":"连续3天，有一次需求直接说出口，不绕弯、不钓鱼。",
   "match":"安全型能接住你的试探；回避型会和你玩成死循环。",
 },
 "t5":{
   "name":"回避疏离型","cat":"回避型",
   "oneliner":"你不是不爱，是不知道怎么“靠太近”。",
   "chips":["回避","独立","隔离"],
   "combo":[
     {"word":"回避","desc":"关系一深入你就想后撤。不是嫌弃对方，是亲密对你来说像一种“被吞没”的危险。"},
     {"word":"独立","desc":"你很能自己待着、自己解决问题。独立是你的骄傲，也是你的壳。"},
     {"word":"隔离","desc":"情绪习惯自己消化，不习惯求助。难过时你更倾向于“一个人静静”，而不是找人。"},
   ],
   "show":{
     "亲密关系":"关系升温就想后撤；讨厌被黏；需要大量独处来“充电”。",
     "日常相处":"少说甜话，用行动多于语言；情绪自己扛，不轻易开口求助。",
     "发消息时":"能看到但不想回；回得短、慢、理性，怕被情绪淹没。",
   },
   "mono":"靠太近，我会丢了自己。",
   "impact":{"good":"独立不粘人，给对方充分的自由。","bad":"冷淡常被误解为“不爱了”，伴侣会不安、会胡思乱想。"},
   "mine":"别在对方脆弱时消失；别用“我需要空间”当永久挡箭牌。",
   "fix":"提前报备：“我要独处两小时，但不是不要你。”给伴侣确定感，再慢慢多给一点温度。",
   "week":"今天主动分享一件“无聊小事”给伴侣，不期待回复，只是让他知道你在。",
   "match":"配安全型/温暖型最舒服；两个回避型会处成室友。",
 },
 "t6":{
   "name":"高冷抽离型","cat":"回避型",
   "oneliner":"你把心门锁得很死，亲密对你像危险。",
   "chips":["抽离","自我","压抑"],
   "combo":[
     {"word":"抽离","desc":"几乎不暴露脆弱。关系一升温你就降温，用理性把自己和情绪隔开。"},
     {"word":"自我","desc":"你极度重视边界，讨厌被安排、被入侵。你的世界有门，但很少给人钥匙。"},
     {"word":"压抑","desc":"不是没感觉，是把感觉压下去了。久而久之，连你自己都分不清“不想”和“不敢”。"},
   ],
   "show":{
     "亲密关系":"极少暴露脆弱；关系认真就降温；用理性压抑情感，不轻易交心。",
     "日常相处":"边界感极强，冲突时冷处理、甚至消失，不喜欢被追着聊。",
     "发消息时":"能不回就不回；回了也很公事公办；很少主动开启话题。",
   },
   "mono":"感情太麻烦，靠自己最稳。",
   "impact":{"good":"稳定、不纠缠，给对方空间。","bad":"长期被冷落，伴侣会怀疑自己“是不是多余”，最终真的走掉。"},
   "mine":"别用消失惩罚对方；别把伴侣的在乎当负担甩开。",
   "fix":"从“微小暴露”开始：每周说一件真实感受，哪怕只是“今天有点累”。",
   "week":"想逃时，先发一句“我现在需要静一静，但明天找你”，代替彻底消失。",
   "match":"安全型最好；焦虑型会追着你跑崩。",
 },
 "t7":{
   "name":"恐惧纠结型","cat":"恐惧型",
   "oneliner":"你又想靠近，又怕被伤，于是边爱边逃。",
   "chips":["恐惧","推拉","矛盾"],
   "combo":[
     {"word":"恐惧","desc":"你渴望亲密，又深信“靠近就会受伤”。这种底层恐惧，让你在幸福里也睡不安稳。"},
     {"word":"推拉","desc":"前一秒黏人，后一秒推开。你不是在玩弄对方，是你自己都分不清到底要不要。"},
     {"word":"矛盾","desc":"既想要确认，又怕确认；既盼他回，又怕他回。你卡在“想要”和“怕要”中间。"},
   ],
   "show":{
     "亲密关系":"前一秒黏人后一秒推开；既渴望确认又害怕确认；极易被“不确定”折磨。",
     "日常相处":"信任很难建立，对方好你疑心“别有目的”；小事能脑补成大危机。",
     "发消息时":"回得忽冷忽热；深夜发长篇，白天装没事；既盼他回又怕他回。",
   },
   "mono":"我想要你，又怕你靠近后伤我。",
   "impact":{"good":"你给的爱很浓、很真，被你真正接纳的人会被深深打动。","bad":"反复推拉把对方搞晕，关系像坐过山车，谁都累。"},
   "mine":"别用“拉黑又加回”测试；别在深夜做重大关系决定。",
   "fix":"给情绪“降温12小时”再行动；把“他会不会害我”换成“先看看事实是什么”。",
   "week":"下次想推开对方前，先问自己：“我是真的想分，还是只是怕？”",
   "match":"安全型是解药；两个恐惧型会互相引爆。",
 },
 "t8":{
   "name":"崩塌逃离型","cat":"恐惧型",
   "oneliner":"亲密关系一认真，你就想“先跑为敬”。",
   "chips":["逃离","自我保护","崩塌"],
   "combo":[
     {"word":"逃离","desc":"关系越甜你越慌。你用“先离开”来避免“被离开”，宁可主动断，不愿被动伤。"},
     {"word":"自我保护","desc":"你筑了一整套防御：忙碌、新欢、冷漠，都是为了“别让我再疼一次”。"},
     {"word":"崩塌","desc":"一旦动心，旧伤口就像被掀开。你逃的不是这个人，是“再次失去”的可能性。"},
   ],
   "show":{
     "亲密关系":"关系越甜越慌；一感觉到动心就制造矛盾、抽身。",
     "日常相处":"用忙碌/新欢/冷漠自我保护；表面潇洒，独处时其实空落落的。",
     "发消息时":"热恋期突然断联；用“我们不合适”提前结束，避免被甩。",
   },
   "mono":"先离开的人，不会被抛弃。",
   "impact":{"good":"独立不缠，分寸感强。","bad":"伴侣常莫名其妙被“判出局”，深受其伤，还不知道自己错在哪。"},
   "mine":"别用冷暴力分手；别在新关系里重演旧剧本。",
   "fix":"识别你的“逃跑触发点”（比如对方说“我爱你”），那一刻告诉自己：“这是喜欢，不是危险。”",
   "week":"想逃时，给信任的朋友发一句“我有点想逃，但不是因为不爱”，先破掉沉默。",
   "match":"安全型 + 你愿意慢下来；别找同样爱逃的。",
 },
}

# ====== 阈值 ======
AX_MAX = sum(max((o["w"].get("ax",0) for o in q["opts"]), default=0) for q in QUESTIONS)
AV_MAX = sum(max((o["w"].get("av",0) for o in q["opts"]), default=0) for q in QUESTIONS)
AX_THRESH = max(7, round(AX_MAX*0.40))
AV_THRESH = max(7, round(AV_MAX*0.40))

DATA = {
  "questions": QUESTIONS,
  "types": TYPES,
  "axThresh": AX_THRESH,
  "avThresh": AV_THRESH,
  "axMax": AX_MAX,
  "avMax": AV_MAX,
}
with open(os.path.join(OUT,"data.json"),"w",encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False)
print("AX_MAX",AX_MAX,"AV_MAX",AV_MAX,"thresh",AX_THRESH,AV_THRESH,"questions",len(QUESTIONS))

# ====== HTML ======
HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>依恋类型测试</title>
<style>
:root{
  --bg1:#150a1f; --bg2:#2e1430; --bg3:#4a1f3e;
  --gold:#f7b2c9; --gold2:#c9a7eb; --text:#f5ecf3; --muted:#bda4b6;
  --card:rgba(255,255,255,.06); --line:rgba(247,178,201,.28);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;
  color:var(--text);
  background:linear-gradient(160deg,var(--bg1) 0%,var(--bg2) 55%,var(--bg3) 100%);
  background-attachment:fixed;min-height:100vh;
  line-height:1.7;padding:0 0 84px;
}
.wrap{max-width:640px;margin:0 auto;padding:26px 20px 20px}
.center{text-align:center}
h1{font-size:27px;margin:6px 0 4px;letter-spacing:1px;font-weight:800;
  color:#f7b2c9;
  background:linear-gradient(90deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:var(--muted);font-size:14px;margin:0 0 22px}
.pill{display:inline-block;padding:5px 14px;border:1px solid var(--line);border-radius:999px;
  font-size:12px;color:var(--gold);margin-bottom:14px;letter-spacing:1px}
.btn{display:block;width:100%;border:none;border-radius:16px;padding:16px;
  font-size:17px;font-weight:700;color:#2a0f24;cursor:pointer;
  background:linear-gradient(90deg,var(--gold),var(--gold2));
  box-shadow:0 8px 26px rgba(247,178,201,.28);transition:.15s}
.btn:active{transform:scale(.98)}
.btn.ghost{background:transparent;color:var(--gold);border:1px solid var(--line);box-shadow:none;font-weight:600}
.hide{display:none!important}
/* quiz */
.bar{height:6px;border-radius:99px;background:rgba(255,255,255,.1);overflow:hidden;margin:8px 0 4px}
.bar>i{display:block;height:100%;border-radius:99px;
  background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width .25s}
.qno{font-size:13px;color:var(--muted);text-align:right;margin-bottom:14px}
.q{font-size:19px;font-weight:700;margin:6px 0 18px}
.opt{display:block;width:100%;text-align:left;margin:11px 0;padding:15px 16px;border-radius:14px;
  border:1px solid rgba(255,255,255,.12);background:var(--card);color:var(--text);
  font-size:15.5px;cursor:pointer;transition:.15s;line-height:1.5}
.opt:active{transform:scale(.99)}
.opt.on{border-color:var(--gold);background:rgba(247,178,201,.16);
  box-shadow:0 0 0 2px rgba(247,178,201,.25) inset}
.nav{display:flex;gap:12px;margin-top:22px}
.nav .btn{padding:14px}
/* result */
.res-ct{max-width:640px;margin:0 auto;padding:24px 18px 20px}
.res-cat{color:var(--gold);font-size:14px;letter-spacing:3px;text-align:center}
.res-name{font-size:30px;font-weight:800;text-align:center;margin:4px 0 8px;
  color:#f7b2c9;
  background:linear-gradient(90deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.res-one{text-align:center;color:var(--muted);font-size:15px;margin:0 0 18px}
.chips{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:0 0 20px}
.chip{padding:6px 14px;border:1px solid var(--line);border-radius:999px;font-size:13px;color:var(--gold)}
.block{background:var(--card);border:1px solid rgba(255,255,255,.1);border-radius:16px;
  padding:16px 16px;margin:14px 0}
.block h3{margin:0 0 10px;font-size:16px;color:var(--gold);display:flex;align-items:center;gap:8px}
.block h3 b{width:22px;height:22px;border-radius:7px;display:inline-flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,var(--gold),var(--gold2));color:#2a0f24;font-size:13px;font-weight:800}
.kw{margin:10px 0}
.kw .w{font-weight:800;color:var(--text);font-size:15px}
.kw .w::before{content:"▍";color:var(--gold);margin-right:6px}
.kw .d{color:var(--muted);font-size:14px;display:block;margin-top:2px}
.show-row{margin:9px 0}
.show-row .lab{color:var(--gold2);font-weight:700;font-size:14px}
.show-row .val{color:var(--text);font-size:14.5px;display:block;margin-top:1px}
.mono{font-style:italic;color:var(--gold);font-size:16px;text-align:center;padding:6px 0}
.axis{margin:6px 0 2px}
.axis .top{display:flex;justify-content:space-between;font-size:13px;color:var(--muted);margin-bottom:4px}
.axis .track{height:9px;border-radius:99px;background:rgba(255,255,255,.1);overflow:hidden}
.axis .track>i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--gold),var(--gold2))}
.tip{font-size:12.5px;color:var(--muted);text-align:center;margin:18px 0 6px;line-height:1.6}
footer{position:fixed;bottom:0;left:0;right:0;height:46px;display:flex;align-items:center;justify-content:center;
  background:rgba(21,10,31,.92);backdrop-filter:blur(8px);border-top:1px solid var(--line);
  color:var(--gold);font-size:13.5px;letter-spacing:1px;z-index:50}
</style>
</head>
<body>
<div id="intro" class="wrap center">
  <span class="pill">依恋风格 · 心理测评</span>
  <h1>依恋类型测试</h1>
  <p class="sub">恋爱里你是哪一种？<br>看清自己的相处模式，把关系处得更舒服。</p>
  <button class="btn" onclick="start()">开始测试</button>
</div>

<div id="quiz" class="wrap hide">
  <div class="bar"><i id="bar"></i></div>
  <div class="qno" id="qno"></div>
  <div class="q" id="q"></div>
  <div id="opts"></div>
  <div class="nav">
    <button class="btn ghost" id="prevBtn" onclick="prev()">上一题</button>
    <button class="btn" id="nextBtn" onclick="next()">下一题</button>
  </div>
</div>

<div id="result" class="res-ct hide"></div>

<footer>原创出品 © 小船</footer>

<script>
const DATA = __DATA__;
const Q = DATA.questions, T = DATA.types;
const AX_T = DATA.axThresh, AV_T = DATA.avThresh, AX_M = DATA.axMax, AV_M = DATA.avMax;
let answers = new Array(Q.length).fill(-1);
let cur = 0;

function start(){ document.getElementById('intro').classList.add('hide');
  document.getElementById('quiz').classList.remove('hide'); renderQ(); }

function renderQ(){
  const q = Q[cur];
  document.getElementById('bar').style.width = (cur/Q.length*100)+'%';
  document.getElementById('qno').textContent = '第 '+(cur+1)+' / '+Q.length+' 题';
  document.getElementById('q').textContent = q.q;
  const box = document.getElementById('opts'); box.innerHTML='';
  q.opts.forEach((o,i)=>{
    const b=document.createElement('button');
    b.className='opt'+(answers[cur]===i?' on':'');
    b.textContent=o.t; b.onclick=()=>choose(i); box.appendChild(b);
  });
  document.getElementById('prevBtn').style.visibility = cur===0?'hidden':'visible';
  document.getElementById('nextBtn').textContent = (cur===Q.length-1)?'查看结果':'下一题';
}
function choose(i){ answers[cur]=i; renderQ(); setTimeout(()=>next(), 260); }
function next(){
  if(answers[cur]===-1) return;
  if(cur<Q.length-1){cur++;renderQ();}
  else{ document.getElementById('bar').style.width='100%'; finish(); }
}
function prev(){ if(cur>0){cur--;renderQ();} }

function compute(a){
  let ax=0,av=0,sw=0,sl=0,ao=0,at=0,ad=0,ac=0,fs=0,ff=0;
  Q.forEach((q,i)=>{ const w=q.opts[a[i]].w||{};
    ax+=w.ax||0; av+=w.av||0; sw+=w.sw||0; sl+=w.sl||0;
    ao+=w.ao||0; at+=w.at||0; ad+=w.ad||0; ac+=w.ac||0;
    fs+=w.fs||0; ff+=w.ff||0; });
  const axHi=ax>=AX_T, avHi=av>=AV_T;
  let type;
  if(!axHi&&!avHi) type = sw>=sl?'t2':'t1';
  else if(axHi&&!avHi) type = ao>=at?'t3':'t4';
  else if(!axHi&&avHi) type = ac>=ad?'t6':'t5';
  else type = ff>=fs?'t8':'t7';
  return {type,ax,av};
}

function pct(v,m){ return Math.max(4,Math.min(100,Math.round(v/m*100))); }

function finish(){
  const r=compute(answers); const d=T[r.type];
  document.getElementById('quiz').classList.add('hide');
  const R=document.getElementById('result'); R.className='res-ct'; R.classList.remove('hide');
  let h='';
  h+='<div class="res-cat">'+d.cat+'</div>';
  h+='<div class="res-name">'+d.name+'</div>';
  h+='<div class="res-one">'+d.oneliner+'</div>';
  h+='<div class="chips">'+d.chips.map(c=>'<span class="chip">'+c+'</span>').join('')+'</div>';
  h+='<div class="block"><h3><b>1</b>组合词拆解</h3>';
  d.combo.forEach(k=>{ h+='<div class="kw"><span class="w">'+k.word+'</span><span class="d">'+k.desc+'</span></div>'; });
  h+='</div>';
  h+='<div class="block"><h3><b>2</b>你的典型表现</h3>';
  for(const k in d.show){ h+='<div class="show-row"><span class="lab">'+k+'</span><span class="val">'+d.show[k]+'</span></div>'; }
  h+='</div>';
  h+='<div class="block"><h3><b>3</b>你的内心独白</h3><div class="mono">“'+d.mono+'”</div></div>';
  h+='<div class="block"><h3><b>4</b>对恋人的影响</h3>';
  h+='<div class="show-row"><span class="lab">好的方面</span><span class="val">'+d.impact.good+'</span></div>';
  h+='<div class="show-row"><span class="lab">容易踩的坑</span><span class="val">'+d.impact.bad+'</span></div>';
  h+='</div>';
  h+='<div class="block"><h3><b>5</b>雷区预警</h3><div class="show-row"><span class="val">'+d.mine+'</span></div></div>';
  h+='<div class="block"><h3><b>6</b>怎么调整自己</h3><div class="show-row"><span class="val">'+d.fix+'</span></div></div>';
  h+='<div class="block"><h3><b>7</b>本周小练习</h3><div class="show-row"><span class="val">'+d.week+'</span></div></div>';
  h+='<div class="block"><h3><b>8</b>最适合的搭档</h3><div class="show-row"><span class="val">'+d.match+'</span></div></div>';
  h+='<div class="axis"><div class="top"><span>你的焦虑指数</span><span>'+pct(r.ax,AX_M)+'%</span></div><div class="track"><i style="width:'+pct(r.ax,AX_M)+'%"></i></div></div>';
  h+='<div class="axis"><div class="top"><span>你的回避指数</span><span>'+pct(r.av,AV_M)+'%</span></div><div class="track"><i style="width:'+pct(r.av,AV_M)+'%"></i></div></div>';
  h+='<p class="tip">把结果分享给另一半，一起聊聊你们的相处模式～</p>';
  h+='<p style="text-align:center;font-size:11px;color:var(--muted);margin:8px 0 0;opacity:.6">本测试为娱乐心理参考，结果不构成专业诊断。</p>';
  h+='<button class="btn" onclick="restart()">重新测一次</button>';
  R.innerHTML=h;
  window.scrollTo(0,0);
}
function restart(){
  answers=new Array(Q.length).fill(-1); cur=0;
  document.getElementById('result').classList.add('hide');
  document.getElementById('quiz').classList.remove('hide'); renderQ();
}
</script>
</body>
</html>
"""

html = HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
with open(os.path.join(OUT,"index.html"),"w",encoding="utf-8") as f:
    f.write(html)
print("index.html written, bytes:", len(html))
