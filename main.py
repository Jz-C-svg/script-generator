"""
鑱旂綉闅忔満鑴氭湰/鏂囨鐢熸垚鍣?APP
鏀寔鑷畾涔夎涓氥€佹櫤鑳藉缓璁€佽嚜鍔ㄧ敓鎴愯剼鏈拰鏂囨
"""

import os
import random
import threading
from datetime import datetime
from typing import Optional

from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.chip import MDChip
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem, MDList

# ============ 鏁版嵁瀹氫箟 ============

INDUSTRIES = [
    "鐢靛晢闆跺敭", "鏁欒偛鍩硅", "閲戣瀺鏈嶅姟", "椁愰ギ缇庨", "鍖荤枟鍋ュ悍",
    "绉戞妧鍒涙柊", "濞变箰浼犲獟", "鏃呮父鍑鸿", "鎴夸骇瀹跺眳", "缇庡鎶よ偆",
    "姣嶅┐鑲插効", "杩愬姩鍋ヨ韩", "姹借溅鍑鸿", "娉曞緥鍜ㄨ", "浜哄姏璧勬簮"
]

SCRIPT_TYPES = [
    "浜у搧浠嬬粛", "娲诲姩淇冮攢", "鍝佺墝鏁呬簨", "浣跨敤鏁欑▼", "瀹㈡埛瑙佽瘉",
    "寮€鍦虹櫧", "缁撴潫璇?, "鑷垜浠嬬粛", "闂瑙ｇ瓟", "鍙峰彫琛屽姩"
]

COPY_TYPES = [
    "骞垮憡璇?, "浜у搧鎻忚堪", "鏈嬪弸鍦堟枃妗?, "鐭棰戞枃妗?, "鐩存挱璇濇湳",
    "娴锋姤鏂囨", "鐭俊钀ラ攢", "閭欢钀ラ攢", "灏忕孩涔︾鑽?, "鍏紬鍙锋帹鏂?
]

# 琛屼笟鐗瑰緛璇嶅簱
INDUSTRY_KEYWORDS = {
    "鐢靛晢闆跺敭": ["闄愭椂浼樻儬", "鐖嗘", "绉掓潃", "婊″噺", "鍖呴偖", "鐖嗘鐑崠", "鏂板搧涓婃灦"],
    "鏁欒偛鍩硅": ["瀛︿範鎶€宸?, "鎻愬垎", "鍚嶅笀鎸囧", "璇剧▼浼樻儬", "鍏嶈垂璇曞惉", "瀛﹂湼鍏绘垚"],
    "閲戣瀺鏈嶅姟": ["绋冲仴鏀剁泭", "浣庨闄?, "涓撲笟鐞嗚储", "璧勯噾瀹夊叏", "鐏垫椿瀛樺彇"],
    "椁愰ギ缇庨": ["缇庡懗鍙彛", "鏂伴矞椋熸潗", "鍖犲績鍒朵綔", "鍦伴亾椋庡懗", "闄愭椂鐗规儬"],
    "鍖荤枟鍋ュ悍": ["涓撲笟鍥㈤槦", "鍋ュ悍绠＄悊", "绉戝璋冪悊", "搴峰鎸囧", "浣撴濂楅"],
    "绉戞妧鍒涙柊": ["鏅鸿兘", "楂樻晥", "鍒涙柊", "鍓嶆部鎶€鏈?, "鏁板瓧鍖栬浆鍨?, "瑙ｅ喅鏂规"],
    "濞变箰浼犲獟": ["绮惧僵绾峰憟", "鏄庢槦鍚屾", "濞变箰鐑偣", "绮変笣绂忓埄", "闄愭椂娲诲姩"],
    "鏃呮父鍑鸿": ["搴﹀亣鑳滃湴", "璇磋蛋灏辫蛋", "绾帺鍥?, "鑷敱琛?, "浜插瓙娓?, "铚滄湀鏃呰"],
    "鎴夸骇瀹跺眳": ["鍝佽川鐢熸椿", "鏅鸿兘瀹跺眳", "鎷庡寘鍏ヤ綇", "榛勯噾鍦版", "鍗楀寳閫氶€?],
    "缇庡鎶よ偆": ["鎶よ偆绉樼睄", "缇庡鏁欑▼", "绱犻濂崇", "閫嗛緞鐢熼暱", "鎴愬垎鍏?],
    "姣嶅┐鑲插効": ["瀹濆疂杈呴", "鑲插効鐭ヨ瘑", "鏃╂暀鍚挋", "浜插瓙浜掑姩", "鍋ュ悍鎴愰暱"],
    "杩愬姩鍋ヨ韩": ["鐕冭剛濉戝舰", "澧炶倢璁粌", "绉戝鍋ヨ韩", "绉佹暀鎸囧", "椹敳绾?],
    "姹借溅鍑鸿": ["鏅鸿兘椹鹃┒", "瀹夊叏鍑鸿", "娌硅€椾綆", "绌洪棿澶?, "鎬т环姣?],
    "娉曞緥鍜ㄨ": ["涓撲笟娉曞姟", "鏉冪泭淇濋殰", "鍚堝悓瀹℃牳", "娉曞緥鍜ㄨ", "缁存潈鏈嶅姟"],
    "浜哄姏璧勬簮": ["浜烘墠鎷涜仒", "鑱屽満鍙戝睍", "鍥㈤槦寤鸿", "缁╂晥绠＄悊", "鍩硅浣撶郴"]
}

# 鑴氭湰妯℃澘搴?SCRIPT_TEMPLATES = {
    "寮€鍦虹櫧": [
        "澶у濂斤紝鎴戞槸{role}锛屼粖澶╃粰澶у鍒嗕韩{topic}銆?,
        "Hello锛屾湅鍙嬩滑濂斤紒娆㈣繋鏉ュ埌{topic}鐨勪笘鐣岋紝鎴戞槸{random_name}銆?,
        "鍚勪綅灏忎紮浼翠滑濂斤紒浠婂ぉ鎴戜滑鏉ヨ亰鑱妠topic}锛屽噯澶囧ソ浜嗗悧锛?
    ],
    "鑷垜浠嬬粛": [
        "鎴戞槸{random_name}锛屼笓娉ㄤ簬{industry}棰嗗煙宸叉湁{random_year}骞淬€?,
        "澶у濂斤紝鎴戞槸{random_name}锛屼竴鍚峽industry}浠庝笟鑰咃紝寰堥珮鍏磋璇嗗ぇ瀹躲€?,
        "鎴戞槸{random_name}锛屽湪{industry}琛屼笟娣辫€曞骞达紝浠婂ぉ涓庡ぇ瀹跺垎浜粡楠屻€?
    ],
    "浜у搧浠嬬粛": [
        "杩欐{product}鏈変粈涔堢壒鍒箣澶勫憿锛熻鎴戞潵涓轰綘涓€涓€鎻檽...",
        "璇村埌{product}锛屽彲鑳藉緢澶氫汉杩樹笉澶簡瑙ｏ紝璁╂垜鏉ヨ缁嗕粙缁嶄竴涓?..",
        "浠婂ぉ瑕佹帹鑽愮殑杩欐{product}锛岀粷瀵逛細璁╀綘鐪煎墠涓€浜紒"
    ],
    "鍙峰彫琛屽姩": [
        "蹇冨姩涓嶅琛屽姩锛岀偣鍑讳笅鏂归摼鎺ョ珛鍗硔random_action}锛?,
        "杩樼瓑浠€涔堝憿锛熻刀绱random_action}锛屽悕棰濇湁闄愶紝鍏堝埌鍏堝緱锛?,
        "鎯宠{random_action}鐨勬湅鍙嬩滑锛岃瘎璁哄尯鎵ｃ€?66銆嶏紝绉佷俊鎴戣幏鍙栬鎯咃紒"
    ]
}

COPY_TEMPLATES = {
    "骞垮憡璇?: [
        "{keyword}锛屽氨閫墈brand}锛?,
        "寮曢{industry}鏂版疆娴侊紝{brand}鏇存噦浣狅紒",
        "鐢▄keyword}锛屼韩{benefit}锛寋brand}璁╃敓娲绘洿缇庡ソ锛?,
        "{keyword}鍝寮猴紵{brand}涓轰綘淇濋┚鎶よ埅锛?,
        "鍛婂埆{keword}鐑︽伡锛寋brand}鍔╀綘杞绘澗{random_action}锛?
    ],
    "浜у搧鎻忚堪": [
        "銆恵product}銆戦噰鐢▄feature}璁捐锛屼笓涓簕user_group}鎵撻€犮€倇benefit}锛岃浣犵殑鐢熸椿鏇磠random_adj}锛?,
        "鏂板搧涓婂競锛亄product}闇囨捈鏉ヨ锛寋feature}锛寋benefit}锛岄檺鏃朵紭鎯犱腑锛?,
        "{product}锛歿feature}锛寋benefit}锛屼笓涓鸿拷姹倇random_adj}鐨勪綘鑰岀敓锛?
    ],
    "鏈嬪弸鍦堟枃妗?: [
        "鍒嗕韩涓€娆捐秴妫掔殑{product}锛寋benefit}锛岀敤浜嗗氨鐖变笂锛亄emoji} #濂界墿鎺ㄨ崘",
        "浠婂ぉ浣撻獙浜唟product}锛寋feeling}锛佸己鐑堟帹鑽愮粰澶у~ {emoji}",
        "{feeling}鐨勪竴澶╋紒鎰熻阿{product}甯︽潵鐨剓random_adj}浣撻獙 {emoji} #鐢熸椿鍒嗕韩"
    ],
    "鐭棰戞枃妗?: [
        "杩欎釜{product}缁濅簡锛亄benefit}锛屼綘缁濆娌¤杩?.. {emoji}",
        "寤鸿鏀惰棌锛佸叧浜巤topic}鐨剓random_adj}鎶€宸э紝鐪嬪畬灏辨噦浜嗭紒",
        "鎻锛亄topic}鐨勫唴骞曪紝99%鐨勪汉閮戒笉鐭ラ亾... {emoji}"
    ]
}

# 寤鸿璇嶅簱
SUGGESTION_TEMPLATES = {
    "寮€澶?: [
        "寤鸿寮€澶村姞鍏ヤ竴涓惛寮曠溂鐞冪殑閽╁瓙锛屾瘮濡傛彁闂垨鎮康",
        "寮€澶村彲浠ュ姞涓€涓暟鎹垨妗堜緥锛屽鍔犲彲淇″害",
        "寤鸿浣跨敤瀵硅瘽寮忓紑澶达紝鎷夎繎涓庤浼楃殑璺濈"
    ],
    "缁撴瀯": [
        "缁撴瀯娓呮櫚锛屼絾寤鸿澧炲姞灏忔爣棰橈紝鏂逛究闃呰",
        "鍙互閲囩敤銆岄棶棰?瑙ｅ喅鏂规銆嶇殑鍙欎簨缁撴瀯",
        "寤鸿鍒嗘鍙欒堪锛屾瘡娈佃仛鐒︿竴涓鐐?
    ],
    "鐢ㄨ瘝": [
        "閮ㄥ垎鐢ㄨ瘝鍙互鏇村彛璇寲锛屽鍔犱翰鍜屽姏",
        "涓撲笟鏈寤鸿閫傚綋瑙ｉ噴锛岄伩鍏嶇悊瑙ｉ殰纰?,
        "鍙互澧炲姞涓€浜涙儏缁瘝锛屽寮烘劅鏌撳姏"
    ],
    "缁撳熬": [
        "缁撳熬鍙峰彫涓嶅寮虹儓锛屽缓璁鍔犳槑纭殑琛屽姩鎸囧紩",
        "鍙互鍔犱竴涓噾鍙ユ垨鎬荤粨锛屽己鍖栧嵃璞?,
        "寤鸿寮曞浜掑姩锛屽璇勮鍖虹暀瑷€鎴栬浆鍙?
    ],
    "鏁翠綋": [
        "鏁翠綋涓嶉敊锛屽缓璁鍔犵湡瀹炴渚嬫垨鐢ㄦ埛鍙嶉",
        "鍙互閫傚綋鍔犲叆emoji鎴栬〃鎯呯鍙凤紝澧炲姞娲诲姏",
        "寤鸿鎺у埗绡囧箙锛岄噸鐐瑰唴瀹瑰墠缃?
    ]
}


# ============ 宸ュ叿鍑芥暟 ============

def random_choice_from_dict(d: dict, key: str) -> str:
    """浠庡瓧鍏镐腑闅忔満閫夋嫨"""
    items = d.get(key, ["鍐呭"])
    return random.choice(items)


def generate_random_text(template: str, **kwargs) -> str:
    """鏍规嵁妯℃澘鐢熸垚闅忔満鏂囨湰"""
    replacements = {
        "{random_name}": random.choice(["灏忔潕", "灏忕帇", "闃挎槑", "闃垮崕", "灏忛洦", "灏忔灄"]),
        "{random_year}": str(random.randint(3, 15)),
        "{random_action}": random.choice(["鎶㈣喘", "浣撻獙", "棰勭害", "鍜ㄨ", "涓嬪崟", "鍙備笌"]),
        "{random_adj}": random.choice(["渚挎嵎", "楂樻晥", "鑸掗€?, "缇庡ソ", "绮惧僵", "瀹岀編"]),
        "{emoji}": random.choice(["馃憤", "馃敟", "馃挴", "鉁?, "鉂わ笍", "馃帀", "馃挭", "馃憦"]),
        "{brand}": kwargs.get("brand", "鎴戜滑鍝佺墝"),
        "{industry}": kwargs.get("industry", "鐩稿叧琛屼笟"),
        "{keyword}": kwargs.get("keyword", "浼樿川"),
        "{benefit}": kwargs.get("benefit", "鍝佽川淇濊瘉"),
        "{product}": kwargs.get("product", "鏈骇鍝?),
        "{topic}": kwargs.get("topic", "鏈湡涓婚"),
        "{feature}": kwargs.get("feature", "鐙壒璁捐"),
        "{user_group}": kwargs.get("user_group", "杩芥眰鍝佽川鐨勪綘"),
        "{feeling}": random.choice(["鍏冩皵婊℃弧", "寮€蹇?, "鍏村", "婊¤冻", "瀹岀編", "骞哥"])
    }
    
    result = template
    for key, value in replacements.items():
        if key in result:
            result = result.replace(key, value)
    
    return result


def generate_random_script(industry: str, script_type: str, topic: str) -> str:
    """鐢熸垚闅忔満鑴氭湰"""
    templates = SCRIPT_TEMPLATES.get(script_type, SCRIPT_TEMPLATES["寮€鍦虹櫧"])
    template = random.choice(templates)
    
    # 鑾峰彇琛屼笟鍏抽敭璇?    keywords = INDUSTRY_KEYWORDS.get(industry, ["浼樿川鍐呭"])
    keyword = random.choice(keywords)
    
    return generate_random_text(
        template,
        industry=industry,
        topic=topic or f"{keyword}鐩稿叧鍐呭",
        keyword=keyword,
        brand=f"{industry}涓撳"
    )


def generate_random_copy(industry: str, copy_type: str, keyword: str = "") -> str:
    """鐢熸垚闅忔満鏂囨"""
    templates = COPY_TEMPLATES.get(copy_type, COPY_TEMPLATES["骞垮憡璇?])
    template = random.choice(templates)
    
    # 鑾峰彇琛屼笟鍏抽敭璇?    industry_keywords = INDUSTRY_KEYWORDS.get(industry, ["浼樿川"])
    selected_keyword = keyword or random.choice(industry_keywords)
    
    return generate_random_text(
        template,
        industry=industry,
        keyword=selected_keyword,
        brand=f"{industry}棣栭€夊搧鐗?
    )


def generate_suggestions(content: str, content_type: str) -> list:
    """鐢熸垚浼樺寲寤鸿"""
    suggestions = []
    
    # 鏍规嵁鍐呭绫诲瀷閫夋嫨寤鸿
    categories = ["寮€澶?, "缁撴瀯", "鐢ㄨ瘝", "缁撳熬", "鏁翠綋"]
    
    # 鏍规嵁鍐呭闀垮害娣诲姞寤鸿
    if len(content) < 50:
        suggestions.append("鍐呭杈冪煭锛屽缓璁鍔犳洿澶氱粏鑺傛弿杩?)
        suggestions.append("鍙互鍔犲叆鍏蜂綋鐨勬渚嬫垨鏁版嵁鏀拺")
    elif len(content) > 300:
        suggestions.append("鍐呭杈冮暱锛屽缓璁垎鎴愬涓钀?)
        suggestions.append("寮€澶村拰缁撳熬鍙互鏇寸簿鐐硷紝閲嶇偣绐佸嚭")
    else:
        suggestions.append(random.choice(SUGGESTION_TEMPLATES["鏁翠綋"]))
    
    # 娣诲姞3-5鏉￠殢鏈哄缓璁?    num_suggestions = min(random.randint(3, 5), len(categories))
    random_categories = random.sample(categories, num_suggestions)
    
    for cat in random_categories:
        suggestions.append(random.choice(SUGGESTION_TEMPLATES[cat]))
    
    return suggestions[:6]


def get_ai_suggestions(content: str) -> str:
    """鑱旂綉鑾峰彇AI浼樺寲寤鸿锛堟ā鎷燂級"""
    # 杩欓噷鍙互鎺ュ叆鐪熷疄鐨凙I API
    # 鐩墠杩斿洖鏈湴鐢熸垚鐨勫缓璁?    suggestions = generate_suggestions(content, "閫氱敤")
    return "\n".join([f"鈥?{s}" for s in suggestions])


# ============ KV鐣岄潰瀹氫箟 ============

KV = """
# 涓诲睆骞曠鐞?ScreenManager:
    id: screen_manager
    
    # 棣栭〉
    HomeScreen:
        name: "home"
        
    # 鑴氭湰鐢熸垚
    ScriptScreen:
        name: "script"
        
    # 鏂囨鐢熸垚
    CopyScreen:
        name: "copy"
        
    # 鍘嗗彶璁板綍
    HistoryScreen:
        name: "history"


# ============ 棣栭〉 ============
<HomeScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"
        
        # 椤堕儴鏍囬
        BoxLayout:
            size_hint_y: None
            height: "100dp"
            orientation: "vertical"
            padding: ["10dp", "20dp", "10dp", "10dp"]
            
            MDLabel:
                text: "馃摑 鑴氭湰鏂囨鐢熸垚鍣?
                font_style: "H4"
                halign: "center"
                theme_text_color: "Primary"
                
            MDLabel:
                text: "鑱旂綉闅忔満鐢熸垚锛屼笓涓氶珮鏁?
                font_style: "Subtitle2"
                halign: "center"
                theme_text_color: "Secondary"
        
        # 鍔熻兘鍗＄墖
        GridLayout:
            cols: 2
            spacing: "16dp"
            padding: "10dp"
            
            # 鑴氭湰鐢熸垚鍗＄墖
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                ripple_effect: True
                on_release: root.go_to_script()
                
                MDIcon:
                    icon: "script-text"
                    icon_size: "48dp"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    
                MDLabel:
                    text: "馃摐 鑴氭湰鐢熸垚"
                    font_style: "Subtitle1"
                    halign: "center"
                    
                MDLabel:
                    text: "闅忔満鐢熸垚鍚勭被瑙嗛/鐩存挱鑴氭湰"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Secondary"
            
            # 鏂囨鐢熸垚鍗＄墖
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                ripple_effect: True
                on_release: root.go_to_copy()
                
                MDIcon:
                    icon: "text-box-multiple"
                    icon_size: "48dp"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    
                MDLabel:
                    text: "鉁嶏笍 鏂囨鐢熸垚"
                    font_style: "Subtitle1"
                    halign: "center"
                    
                MDLabel:
                    text: "涓€閿敓鎴愬惛寮曚汉鐨勮惀閿€鏂囨"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Secondary"
            
            # 琛屼笟璁剧疆鍗＄墖
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                ripple_effect: True
                on_release: root.go_to_settings()
                
                MDIcon:
                    icon: "briefcase-outline"
                    icon_size: "48dp"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.accent_color
                    
                MDLabel:
                    text: "馃彚 琛屼笟璁剧疆"
                    font_style: "Subtitle1"
                    halign: "center"
                    
                MDLabel:
                    text: "鑷畾涔変綘鐨勮涓氱被鍨?
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Secondary"
            
            # 鍘嗗彶璁板綍鍗＄墖
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                ripple_effect: True
                on_release: root.go_to_history()
                
                MDIcon:
                    icon: "history"
                    icon_size: "48dp"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.accent_color
                    
                MDLabel:
                    text: "馃摎 鍘嗗彶璁板綍"
                    font_style: "Subtitle1"
                    halign: "center"
                    
                MDLabel:
                    text: "鏌ョ湅宸茬敓鎴愮殑鍐呭"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Secondary"
        
        # 搴曢儴鎻愮ず
        BoxLayout:
            size_hint_y: None
            height: "60dp"
            
            MDLabel:
                text: "馃挕 鎻愮ず锛氱偣鍑诲崱鐗囧紑濮嬬敓鎴愬唴瀹?
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Hint"


# ============ 鑴氭湰鐢熸垚椤?============
<ScriptScreen>:
    ScrollView:
        do_scroll_x: False
        
        BoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "16dp"
            size_hint_y: None
            height: self.minimum_height
            
            # 椤堕儴瀵艰埅鏍?            BoxLayout:
                size_hint_y: None
                height: "50dp"
                spacing: "10dp"
                
                MDIconButton:
                    icon: "arrow-left"
                    on_release: root.go_back()
                    
                MDLabel:
                    text: "馃摐 鑴氭湰鐢熸垚"
                    font_style: "H5"
                    valign: "middle"
            
            # 琛屼笟閫夋嫨
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                
                MDLabel:
                    text: "閫夋嫨琛屼笟"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "50dp"
                    
                    MDChipList:
                        id: script_industry_chips
                        # 鑺墖灏嗗湪Python涓姩鎬佹坊鍔?            
            # 鑴氭湰绫诲瀷閫夋嫨
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                
                MDLabel:
                    text: "閫夋嫨鑴氭湰绫诲瀷"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "50dp"
                    
                    MDChipList:
                        id: script_type_chips
            
            # 涓婚杈撳叆
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                
                MDLabel:
                    text: "杈撳叆涓婚锛堝彲閫夛級"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                MDTextField:
                    id: script_topic
                    hint_text: "渚嬪锛?18澶т績娲诲姩浠嬬粛"
                    mode: "rectangle"
                    max_text_length: 100
            
            # 鐢熸垚鎸夐挳
            MDRaisedButton:
                text: "馃幉 闅忔満鐢熸垚鑴氭湰"
                on_release: root.generate_script()
                size_hint_x: 1
                height: "56dp"
                pos_hint: {"center_x": 0.5}
            
            # 缁撴灉鏄剧ず鍖?            MDCard:
                id: script_result_card
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                opacity: 0
                
                MDLabel:
                    text: "鐢熸垚缁撴灉"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "200dp"
                    
                    MDLabel:
                        id: script_result_label
                        text: ""
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                
                # 寤鸿鎸夐挳
                MDRaisedButton:
                    text: "馃挕 鑾峰彇浼樺寲寤鸿"
                    on_release: root.get_suggestions()
                    size_hint_x: 1
                    height: "48dp"
                    md_bg_color: app.theme_cls.accent_color
                    opacity: 0 if script_result_card.opacity == 0 else 1
            
            # 寤鸿鏄剧ず鍖?            MDCard:
                id: script_suggestion_card
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                opacity: 0
                
                MDLabel:
                    text: "馃挕 浼樺寲寤鸿"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "150dp"
                    
                    MDLabel:
                        id: script_suggestion_label
                        text: ""
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
            
            # 闂磋窛
            BoxLayout:
                size_hint_y: None
                height: "30dp"


# ============ 鏂囨鐢熸垚椤?============
<CopyScreen>:
    ScrollView:
        do_scroll_x: False
        
        BoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "16dp"
            size_hint_y: None
            height: self.minimum_height
            
            # 椤堕儴瀵艰埅鏍?            BoxLayout:
                size_hint_y: None
                height: "50dp"
                spacing: "10dp"
                
                MDIconButton:
                    icon: "arrow-left"
                    on_release: root.go_back()
                    
                MDLabel:
                    text: "鉁嶏笍 鏂囨鐢熸垚"
                    font_style: "H5"
                    valign: "middle"
            
            # 琛屼笟閫夋嫨
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                
                MDLabel:
                    text: "閫夋嫨琛屼笟"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "50dp"
                    
                    MDChipList:
                        id: copy_industry_chips
            
            # 鏂囨绫诲瀷閫夋嫨
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                
                MDLabel:
                    text: "閫夋嫨鏂囨绫诲瀷"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "50dp"
                    
                    MDChipList:
                        id: copy_type_chips
            
            # 鍏抽敭璇嶈緭鍏?            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                
                MDLabel:
                    text: "杈撳叆鍏抽敭璇嶏紙鍙€夛級"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                MDTextField:
                    id: copy_keyword
                    hint_text: "渚嬪锛氶檺鏃朵紭鎯犮€佹柊鍝佷笂甯?
                    mode: "rectangle"
                    max_text_length: 50
            
            # 鐢熸垚鎸夐挳
            MDRaisedButton:
                text: "馃幉 闅忔満鐢熸垚鏂囨"
                on_release: root.generate_copy()
                size_hint_x: 1
                height: "56dp"
                pos_hint: {"center_x": 0.5}
            
            # 缁撴灉鏄剧ず鍖?            MDCard:
                id: copy_result_card
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                opacity: 0
                
                MDLabel:
                    text: "鐢熸垚缁撴灉"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "150dp"
                    
                    MDLabel:
                        id: copy_result_label
                        text: ""
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
                
                # 寤鸿鎸夐挳
                MDRaisedButton:
                    text: "馃挕 鑾峰彇浼樺寲寤鸿"
                    on_release: root.get_suggestions()
                    size_hint_x: 1
                    height: "48dp"
                    md_bg_color: app.theme_cls.accent_color
                    opacity: 0 if copy_result_card.opacity == 0 else 1
            
            # 寤鸿鏄剧ず鍖?            MDCard:
                id: copy_suggestion_card
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                opacity: 0
                
                MDLabel:
                    text: "馃挕 浼樺寲寤鸿"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"
                    
                ScrollView:
                    do_scroll_x: False
                    size_hint_y: None
                    height: "120dp"
                    
                    MDLabel:
                        id: copy_suggestion_label
                        text: ""
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]
            
            # 闂磋窛
            BoxLayout:
                size_hint_y: None
                height: "30dp"


# ============ 鍘嗗彶璁板綍椤?============
<HistoryScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        
        # 椤堕儴瀵艰埅鏍?        BoxLayout:
            size_hint_y: None
            height: "50dp"
            spacing: "10dp"
            
            MDIconButton:
                icon: "arrow-left"
                on_release: root.go_back()
                
            MDLabel:
                text: "馃摎 鍘嗗彶璁板綍"
                font_style: "H5"
                valign: "middle"
            
            MDIconButton:
                icon: "delete-sweep"
                on_release: root.clear_history()
                pos_hint: {"right": 1}
        
        # 鍘嗗彶鍒楄〃
        ScrollView:
            do_scroll_x: False
            
            MDList:
                id: history_list
        
        # 绌虹姸鎬佹彁绀?        MDLabel:
            id: empty_label
            text: "鏆傛棤鍘嗗彶璁板綍\n鐢熸垚鍐呭鍚庝細鑷姩淇濆瓨"
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Secondary"
            opacity: 1
"""


# ============ 灞忓箷瀹氫箟 ============

class HomeScreen(MDScreen):
    """棣栭〉"""
    def go_to_script(self):
        self.manager.get_screen("script").refresh_chips()
        self.manager.current = "script"
    
    def go_to_copy(self):
        self.manager.get_screen("copy").refresh_chips()
        self.manager.current = "copy"
    
    def go_to_history(self):
        self.manager.get_screen("history").load_history()
        self.manager.current = "history"
    
    def go_to_settings(self):
        # 璺宠浆鍒拌剼鏈〉闈㈣缃涓?        self.manager.get_screen("script").refresh_chips()
        self.manager.current = "script"


class ScriptScreen(MDScreen):
    """鑴氭湰鐢熸垚椤?""
    
    def refresh_chips(self):
        """鍒锋柊琛屼笟鍜岀被鍨嬮€夋嫨"""
        from kivymd.uix.chip import MDChip
        
        # 娓呯┖骞舵坊鍔犺涓氳姱鐗?        self.ids.script_industry_chips.clear_widgets()
        for industry in INDUSTRIES[:8]:  # 鍙樉绀哄墠8涓?            chip = MDChip(
                text=industry,
                on_release=self.on_industry_selected
            )
            self.ids.script_industry_chips.add_widget(chip)
        
        # 榛樿閫変腑绗竴涓?        if self.ids.script_industry_chips.children:
            self.ids.script_industry_chips.children[-1].selected = True
        
        # 娓呯┖骞舵坊鍔犵被鍨嬭姱鐗?        self.ids.script_type_chips.clear_widgets()
        for stype in SCRIPT_TYPES[:6]:
            chip = MDChip(
                text=stype,
                on_release=self.on_type_selected
            )
            self.ids.script_type_chips.add_widget(chip)
        
        # 榛樿閫変腑绗竴涓?        if self.ids.script_type_chips.children:
            self.ids.script_type_chips.children[-1].selected = True
        
        # 閲嶇疆缁撴灉鍖?        self.ids.script_result_card.opacity = 0
        self.ids.script_suggestion_card.opacity = 0
    
    def on_industry_selected(self, chip):
        """琛屼笟閫変腑鍥炶皟"""
        # 鍙栨秷鍏朵粬閫変腑
        for c in self.ids.script_industry_chips.children:
            if c != chip:
                c.selected = False
        chip.selected = True
    
    def on_type_selected(self, chip):
        """绫诲瀷閫変腑鍥炶皟"""
        for c in self.ids.script_type_chips.children:
            if c != chip:
                c.selected = False
        chip.selected = True
    
    def get_selected_industry(self):
        """鑾峰彇閫変腑鐨勮涓?""
        for chip in self.ids.script_industry_chips.children:
            if chip.selected:
                return chip.text
        return INDUSTRIES[0]
    
    def get_selected_type(self):
        """鑾峰彇閫変腑鐨勭被鍨?""
        for chip in self.ids.script_type_chips.children:
            if chip.selected:
                return chip.text
        return SCRIPT_TYPES[0]
    
    def generate_script(self):
        """鐢熸垚鑴氭湰"""
        industry = self.get_selected_industry()
        script_type = self.get_selected_type()
        topic = self.ids.script_topic.text.strip()
        
        # 鐢熸垚鑴氭湰
        script = generate_random_script(industry, script_type, topic)
        
        # 鏄剧ず缁撴灉
        self.ids.script_result_label.text = script
        self.ids.script_result_card.opacity = 1
        
        # 闅愯棌寤鸿鍖?        self.ids.script_suggestion_card.opacity = 0
        
        # 淇濆瓨鍒板巻鍙?        self.save_to_history(script, "鑴氭湰", industry, script_type)
        
        # 鏄剧ず鎻愮ず
        Snackbar(text="鉁?鑴氭湰鐢熸垚鎴愬姛锛?).open()
    
    def get_suggestions(self):
        """鑾峰彇浼樺寲寤鸿"""
        content = self.ids.script_result_label.text
        if not content:
            Snackbar(text="璇峰厛鐢熸垚鍐呭").open()
            return
        
        # 鐢熸垚寤鸿
        suggestions = generate_suggestions(content, "鑴氭湰")
        suggestion_text = "\n".join([f"鈥?{s}" for s in suggestions])
        
        self.ids.script_suggestion_label.text = suggestion_text
        self.ids.script_suggestion_card.opacity = 1
    
    def save_to_history(self, content, content_type, industry, sub_type):
        """淇濆瓨鍒板巻鍙茶褰?""
        app = MDApp.get_running_app()
        record = {
            "type": content_type,
            "industry": industry,
            "sub_type": sub_type,
            "content": content,
            "time": datetime.now().strftime("%H:%M")
        }
        app.history.insert(0, record)
        # 鍙繚鐣欐渶杩?0鏉?        app.history = app.history[:20]
    
    def go_back(self):
        self.manager.current = "home"


class CopyScreen(MDScreen):
    """鏂囨鐢熸垚椤?""
    
    def refresh_chips(self):
        """鍒锋柊閫夋嫨"""
        from kivymd.uix.chip import MDChip
        
        # 娓呯┖骞舵坊鍔犺涓氳姱鐗?        self.ids.copy_industry_chips.clear_widgets()
        for industry in INDUSTRIES[:8]:
            chip = MDChip(
                text=industry,
                on_release=self.on_industry_selected
            )
            self.ids.copy_industry_chips.add_widget(chip)
        
        if self.ids.copy_industry_chips.children:
            self.ids.copy_industry_chips.children[-1].selected = True
        
        # 娓呯┖骞舵坊鍔犳枃妗堢被鍨嬭姱鐗?        self.ids.copy_type_chips.clear_widgets()
        for ctype in COPY_TYPES[:6]:
            chip = MDChip(
                text=ctype,
                on_release=self.on_type_selected
            )
            self.ids.copy_type_chips.add_widget(chip)
        
        if self.ids.copy_type_chips.children:
            self.ids.copy_type_chips.children[-1].selected = True
        
        # 閲嶇疆缁撴灉鍖?        self.ids.copy_result_card.opacity = 0
        self.ids.copy_suggestion_card.opacity = 0
    
    def on_industry_selected(self, chip):
        for c in self.ids.copy_industry_chips.children:
            if c != chip:
                c.selected = False
        chip.selected = True
    
    def on_type_selected(self, chip):
        for c in self.ids.copy_type_chips.children:
            if c != chip:
                c.selected = False
        chip.selected = True
    
    def get_selected_industry(self):
        for chip in self.ids.copy_industry_chips.children:
            if chip.selected:
                return chip.text
        return INDUSTRIES[0]
    
    def get_selected_type(self):
        for chip in self.ids.copy_type_chips.children:
            if chip.selected:
                return chip.text
        return COPY_TYPES[0]
    
    def generate_copy(self):
        """鐢熸垚鏂囨"""
        industry = self.get_selected_industry()
        copy_type = self.get_selected_type()
        keyword = self.ids.copy_keyword.text.strip()
        
        # 鐢熸垚鏂囨
        copy_text = generate_random_copy(industry, copy_type, keyword)
        
        # 鏄剧ず缁撴灉
        self.ids.copy_result_label.text = copy_text
        self.ids.copy_result_card.opacity = 1
        
        # 闅愯棌寤鸿鍖?        self.ids.copy_suggestion_card.opacity = 0
        
        # 淇濆瓨鍒板巻鍙?        self.save_to_history(copy_text, "鏂囨", industry, copy_type)
        
        Snackbar(text="鉁?鏂囨鐢熸垚鎴愬姛锛?).open()
    
    def get_suggestions(self):
        content = self.ids.copy_result_label.text
        if not content:
            Snackbar(text="璇峰厛鐢熸垚鍐呭").open()
            return
        
        suggestions = generate_suggestions(content, "鏂囨")
        suggestion_text = "\n".join([f"鈥?{s}" for s in suggestions])
        
        self.ids.copy_suggestion_label.text = suggestion_text
        self.ids.copy_suggestion_card.opacity = 1
    
    def save_to_history(self, content, content_type, industry, sub_type):
        app = MDApp.get_running_app()
        record = {
            "type": content_type,
            "industry": industry,
            "sub_type": sub_type,
            "content": content,
            "time": datetime.now().strftime("%H:%M")
        }
        app.history.insert(0, record)
        app.history = app.history[:20]
    
    def go_back(self):
        self.manager.current = "home"


class HistoryScreen(MDScreen):
    """鍘嗗彶璁板綍椤?""
    
    def load_history(self):
        """鍔犺浇鍘嗗彶璁板綍"""
        app = MDApp.get_running_app()
        self.ids.history_list.clear_widgets()
        
        if not app.history:
            self.ids.empty_label.opacity = 1
            return
        
        self.ids.empty_label.opacity = 0
        
        for record in app.history:
            item = OneLineListItem(
                text=f"[{record['time']}] {record['type']} - {record['industry']} - {record['sub_type']}",
                secondary_text=record['content'][:50] + "..." if len(record['content']) > 50 else record['content'],
                on_release=lambda x, r=record: self.show_detail(r)
            )
            self.ids.history_list.add_widget(item)
    
    def show_detail(self, record):
        """鏄剧ず璇︽儏"""
        dialog = MDDialog(
            title=f"{record['type']}璇︽儏",
            text=f"绫诲瀷锛歿record['type']}\n琛屼笟锛歿record['industry']}\n瀛愮被鍨嬶細{record['sub_type']}\n鏃堕棿锛歿record['time']}\n\n鍐呭锛歕n{record['content']}",
            buttons=[
                MDFlatButton(text="鍏抽棴", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
    
    def clear_history(self):
        """娓呯┖鍘嗗彶"""
        app = MDApp.get_running_app()
        app.history = []
        self.load_history()
        Snackbar(text="鍘嗗彶璁板綍宸叉竻绌?).open()
    
    def go_back(self):
        self.manager.current = "home"


# ============ APP涓荤被 ============

class ScriptGeneratorApp(MDApp):
    """鑴氭湰鏂囨鐢熸垚鍣ˋPP"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []  # 鍘嗗彶璁板綍
        self.title = "鑴氭湰鏂囨鐢熸垚鍣?
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Teal"
    
    def build(self):
        # 鍔犺浇KV鐣岄潰
        Builder.load_string(KV)
        
        # 鍒涘缓灞忓箷绠＄悊鍣?        sm = MDScreenManager()
        
        # 娣诲姞灞忓箷
        home = HomeScreen(name="home")
        script = ScriptScreen(name="script")
        copy = CopyScreen(name="copy")
        history = HistoryScreen(name="history")
        
        sm.add_widget(home)
        sm.add_widget(script)
        sm.add_widget(copy)
        sm.add_widget(history)
        
        return sm


# ============ 鍏ュ彛 ============

if __name__ == "__main__":
    ScriptGeneratorApp().run()
