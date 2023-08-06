import ast
import unicodedata
from random import choice


def to_utf8(code: str) -> str:
    visitor = _Visitor(fw=False)
    return _action(code, visitor)


def to_unicode(code: str) -> str:
    visitor = _Visitor()
    return _action(code, visitor)


def _action(code: str, visitor: ast.NodeVisitor) -> str:
    tree = ast.parse(code)
    visitor.visit(tree)
    return ast.unparse(tree)


class _Visitor(ast.NodeVisitor):
    def __init__(self, fw=True) -> None:
        super().__init__()
        self._action = _Visitor._fw_action if fw else _Visitor._bw_action

    @staticmethod
    def _fw_action(v: str) -> str:
        return ''.join([_put(i) for i in v])

    @staticmethod
    def _bw_action(v: str) -> str:
        return unicodedata.normalize('NFKC', v)

    def visit_Name(self, node):
        node.id = self._action(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.name = self._action(node.name)
        for arg in node.args.args:
            arg.arg = self._action(arg.arg)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = self._action(node.name)
        self.generic_visit(node)


def _put(token: str) -> str:
    val = UNICODE_MAP.get(token)
    return choice(val) if val else token


UNICODE_MAP: dict[str, str] = {
    "0": "0０𝟎𝟘𝟢𝟬𝟶🯰",
    "1": "1１𝟏𝟙𝟣𝟭𝟷🯱",
    "2": "2２𝟐𝟚𝟤𝟮𝟸🯲",
    "3": "3３𝟑𝟛𝟥𝟯𝟹🯳",
    "4": "4４𝟒𝟜𝟦𝟰𝟺🯴",
    "5": "5５𝟓𝟝𝟧𝟱𝟻🯵",
    "6": "6６𝟔𝟞𝟨𝟲𝟼🯶",
    "7": "7７𝟕𝟟𝟩𝟳𝟽🯷",
    "8": "8８𝟖𝟠𝟪𝟴𝟾🯸",
    "9": "9９𝟗𝟡𝟫𝟵𝟿🯹",
    "a": "aªᵃₐａ𝐚𝑎𝒂𝒶𝓪𝔞𝕒𝖆𝖺𝗮𝘢𝙖𝚊",
    "b": "bᵇｂ𝐛𝑏𝒃𝒷𝓫𝔟𝕓𝖇𝖻𝗯𝘣𝙗𝚋",
    "c": "cᶜⅽｃ𝐜𝑐𝒄𝒸𝓬𝔠𝕔𝖈𝖼𝗰𝘤𝙘𝚌",
    "d": "dᵈⅆⅾｄ𝐝𝑑𝒅𝒹𝓭𝔡𝕕𝖉𝖽𝗱𝘥𝙙𝚍",
    "e": "eᵉₑℯⅇｅ𝐞𝑒𝒆𝓮𝔢𝕖𝖊𝖾𝗲𝘦𝙚𝚎",
    "f": "fᶠｆ𝐟𝑓𝒇𝒻𝓯𝔣𝕗𝖋𝖿𝗳𝘧𝙛𝚏",
    "g": "gᵍℊｇ𝐠𝑔𝒈𝓰𝔤𝕘𝖌𝗀𝗴𝘨𝙜𝚐",
    "h": "hʰₕℎｈ𝐡𝒉𝒽𝓱𝔥𝕙𝖍𝗁𝗵𝘩𝙝𝚑",
    "i": "iᵢⁱℹⅈⅰｉ𝐢𝑖𝒊𝒾𝓲𝔦𝕚𝖎𝗂𝗶𝘪𝙞𝚒",
    "j": "jʲⅉⱼｊ𝐣𝑗𝒋𝒿𝓳𝔧𝕛𝖏𝗃𝗷𝘫𝙟𝚓",
    "k": "kᵏₖｋ𝐤𝑘𝒌𝓀𝓴𝔨𝕜𝖐𝗄𝗸𝘬𝙠𝚔",
    "l": "lˡₗℓⅼｌ𝐥𝑙𝒍𝓁𝓵𝔩𝕝𝖑𝗅𝗹𝘭𝙡𝚕",
    "m": "mᵐₘⅿｍ𝐦𝑚𝒎𝓂𝓶𝔪𝕞𝖒𝗆𝗺𝘮𝙢𝚖",
    "n": "nⁿₙｎ𝐧𝑛𝒏𝓃𝓷𝔫𝕟𝖓𝗇𝗻𝘯𝙣𝚗",
    "o": "oºᵒₒℴｏ𝐨𝑜𝒐𝓸𝔬𝕠𝖔𝗈𝗼𝘰𝙤𝚘",
    "p": "pᵖₚｐ𝐩𝑝𝒑𝓅𝓹𝔭𝕡𝖕𝗉𝗽𝘱𝙥𝚙",
    "q": "qｑ𝐪𝑞𝒒𝓆𝓺𝔮𝕢𝖖𝗊𝗾𝘲𝙦𝚚",
    "r": "rʳᵣｒ𝐫𝑟𝒓𝓇𝓻𝔯𝕣𝖗𝗋𝗿𝘳𝙧𝚛",
    "s": "sſˢₛｓ𝐬𝑠𝒔𝓈𝓼𝔰𝕤𝖘𝗌𝘀𝘴𝙨𝚜",
    "t": "tᵗₜｔ𝐭𝑡𝒕𝓉𝓽𝔱𝕥𝖙𝗍𝘁𝘵𝙩𝚝",
    "u": "uᵘᵤｕ𝐮𝑢𝒖𝓊𝓾𝔲𝕦𝖚𝗎𝘂𝘶𝙪𝚞",
    "v": "vᵛᵥⅴｖ𝐯𝑣𝒗𝓋𝓿𝔳𝕧𝖛𝗏𝘃𝘷𝙫𝚟",
    "w": "wʷｗ𝐰𝑤𝒘𝓌𝔀𝔴𝕨𝖜𝗐𝘄𝘸𝙬𝚠",
    "x": "xˣₓⅹｘ𝐱𝑥𝒙𝓍𝔁𝔵𝕩𝖝𝗑𝘅𝘹𝙭𝚡",
    "y": "yʸｙ𝐲𝑦𝒚𝓎𝔂𝔶𝕪𝖞𝗒𝘆𝘺𝙮𝚢",
    "z": "zᶻｚ𝐳𝑧𝒛𝓏𝔃𝔷𝕫𝖟𝗓𝘇𝘻𝙯𝚣",
    "A": "AᴬＡ𝐀𝐴𝑨𝒜𝓐𝔄𝔸𝕬𝖠𝗔𝘈𝘼𝙰",
    "B": "BᴮℬＢ𝐁𝐵𝑩𝓑𝔅𝔹𝕭𝖡𝗕𝘉𝘽𝙱",
    "C": "CℂℭⅭＣ𝐂𝐶𝑪𝒞𝓒𝕮𝖢𝗖𝘊𝘾𝙲",
    "D": "DᴰⅅⅮＤ𝐃𝐷𝑫𝒟𝓓𝔇𝔻𝕯𝖣𝗗𝘋𝘿𝙳",
    "E": "EᴱℰＥ𝐄𝐸𝑬𝓔𝔈𝔼𝕰𝖤𝗘𝘌𝙀𝙴",
    "F": "FℱＦ𝐅𝐹𝑭𝓕𝔉𝔽𝕱𝖥𝗙𝘍𝙁𝙵",
    "G": "GᴳＧ𝐆𝐺𝑮𝒢𝓖𝔊𝔾𝕲𝖦𝗚𝘎𝙂𝙶",
    "H": "HᴴℋℌℍＨ𝐇𝐻𝑯𝓗𝕳𝖧𝗛𝘏𝙃𝙷",
    "I": "IᴵℐℑⅠＩ𝐈𝐼𝑰𝓘𝕀𝕴𝖨𝗜𝘐𝙄𝙸",
    "J": "JᴶＪ𝐉𝐽𝑱𝒥𝓙𝔍𝕁𝕵𝖩𝗝𝘑𝙅𝙹",
    "K": "KᴷKＫ𝐊𝐾𝑲𝒦𝓚𝔎𝕂𝕶𝖪𝗞𝘒𝙆𝙺",
    "L": "LᴸℒⅬＬ𝐋𝐿𝑳𝓛𝔏𝕃𝕷𝖫𝗟𝘓𝙇𝙻",
    "M": "MᴹℳⅯＭ𝐌𝑀𝑴𝓜𝔐𝕄𝕸𝖬𝗠𝘔𝙈𝙼",
    "N": "NᴺℕＮ𝐍𝑁𝑵𝒩𝓝𝔑𝕹𝖭𝗡𝘕𝙉𝙽",
    "O": "OᴼＯ𝐎𝑂𝑶𝒪𝓞𝔒𝕆𝕺𝖮𝗢𝘖𝙊𝙾",
    "P": "PᴾℙＰ𝐏𝑃𝑷𝒫𝓟𝔓𝕻𝖯𝗣𝘗𝙋𝙿",
    "Q": "QℚＱ𝐐𝑄𝑸𝒬𝓠𝔔𝕼𝖰𝗤𝘘𝙌𝚀",
    "R": "RᴿℛℜℝＲ𝐑𝑅𝑹𝓡𝕽𝖱𝗥𝘙𝙍𝚁",
    "S": "SＳ𝐒𝑆𝑺𝒮𝓢𝔖𝕊𝕾𝖲𝗦𝘚𝙎𝚂",
    "T": "TᵀＴ𝐓𝑇𝑻𝒯𝓣𝔗𝕋𝕿𝖳𝗧𝘛𝙏𝚃",
    "U": "UᵁＵ𝐔𝑈𝑼𝒰𝓤𝔘𝕌𝖀𝖴𝗨𝘜𝙐𝚄",
    "V": "VⅤⱽＶ𝐕𝑉𝑽𝒱𝓥𝔙𝕍𝖁𝖵𝗩𝘝𝙑𝚅",
    "W": "WᵂＷ𝐖𝑊𝑾𝒲𝓦𝔚𝕎𝖂𝖶𝗪𝘞𝙒𝚆",
    "X": "XⅩＸ𝐗𝑋𝑿𝒳𝓧𝔛𝕏𝖃𝖷𝗫𝘟𝙓𝚇",
    "Y": "YＹ𝐘𝑌𝒀𝒴𝓨𝔜𝕐𝖄𝖸𝗬𝘠𝙔𝚈",
    "Z": "ZℤℨＺ𝐙𝑍𝒁𝒵𝓩𝖅𝖹𝗭𝘡𝙕𝚉"
}
