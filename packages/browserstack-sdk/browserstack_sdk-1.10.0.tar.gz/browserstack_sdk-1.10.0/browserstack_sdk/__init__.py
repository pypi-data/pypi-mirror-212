# coding: UTF-8
import sys
bstack11_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack1ll1_opy_ = 7
def bstackl_opy_ (bstack1l_opy_):
    global bstack1ll_opy_
    stringNr = ord (bstack1l_opy_ [-1])
    bstack1l1_opy_ = bstack1l_opy_ [:-1]
    bstack1lll_opy_ = stringNr % len (bstack1l1_opy_)
    bstack11l_opy_ = bstack1l1_opy_ [:bstack1lll_opy_] + bstack1l1_opy_ [bstack1lll_opy_:]
    if bstack11_opy_:
        bstack1l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack111_opy_ + stringNr) % bstack1ll1_opy_) for bstack111_opy_, char in enumerate (bstack11l_opy_)])
    else:
        bstack1l1l_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack111_opy_ + stringNr) % bstack1ll1_opy_) for bstack111_opy_, char in enumerate (bstack11l_opy_)])
    return eval (bstack1l1l_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l11l11ll_opy_ = {
	bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstackl_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstackl_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstackl_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstackl_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstackl_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstackl_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstackl_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstackl_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstackl_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstackl_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstackl_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstackl_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstackl_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack1ll1l11ll_opy_ = [
  bstackl_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstackl_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstackl_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l1111l11_opy_ = {
  bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1ll1lll1l_opy_ = {
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstackl_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1l11l11l1_opy_ = {
  bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstackl_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstackl_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstackl_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstackl_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1ll1ll1ll_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstackl_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstackl_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstackl_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack1lll1llll_opy_ = [
  bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstackl_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1lllll1ll_opy_ = [
  bstackl_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstackl_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstackl_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstackl_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstackl_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstackl_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstackl_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstackl_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstackl_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstackl_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstackl_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstackl_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstackl_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstackl_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstackl_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstackl_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstackl_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstackl_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstackl_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstackl_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstackl_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstackl_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstackl_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstackl_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstackl_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstackl_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstackl_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstackl_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstackl_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstackl_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstackl_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstackl_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstackl_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstackl_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstackl_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstackl_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstackl_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstackl_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstackl_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstackl_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstackl_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstackl_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstackl_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstackl_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstackl_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstackl_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstackl_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1l11l1l11_opy_ = {
  bstackl_opy_ (u"࠭ࡶࠨच"): bstackl_opy_ (u"ࠧࡷࠩछ"),
  bstackl_opy_ (u"ࠨࡨࠪज"): bstackl_opy_ (u"ࠩࡩࠫझ"),
  bstackl_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstackl_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstackl_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstackl_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstackl_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstackl_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstackl_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstackl_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstackl_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstackl_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstackl_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstackl_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstackl_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstackl_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstackl_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstackl_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstackl_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstackl_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstackl_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstackl_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstackl_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1ll11ll11_opy_ = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1lll1ll_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack111111_opy_ = bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1ll1ll11l_opy_ = {
  bstackl_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstackl_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstackl_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstackl_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1l11l1ll1_opy_ = bstack1ll1ll11l_opy_[bstackl_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack11l111l1_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1l1lll_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l1l1_opy_ = bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1ll1ll1_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1ll1111ll_opy_ = [bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1l111_opy_ = [bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1l1111ll1_opy_ = [
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstackl_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstackl_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstackl_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstackl_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstackl_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstackl_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstackl_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstackl_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstackl_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstackl_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstackl_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstackl_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstackl_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstackl_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstackl_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstackl_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstackl_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstackl_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstackl_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstackl_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstackl_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstackl_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstackl_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstackl_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstackl_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstackl_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstackl_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstackl_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstackl_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstackl_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstackl_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstackl_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstackl_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstackl_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstackl_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstackl_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstackl_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstackl_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstackl_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstackl_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstackl_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstackl_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstackl_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstackl_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstackl_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstackl_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstackl_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstackl_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstackl_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstackl_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstackl_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstackl_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstackl_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstackl_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstackl_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstackl_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstackl_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstackl_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstackl_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstackl_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstackl_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstackl_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstackl_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstackl_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstackl_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstackl_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstackl_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstackl_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstackl_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstackl_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstackl_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstackl_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstackl_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstackl_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstackl_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstackl_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstackl_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstackl_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstackl_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstackl_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstackl_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstackl_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1l111ll1_opy_ = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1lll1l111_opy_ = [bstackl_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstackl_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstackl_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack111lll11_opy_ = [bstackl_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstackl_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1111111l_opy_ = {
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstackl_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstackl_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstackl_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1l1lll1ll_opy_ = [
  bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstackl_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1lllll1l1_opy_ = bstack1lll1llll_opy_ + bstack1lllll1ll_opy_ + bstack1l1111ll1_opy_
bstack1l1l111ll_opy_ = [
  bstackl_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstackl_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstackl_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstackl_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstackl_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstackl_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstackl_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstackl_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1l1111l1_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1ll1l11_opy_ = bstackl_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack1111ll1_opy_ = [ bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack111ll11_opy_ = [ bstackl_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack11llll11_opy_ = [ bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack1111l1ll_opy_ = bstackl_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1l1111ll_opy_ = bstackl_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack1l1ll1l11_opy_ = bstackl_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack11ll1l11_opy_ = bstackl_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1ll11ll_opy_ = [
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
def bstack1l1lll111_opy_():
  global CONFIG
  headers = {
        bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਧ"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਨ"),
      }
  proxy = bstack1ll111_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ਩")) or CONFIG.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩਪ")):
    proxies = {
      bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬਫ"): proxy
    }
  try:
    response = requests.get(bstack111111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l1111_opy_ = response.json()[bstackl_opy_ (u"ࠧࡩࡷࡥࡷࠬਬ")]
      logger.debug(bstack1lll1l1_opy_.format(response.json()))
      return bstack11l1111_opy_
    else:
      logger.debug(bstack11l1111l_opy_.format(bstackl_opy_ (u"ࠣࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡫ࠠࡦࡴࡵࡳࡷࠦࠢਭ")))
  except Exception as e:
    logger.debug(bstack11l1111l_opy_.format(e))
def bstack11l1lll1_opy_(hub_url):
  global CONFIG
  url = bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦਮ")+  hub_url + bstackl_opy_ (u"ࠥ࠳ࡨ࡮ࡥࡤ࡭ࠥਯ")
  headers = {
        bstackl_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪਰ"): bstackl_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ਱"),
      }
  proxy = bstack1ll111_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩਲ")) or CONFIG.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫਲ਼")):
    proxies = {
      bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ਴"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1lll1l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111ll1_opy_.format(hub_url, e))
def bstack11l1ll1l_opy_():
  try:
    global bstack1l1111l1l_opy_
    bstack11l1111_opy_ = bstack1l1lll111_opy_()
    with Pool() as pool:
      results = pool.map(bstack11l1lll1_opy_, bstack11l1111_opy_)
    bstack1llllll_opy_ = {}
    for item in results:
      hub_url = item[bstackl_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪਵ")]
      latency = item[bstackl_opy_ (u"ࠪࡰࡦࡺࡥ࡯ࡥࡼࠫਸ਼")]
      bstack1llllll_opy_[hub_url] = latency
    bstack1lll1l11_opy_ = min(bstack1llllll_opy_, key= lambda x: bstack1llllll_opy_[x])
    bstack1l1111l1l_opy_ = bstack1lll1l11_opy_
    logger.debug(bstack1llllll1l_opy_.format(bstack1lll1l11_opy_))
  except Exception as e:
    logger.debug(bstack11ll1_opy_.format(e))
bstack1lllll1l_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠰ࠥࡻࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࡽࢀࠫ਷")
bstack1l11ll111_opy_ = bstackl_opy_ (u"ࠬࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡨࡸࡺࡶࠡࠨਸ")
bstack11111111_opy_ = bstackl_opy_ (u"࠭ࡐࡢࡴࡶࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਹ")
bstack1lll111_opy_ = bstackl_opy_ (u"ࠧࡔࡣࡱ࡭ࡹ࡯ࡺࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬ਺")
bstack1ll1lll_opy_ = bstackl_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡩࡷࡥࠤࡺࡸ࡬࠻ࠢࡾࢁࠬ਻")
bstack1l11l1ll_opy_ = bstackl_opy_ (u"ࠩࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࡻࡾ਼ࠩ")
bstack1l11_opy_ = bstackl_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥ࡯࡮ࡵࡧࡵࡶࡺࡶࡴ࠭ࠢࡨࡼ࡮ࡺࡩ࡯ࡩࠪ਽")
bstack111ll1ll_opy_ = bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩਾ")
bstack11l111l_opy_ = bstackl_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack1ll1ll11_opy_ = bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࠲ࠠࡱࡣࡥࡳࡹࠦࡡ࡯ࡦࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡵࡱࠣࡶࡺࡴࠠࡳࡱࡥࡳࡹࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡶࡡࡣࡱࡷࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࡠࠨੀ")
bstack1l1l1l11l_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࡠࠨੁ")
bstack1l1llll1l_opy_ = bstackl_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡤࡴࡵ࡯ࡵ࡮࠯ࡦࡰ࡮࡫࡮ࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡃࡳࡴ࡮ࡻ࡭࠮ࡒࡼࡸ࡭ࡵ࡮࠮ࡅ࡯࡭ࡪࡴࡴࡡࠩੂ")
bstack1111ll11_opy_ = bstackl_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡣࠫ੃")
bstack1lll11lll_opy_ = bstackl_opy_ (u"ࠪࡌࡦࡴࡤ࡭࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣ࡭ࡱࡶࡩࠬ੄")
bstack1ll111ll_opy_ = bstackl_opy_ (u"ࠫࡆࡲ࡬ࠡࡦࡲࡲࡪࠧࠧ੅")
bstack11l11l_opy_ = bstackl_opy_ (u"ࠬࡉ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࠤࡦࡺࠠࡢࡰࡼࠤࡵࡧࡲࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡰࡨࠣࠦࢀࢃࠢ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡨࡲࡵࡥࡧࠣࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡵ࠱ࠫ੆")
bstack1l1lll11_opy_ = bstackl_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩࡲࡦࡦࡨࡲࡹ࡯ࡡ࡭ࡵࠣࡲࡴࡺࠠࡱࡴࡲࡺ࡮ࡪࡥࡥ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡥࡩࡪࠠࡵࡪࡨࡱࠥ࡯࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦࠢࡤࡷࠥࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣࠢࡤࡲࡩࠦࠢࡢࡥࡦࡩࡸࡹࡋࡦࡻࠥࠤࡴࡸࠠࡴࡧࡷࠤࡹ࡮ࡥ࡮ࠢࡤࡷࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࡀࠠࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤࠣࡥࡳࡪࠠࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠦࠬੇ")
bstack1l111l111_opy_ = bstackl_opy_ (u"ࠧࡎࡣ࡯ࡪࡴࡸ࡭ࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠤࡾࢁࠧ࠭ੈ")
bstack1lll11_opy_ = bstackl_opy_ (u"ࠨࡇࡱࡧࡴࡻ࡮ࡵࡧࡵࡩࡩࠦࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡ࠯ࠣࡿࢂ࠭੉")
bstack11l1l111_opy_ = bstackl_opy_ (u"ࠩࡖࡸࡦࡸࡴࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭ࠩ੊")
bstack111l1l11_opy_ = bstackl_opy_ (u"ࠪࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪੋ")
bstack1l11l1_opy_ = bstackl_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭ࠢ࡬ࡷࠥࡴ࡯ࡸࠢࡵࡹࡳࡴࡩ࡯ࡩࠤࠫੌ")
bstack1l11l1l1l_opy_ = bstackl_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰ࠿ࠦࡻࡾ੍ࠩ")
bstack11111l11_opy_ = bstackl_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡ࡮ࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠࡸ࡫ࡷ࡬ࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࡼࡿࠪ੎")
bstack1ll1111l1_opy_ = bstackl_opy_ (u"ࠧࡖࡲࡧࡥࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠨ੏")
bstack111l11_opy_ = bstackl_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡺࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠧ੐")
bstack11ll1l_opy_ = bstackl_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢࡳࡶࡴࡼࡩࡥࡧࠣࡥࡳࠦࡡࡱࡲࡵࡳࡵࡸࡩࡢࡶࡨࠤࡋ࡝ࠠࠩࡴࡲࡦࡴࡺ࠯ࡱࡣࡥࡳࡹ࠯ࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠭ࠢࡶ࡯࡮ࡶࠠࡵࡪࡨࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡬ࡧࡼࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡨࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡸ࡯࡭ࡱ࡮ࡨࠤࡵࡿࡴࡩࡱࡱࠤࡸࡩࡲࡪࡲࡷࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡧ࡮ࡺࠢࡉ࡛࠳࠭ੑ")
bstack11ll111_opy_ = bstackl_opy_ (u"ࠪࡗࡪࡺࡴࡪࡰࡪࠤ࡭ࡺࡴࡱࡒࡵࡳࡽࡿ࠯ࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡰࡰࠣࡧࡺࡸࡲࡦࡰࡷࡰࡾࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢࡹࡩࡷࡹࡩࡰࡰࠣࡳ࡫ࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࠪࡾࢁ࠮࠲ࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡶࡲࡪࡶࡦࡪࡥࠡࡶࡲࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡄ࠽࠵࠰࠳࠲࠵ࠦ࡯ࡳࠢࡵࡩ࡫࡫ࡲࠡࡶࡲࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡽࡷࡸ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪ࡯ࡤࡵ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠯ࡳࡷࡱ࠱ࡹ࡫ࡳࡵࡵ࠰ࡦࡪ࡮ࡩ࡯ࡦ࠰ࡴࡷࡵࡸࡺࠥࡳࡽࡹ࡮࡯࡯ࠢࡩࡳࡷࠦࡡࠡࡹࡲࡶࡰࡧࡲࡰࡷࡱࡨ࠳࠭੒")
bstack11ll_opy_ = bstackl_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰࠱ࠫ੓")
bstack11lll111_opy_ = bstackl_opy_ (u"࡙ࠬࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡵࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠣࠪ੔")
bstack1l1ll1_opy_ = bstackl_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩ࠳ࠦࡻࡾࠩ੕")
bstack11lll1_opy_ = bstackl_opy_ (u"ࠧࡆࡺࡳࡩࡨࡺࡥࡥࠢࡤࡸࠥࡲࡥࡢࡵࡷࠤ࠶ࠦࡩ࡯ࡲࡸࡸ࠱ࠦࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡ࠲ࠪ੖")
bstack11l11ll1_opy_ = bstackl_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡂࡲࡳࠤࡺࡶ࡬ࡰࡣࡧ࠲ࠥࢁࡽࠨ੗")
bstack1ll111l1l_opy_ = bstackl_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰ࡭ࡱࡤࡨࠥࡇࡰࡱ࠰ࠣࡍࡳࡼࡡ࡭࡫ࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡾࢁ࠳࠭੘")
bstack1llll_opy_ = bstackl_opy_ (u"ࠪࡏࡪࡿࡳࠡࡥࡤࡲࡳࡵࡴࠡࡥࡲ࠱ࡪࡾࡩࡴࡶࠣࡥࡸࠦࡡࡱࡲࠣࡺࡦࡲࡵࡦࡵ࠯ࠤࡺࡹࡥࠡࡣࡱࡽࠥࡵ࡮ࡦࠢࡳࡶࡴࡶࡥࡳࡶࡼࠤ࡫ࡸ࡯࡮ࠢࡾ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡲࡤࡸ࡭ࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃࢃࠬࠡࡱࡱࡰࡾࠦࠢࡱࡣࡷ࡬ࠧࠦࡡ࡯ࡦࠣࠦࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠢࠡࡥࡤࡲࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡵࡱࡪࡩࡹ࡮ࡥࡳ࠰ࠪਖ਼")
bstack1llll111_opy_ = bstackl_opy_ (u"ࠫࡠࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡡࡱࡲࠣࡴࡷࡵࡰࡦࡴࡷࡽࡢࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸࠦࡡࡳࡧࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠯ࠢࡉࡳࡷࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡶ࡬ࡦࡣࡶࡩࠥࡼࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡽࡷࡸ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪ࡯ࡤࡵ࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴࡵ࡯ࡵ࡮࠱ࡶࡩࡹ࠳ࡵࡱ࠯ࡷࡩࡸࡺࡳ࠰ࡵࡳࡩࡨ࡯ࡦࡺ࠯ࡤࡴࡵ࠭ਗ਼")
bstack1lll111ll_opy_ = bstackl_opy_ (u"ࠬࡡࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡢࡲࡳࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࡣࠠࡔࡷࡳࡴࡴࡸࡴࡦࡦࠣࡺࡦࡲࡵࡦࡵࠣࡳ࡫ࠦࡡࡱࡲࠣࡥࡷ࡫ࠠࡰࡨࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠯ࠢࡉࡳࡷࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡶ࡬ࡦࡣࡶࡩࠥࡼࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡽࡷࡸ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪ࡯ࡤࡵ࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴࡵ࡯ࡵ࡮࠱ࡶࡩࡹ࠳ࡵࡱ࠯ࡷࡩࡸࡺࡳ࠰ࡵࡳࡩࡨ࡯ࡦࡺ࠯ࡤࡴࡵ࠭ਜ਼")
bstack1111l_opy_ = bstackl_opy_ (u"࠭ࡕࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡲࡳࠤ࡮ࡪࠠࡼࡿࠣࡪࡴࡸࠠࡩࡣࡶ࡬ࠥࡀࠠࡼࡿ࠱ࠫੜ")
bstack11l1ll1_opy_ = bstackl_opy_ (u"ࠧࡂࡲࡳࠤ࡚ࡶ࡬ࡰࡣࡧࡩࡩࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠦࡉࡅࠢ࠽ࠤࢀࢃࠧ੝")
bstack1l1l1111l_opy_ = bstackl_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡂࡲࡳࠤ࠿ࠦࡻࡾ࠰ࠪਫ਼")
bstack1l1lllll_opy_ = bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬࡯ࡳࠢࡹࡥࡳ࡯࡬࡭ࡣࠣࡴࡾࡺࡨࡰࡰࠣࡸࡪࡹࡴࡴ࠮ࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡼ࡯ࡴࡩࠢࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠡ࠿ࠣ࠵ࠬ੟")
bstack111l111_opy_ = bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࠼ࠣࡿࢂ࠭੠")
bstack1llll11_opy_ = bstackl_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡤ࡮ࡲࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸ࠺ࠡࡽࢀࠫ੡")
bstack1l111l1l1_opy_ = bstackl_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡩࡨࡸࠥࡸࡥࡢࡵࡲࡲࠥ࡬࡯ࡳࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡩࡦࡺࡵࡳࡧࠣࡪࡦ࡯࡬ࡶࡴࡨ࠲ࠥࢁࡽࠨ੢")
bstack11llll1_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡧࡰࡪࠢࡦࡥࡱࡲ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ੣")
bstack1l1ll111l_opy_ = bstackl_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷ࡭ࡵࡷࠡࡤࡸ࡭ࡱࡪࠠࡖࡔࡏ࠰ࠥࡧࡳࠡࡤࡸ࡭ࡱࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡺࡹࡥࡥ࠰ࠪ੤")
bstack1l1l1111_opy_ = bstackl_opy_ (u"ࠨࡕࡨࡶࡻ࡫ࡲࠡࡵ࡬ࡨࡪࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠪࡾࢁ࠮ࠦࡩࡴࠢࡱࡳࡹࠦࡳࡢ࡯ࡨࠤࡦࡹࠠࡤ࡮࡬ࡩࡳࡺࠠࡴ࡫ࡧࡩࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠩࡽࢀ࠭ࠬ੥")
bstack1l11l1lll_opy_ = bstackl_opy_ (u"࡙ࠩ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦ࡯࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡦࡤࡷ࡭ࡨ࡯ࡢࡴࡧ࠾ࠥࢁࡽࠨ੦")
bstack11lllll1_opy_ = bstackl_opy_ (u"࡙ࠪࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡡࡤࡥࡨࡷࡸࠦࡡࠡࡲࡵ࡭ࡻࡧࡴࡦࠢࡧࡳࡲࡧࡩ࡯࠼ࠣࡿࢂࠦ࠮ࠡࡕࡨࡸࠥࡺࡨࡦࠢࡩࡳࡱࡲ࡯ࡸ࡫ࡱ࡫ࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯࡮ࠡࡻࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠺ࠡ࡞ࡱ࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭ࠡ࡞ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬࠻ࠢࡷࡶࡺ࡫ࠠ࡝ࡰ࠰࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳ࠧ੧")
bstack1lll111l_opy_ = bstackl_opy_ (u"ࠫࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࡠࡧࡵࡶࡴࡸࠠ࠻ࠢࡾࢁࠬ੨")
bstack1l1l11l_opy_ = bstackl_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡱࡨࡤࡧ࡭ࡱ࡮࡬ࡸࡺࡪࡥࡠࡧࡹࡩࡳࡺࠠࡧࡱࡵࠤࡘࡊࡋࡔࡧࡷࡹࡵࠦࡻࡾࠤ੩")
bstack111ll1l_opy_ = bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡲࡩࡥࡡ࡮ࡲ࡯࡭ࡹࡻࡤࡦࡡࡨࡺࡪࡴࡴࠡࡨࡲࡶ࡙ࠥࡄࡌࡖࡨࡷࡹࡇࡴࡵࡧࡰࡴࡹ࡫ࡤࠡࡽࢀࠦ੪")
bstack1l11l111_opy_ = bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡗࡩࡸࡺࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠣࡿࢂࠨ੫")
bstack1111_opy_ = bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡸࡥࡠࡴࡨࡵࡺ࡫ࡳࡵࠢࡾࢁࠧ੬")
bstack1lllll11_opy_ = bstackl_opy_ (u"ࠤࡓࡓࡘ࡚ࠠࡆࡸࡨࡲࡹࠦࡻࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࠿ࠦࡻࡾࠤ੭")
bstack11111l1l_opy_ = bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࠢࡳࡶࡴࡾࡹࠡࡵࡨࡸࡹ࡯࡮ࡨࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ੮")
bstack1lll1l1_opy_ = bstackl_opy_ (u"ࠫࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠡࡽࢀࠫ੯")
bstack11l1111l_opy_ = bstackl_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡ࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷ࠿ࠦࡻࡾࠩੰ")
bstack1llllll1l_opy_ = bstackl_opy_ (u"࠭ࡎࡦࡣࡵࡩࡸࡺࠠࡩࡷࡥࠤࡦࡲ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡵ࠽ࠤࢀࢃࠧੱ")
bstack111l11ll_opy_ = bstackl_opy_ (u"ࠧࡆࡔࡕࡓࡗࠦࡉࡏࠢࡄࡐࡑࡕࡃࡂࡖࡈࠤࡍ࡛ࡂࠡࡽࢀࠫੲ")
bstack1l1lll1l1_opy_ = bstackl_opy_ (u"ࠨࡎࡤࡸࡪࡴࡣࡺࠢࡲࡪࠥ࡮ࡵࡣ࠼ࠣࡿࢂࠦࡩࡴ࠼ࠣࡿࢂ࠭ੳ")
bstack111ll1_opy_ = bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡲࡡࡵࡧࡱࡧࡾࠦࡦࡰࡴࠣࡿࢂࠦࡨࡶࡤ࠽ࠤࢀࢃࠧੴ")
bstack1ll1ll1l1_opy_ = bstackl_opy_ (u"ࠪࡌࡺࡨࠠࡶࡴ࡯ࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡵࡰࡵ࡫ࡰࡥࡱࠦࡨࡶࡤ࠽ࠤࢀࢃࠧੵ")
bstack1l1ll11ll_opy_ = bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡰࡲࡷ࡭ࡲࡧ࡬ࠡࡪࡸࡦࠥࡻࡲ࡭࠼ࠣࡿࢂ࠭੶")
bstack1ll1l11l1_opy_ = bstackl_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬ੷")
bstack1l11ll11l_opy_ = bstackl_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ੸")
from ._version import __version__
bstack1ll111l1_opy_ = None
CONFIG = {}
bstack1ll11l1_opy_ = {}
bstack1111l1l_opy_ = {}
bstack111l1ll_opy_ = None
bstack1l11l1l_opy_ = None
bstack1l111ll_opy_ = None
bstack1l111111l_opy_ = -1
bstack11l111ll_opy_ = bstack1l11l1ll1_opy_
bstack111l1111_opy_ = 1
bstack1lll11ll1_opy_ = False
bstack1l111l1ll_opy_ = bstackl_opy_ (u"ࠧࠨ੹")
bstack1ll1l1l_opy_ = bstackl_opy_ (u"ࠨࠩ੺")
bstack1llll1ll_opy_ = False
bstack1l11111_opy_ = True
bstack1l11l_opy_ = bstackl_opy_ (u"ࠩࠪ੻")
bstack1ll1lll11_opy_ = []
bstack1l1111l1l_opy_ = bstackl_opy_ (u"ࠪࠫ੼")
bstack1l1l1llll_opy_ = None
bstack11l1ll11_opy_ = None
bstack1l1l1l1_opy_ = None
bstack11lll1l_opy_ = None
bstack1l111l1_opy_ = None
bstack1l11l1111_opy_ = None
bstack1l1l1l_opy_ = None
bstack111ll_opy_ = None
bstack111llll_opy_ = None
bstack1llll11ll_opy_ = None
bstack111111l1_opy_ = None
bstack111l11l1_opy_ = None
bstack11l1ll_opy_ = bstackl_opy_ (u"ࠦࠧ੽")
class bstack1ll1l1l11_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1ll1l1l11_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l111ll_opy_,
                    format=bstackl_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪ੾"),
                    datefmt=bstackl_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ੿"))
def bstack111lll1l_opy_():
  global CONFIG
  global bstack11l111ll_opy_
  if bstackl_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ઀") in CONFIG:
    bstack11l111ll_opy_ = bstack1ll1ll11l_opy_[CONFIG[bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઁ")]]
    logging.getLogger().setLevel(bstack11l111ll_opy_)
def bstack11ll1l1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1l1l111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1llll1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstackl_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨં") == args[i].lower() or bstackl_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦઃ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l11l_opy_
      bstack1l11l_opy_ += bstackl_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩ઄") + path
      return path
  return None
def bstack11lll1ll_opy_():
  bstack1l111lll_opy_ = bstack1llll1111_opy_()
  if bstack1l111lll_opy_ and os.path.exists(os.path.abspath(bstack1l111lll_opy_)):
    fileName = bstack1l111lll_opy_
  if bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઅ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪઆ")])) and not bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩઇ") in locals():
    fileName = os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬઈ")]
  if bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫઉ") in locals():
    bstack1111111_opy_ = os.path.abspath(fileName)
  else:
    bstack1111111_opy_ = bstackl_opy_ (u"ࠪࠫઊ")
  bstack1l11l11_opy_ = os.getcwd()
  bstack11111l1_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧઋ")
  bstack1ll11_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩઌ")
  while (not os.path.exists(bstack1111111_opy_)) and bstack1l11l11_opy_ != bstackl_opy_ (u"ࠨࠢઍ"):
    bstack1111111_opy_ = os.path.join(bstack1l11l11_opy_, bstack11111l1_opy_)
    if not os.path.exists(bstack1111111_opy_):
      bstack1111111_opy_ = os.path.join(bstack1l11l11_opy_, bstack1ll11_opy_)
    if bstack1l11l11_opy_ != os.path.dirname(bstack1l11l11_opy_):
      bstack1l11l11_opy_ = os.path.dirname(bstack1l11l11_opy_)
    else:
      bstack1l11l11_opy_ = bstackl_opy_ (u"ࠢࠣ઎")
  if not os.path.exists(bstack1111111_opy_):
    bstack1l11llll1_opy_(
      bstack11l11l_opy_.format(os.getcwd()))
  with open(bstack1111111_opy_, bstackl_opy_ (u"ࠨࡴࠪએ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l11llll1_opy_(bstack1l111l111_opy_.format(str(exc)))
def bstack1ll11l111_opy_(config):
  bstack1lllll111_opy_ = bstack1l1l1lll1_opy_(config)
  for option in list(bstack1lllll111_opy_):
    if option.lower() in bstack1l11l1l11_opy_ and option != bstack1l11l1l11_opy_[option.lower()]:
      bstack1lllll111_opy_[bstack1l11l1l11_opy_[option.lower()]] = bstack1lllll111_opy_[option]
      del bstack1lllll111_opy_[option]
  return config
def bstack1ll11l_opy_():
  global bstack1111l1l_opy_
  for key, bstack1lll1l1l_opy_ in bstack1l1111l11_opy_.items():
    if isinstance(bstack1lll1l1l_opy_, list):
      for var in bstack1lll1l1l_opy_:
        if var in os.environ:
          bstack1111l1l_opy_[key] = os.environ[var]
          break
    elif bstack1lll1l1l_opy_ in os.environ:
      bstack1111l1l_opy_[key] = os.environ[bstack1lll1l1l_opy_]
  if bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫઐ") in os.environ:
    bstack1111l1l_opy_[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧઑ")] = {}
    bstack1111l1l_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ઒")][bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧઓ")] = os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨઔ")]
def bstack11l1lll_opy_():
  global bstack1ll11l1_opy_
  global bstack1l11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstackl_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪક").lower() == val.lower():
      bstack1ll11l1_opy_[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬખ")] = {}
      bstack1ll11l1_opy_[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ગ")][bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬઘ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack111lll_opy_ in bstack1ll1lll1l_opy_.items():
    if isinstance(bstack111lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack111lll_opy_:
          if idx<len(sys.argv) and bstackl_opy_ (u"ࠫ࠲࠳ࠧઙ") + var.lower() == val.lower() and not key in bstack1ll11l1_opy_:
            bstack1ll11l1_opy_[key] = sys.argv[idx+1]
            bstack1l11l_opy_ += bstackl_opy_ (u"ࠬࠦ࠭࠮ࠩચ") + var + bstackl_opy_ (u"࠭ࠠࠨછ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstackl_opy_ (u"ࠧ࠮࠯ࠪજ") + bstack111lll_opy_.lower() == val.lower() and not key in bstack1ll11l1_opy_:
          bstack1ll11l1_opy_[key] = sys.argv[idx+1]
          bstack1l11l_opy_ += bstackl_opy_ (u"ࠨࠢ࠰࠱ࠬઝ") + bstack111lll_opy_ + bstackl_opy_ (u"ࠩࠣࠫઞ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1l1l11ll_opy_(config):
  bstack1111l1l1_opy_ = config.keys()
  for bstack1ll1l1l1l_opy_, bstack1l1ll11l_opy_ in bstack1l11l11ll_opy_.items():
    if bstack1l1ll11l_opy_ in bstack1111l1l1_opy_:
      config[bstack1ll1l1l1l_opy_] = config[bstack1l1ll11l_opy_]
      del config[bstack1l1ll11l_opy_]
  for bstack1ll1l1l1l_opy_, bstack1l1ll11l_opy_ in bstack1l11l11l1_opy_.items():
    if isinstance(bstack1l1ll11l_opy_, list):
      for bstack1lll1_opy_ in bstack1l1ll11l_opy_:
        if bstack1lll1_opy_ in bstack1111l1l1_opy_:
          config[bstack1ll1l1l1l_opy_] = config[bstack1lll1_opy_]
          del config[bstack1lll1_opy_]
          break
    elif bstack1l1ll11l_opy_ in bstack1111l1l1_opy_:
        config[bstack1ll1l1l1l_opy_] = config[bstack1l1ll11l_opy_]
        del config[bstack1l1ll11l_opy_]
  for bstack1lll1_opy_ in list(config):
    for bstack11l11l11_opy_ in bstack1lllll1l1_opy_:
      if bstack1lll1_opy_.lower() == bstack11l11l11_opy_.lower() and bstack1lll1_opy_ != bstack11l11l11_opy_:
        config[bstack11l11l11_opy_] = config[bstack1lll1_opy_]
        del config[bstack1lll1_opy_]
  bstack1llll1l_opy_ = []
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ટ") in config:
    bstack1llll1l_opy_ = config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧઠ")]
  for platform in bstack1llll1l_opy_:
    for bstack1lll1_opy_ in list(platform):
      for bstack11l11l11_opy_ in bstack1lllll1l1_opy_:
        if bstack1lll1_opy_.lower() == bstack11l11l11_opy_.lower() and bstack1lll1_opy_ != bstack11l11l11_opy_:
          platform[bstack11l11l11_opy_] = platform[bstack1lll1_opy_]
          del platform[bstack1lll1_opy_]
  for bstack1ll1l1l1l_opy_, bstack1l1ll11l_opy_ in bstack1l11l11l1_opy_.items():
    for platform in bstack1llll1l_opy_:
      if isinstance(bstack1l1ll11l_opy_, list):
        for bstack1lll1_opy_ in bstack1l1ll11l_opy_:
          if bstack1lll1_opy_ in platform:
            platform[bstack1ll1l1l1l_opy_] = platform[bstack1lll1_opy_]
            del platform[bstack1lll1_opy_]
            break
      elif bstack1l1ll11l_opy_ in platform:
        platform[bstack1ll1l1l1l_opy_] = platform[bstack1l1ll11l_opy_]
        del platform[bstack1l1ll11l_opy_]
  for bstack1lll1lll_opy_ in bstack1111111l_opy_:
    if bstack1lll1lll_opy_ in config:
      if not bstack1111111l_opy_[bstack1lll1lll_opy_] in config:
        config[bstack1111111l_opy_[bstack1lll1lll_opy_]] = {}
      config[bstack1111111l_opy_[bstack1lll1lll_opy_]].update(config[bstack1lll1lll_opy_])
      del config[bstack1lll1lll_opy_]
  for platform in bstack1llll1l_opy_:
    for bstack1lll1lll_opy_ in bstack1111111l_opy_:
      if bstack1lll1lll_opy_ in list(platform):
        if not bstack1111111l_opy_[bstack1lll1lll_opy_] in platform:
          platform[bstack1111111l_opy_[bstack1lll1lll_opy_]] = {}
        platform[bstack1111111l_opy_[bstack1lll1lll_opy_]].update(platform[bstack1lll1lll_opy_])
        del platform[bstack1lll1lll_opy_]
  config = bstack1ll11l111_opy_(config)
  return config
def bstack11l1_opy_(config):
  global bstack1ll1l1l_opy_
  if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩડ") in config and str(config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪઢ")]).lower() != bstackl_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ણ"):
    if not bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬત") in config:
      config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭થ")] = {}
    if not bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬદ") in config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨધ")]:
      bstack1ll1l1l1_opy_ = datetime.datetime.now()
      bstack1ll1ll1l_opy_ = bstack1ll1l1l1_opy_.strftime(bstackl_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩન"))
      hostname = socket.gethostname()
      bstack1l1l1ll11_opy_ = bstackl_opy_ (u"࠭ࠧ઩").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstackl_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩપ").format(bstack1ll1ll1l_opy_, hostname, bstack1l1l1ll11_opy_)
      config[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫબ")] = identifier
    bstack1ll1l1l_opy_ = config[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧભ")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭મ")]
  return config
def bstack1l1ll1lll_opy_():
  if (
    isinstance(os.getenv(bstackl_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪય")), str) and len(os.getenv(bstackl_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫર"))) > 0
  ) or (
    isinstance(os.getenv(bstackl_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭઱")), str) and len(os.getenv(bstackl_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧલ"))) > 0
  ):
    return os.getenv(bstackl_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨળ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠪࡇࡎ࠭઴"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩવ") and str(os.getenv(bstackl_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡈࡏࠧશ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫષ"):
    return os.getenv(bstackl_opy_ (u"ࠧࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠪસ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࠫહ"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ઺") and str(os.getenv(bstackl_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࠪ઻"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦ઼ࠩ"):
    return os.getenv(bstackl_opy_ (u"࡚ࠬࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫઽ"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࠩા"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬિ") and str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࡣࡓࡇࡍࡆࠩી"))).lower() == bstackl_opy_ (u"ࠩࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠫુ"):
    return 0 # bstack11ll111l_opy_ bstack11111lll_opy_ not set build number env
  if os.getenv(bstackl_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍ࠭ૂ")) and os.getenv(bstackl_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠧૃ")):
    return os.getenv(bstackl_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧૄ"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࠩૅ"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૆") and str(os.getenv(bstackl_opy_ (u"ࠨࡆࡕࡓࡓࡋࠧે"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧૈ"):
    return os.getenv(bstackl_opy_ (u"ࠪࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨૉ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠫࡈࡏࠧ૊"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪો") and str(os.getenv(bstackl_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࠩૌ"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩ્ࠬ"):
    return os.getenv(bstackl_opy_ (u"ࠨࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠫ૎"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࠬ૏"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨૐ") and str(os.getenv(bstackl_opy_ (u"ࠫࡌࡏࡔࡍࡃࡅࡣࡈࡏࠧ૑"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒"):
    return os.getenv(bstackl_opy_ (u"࠭ࡃࡊࡡࡍࡓࡇࡥࡉࡅࠩ૓"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠧࡄࡋࠪ૔"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭૕") and str(os.getenv(bstackl_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠬ૖"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗"):
    return os.getenv(bstackl_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૘"), 0)
  if str(os.getenv(bstackl_opy_ (u"࡚ࠬࡆࡠࡄࡘࡍࡑࡊࠧ૙"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫ૚"):
    return os.getenv(bstackl_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧ૛"), 0)
  return -1
def bstack1l1111lll_opy_(bstack1l1111_opy_):
  global CONFIG
  if not bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૜") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૝")]:
    return
  CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૞")] = CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૟")].replace(
    bstackl_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧૠ"),
    str(bstack1l1111_opy_)
  )
def bstack1l11ll1l1_opy_():
  global CONFIG
  if not bstackl_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬૡ") in CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩૢ")]:
    return
  bstack1ll1l1l1_opy_ = datetime.datetime.now()
  bstack1ll1ll1l_opy_ = bstack1ll1l1l1_opy_.strftime(bstackl_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ૣ"))
  CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૤")] = CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૥")].replace(
    bstackl_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૦"),
    bstack1ll1ll1l_opy_
  )
def bstack1llll111l_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૧") in CONFIG and not bool(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")]):
    del CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")]
    return
  if not bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪") in CONFIG:
    CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")] = bstackl_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૬")
  if bstackl_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૭") in CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]:
    bstack1l11ll1l1_opy_()
    os.environ[bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ૯")] = CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰")]
  if not bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૱") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]:
    return
  bstack1l1111_opy_ = bstackl_opy_ (u"ࠪࠫ૳")
  bstack1111l11_opy_ = bstack1l1ll1lll_opy_()
  if bstack1111l11_opy_ != -1:
    bstack1l1111_opy_ = bstackl_opy_ (u"ࠫࡈࡏࠠࠨ૴") + str(bstack1111l11_opy_)
  if bstack1l1111_opy_ == bstackl_opy_ (u"ࠬ࠭૵"):
    bstack1l111llll_opy_ = bstack1l111111_opy_(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ૶")])
    if bstack1l111llll_opy_ != -1:
      bstack1l1111_opy_ = str(bstack1l111llll_opy_)
  if bstack1l1111_opy_:
    bstack1l1111lll_opy_(bstack1l1111_opy_)
    os.environ[bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ૷")] = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]
def bstack1l1llll11_opy_(bstack1l1l1ll1_opy_, bstack1lllll_opy_, path):
  bstack11l11l1l_opy_ = {
    bstackl_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ૹ"): bstack1lllll_opy_
  }
  if os.path.exists(path):
    bstack1l1l11l1_opy_ = json.load(open(path, bstackl_opy_ (u"ࠪࡶࡧ࠭ૺ")))
  else:
    bstack1l1l11l1_opy_ = {}
  bstack1l1l11l1_opy_[bstack1l1l1ll1_opy_] = bstack11l11l1l_opy_
  with open(path, bstackl_opy_ (u"ࠦࡼ࠱ࠢૻ")) as outfile:
    json.dump(bstack1l1l11l1_opy_, outfile)
def bstack1l111111_opy_(bstack1l1l1ll1_opy_):
  bstack1l1l1ll1_opy_ = str(bstack1l1l1ll1_opy_)
  bstack1lll1lll1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧૼ")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭૽"))
  try:
    if not os.path.exists(bstack1lll1lll1_opy_):
      os.makedirs(bstack1lll1lll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩ૾")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ૿"), bstackl_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ଀"))
    if not os.path.isfile(file_path):
      with open(file_path, bstackl_opy_ (u"ࠪࡻࠬଁ")):
        pass
      with open(file_path, bstackl_opy_ (u"ࠦࡼ࠱ࠢଂ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstackl_opy_ (u"ࠬࡸࠧଃ")) as bstack1l11l1l1_opy_:
      bstack1l1l11ll1_opy_ = json.load(bstack1l11l1l1_opy_)
    if bstack1l1l1ll1_opy_ in bstack1l1l11ll1_opy_:
      bstack111l_opy_ = bstack1l1l11ll1_opy_[bstack1l1l1ll1_opy_][bstackl_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ଄")]
      bstack1l11111l_opy_ = int(bstack111l_opy_) + 1
      bstack1l1llll11_opy_(bstack1l1l1ll1_opy_, bstack1l11111l_opy_, file_path)
      return bstack1l11111l_opy_
    else:
      bstack1l1llll11_opy_(bstack1l1l1ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111l111_opy_.format(str(e)))
    return -1
def bstack1llllll1_opy_(config):
  if not config[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩଅ")] or not config[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫଆ")]:
    return True
  else:
    return False
def bstack1l11ll1ll_opy_(config):
  if bstack1l1l1l111_opy_() < version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨଇ")):
    return False
  if bstack1l1l1l111_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩଈ")):
    return True
  if bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଉ") in config and config[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬଊ")] == False:
    return False
  else:
    return True
def bstack1l1l1l11_opy_(config, index = 0):
  global bstack1llll1ll_opy_
  bstack1lll111l1_opy_ = {}
  caps = bstack1lll1llll_opy_ + bstack1ll1ll1ll_opy_
  if bstack1llll1ll_opy_:
    caps += bstack1l1111ll1_opy_
  for key in config:
    if key in caps + [bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଋ")]:
      continue
    bstack1lll111l1_opy_[key] = config[key]
  if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଌ") in config:
    for bstack1lll1111l_opy_ in config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଍")][index]:
      if bstack1lll1111l_opy_ in caps + [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଎"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଏ")]:
        continue
      bstack1lll111l1_opy_[bstack1lll1111l_opy_] = config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଐ")][index][bstack1lll1111l_opy_]
  bstack1lll111l1_opy_[bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ଑")] = socket.gethostname()
  if bstackl_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ଒") in bstack1lll111l1_opy_:
    del(bstack1lll111l1_opy_[bstackl_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଓ")])
  return bstack1lll111l1_opy_
def bstack11lllllll_opy_(config):
  global bstack1llll1ll_opy_
  bstack1l1l1l1l_opy_ = {}
  caps = bstack1ll1ll1ll_opy_
  if bstack1llll1ll_opy_:
    caps+= bstack1l1111ll1_opy_
  for key in caps:
    if key in config:
      bstack1l1l1l1l_opy_[key] = config[key]
  return bstack1l1l1l1l_opy_
def bstack11lll11_opy_(bstack1lll111l1_opy_, bstack1l1l1l1l_opy_):
  bstack111111ll_opy_ = {}
  for key in bstack1lll111l1_opy_.keys():
    if key in bstack1l11l11ll_opy_:
      bstack111111ll_opy_[bstack1l11l11ll_opy_[key]] = bstack1lll111l1_opy_[key]
    else:
      bstack111111ll_opy_[key] = bstack1lll111l1_opy_[key]
  for key in bstack1l1l1l1l_opy_:
    if key in bstack1l11l11ll_opy_:
      bstack111111ll_opy_[bstack1l11l11ll_opy_[key]] = bstack1l1l1l1l_opy_[key]
    else:
      bstack111111ll_opy_[key] = bstack1l1l1l1l_opy_[key]
  return bstack111111ll_opy_
def bstack1l1lllll1_opy_(config, index = 0):
  global bstack1llll1ll_opy_
  caps = {}
  bstack1l1l1l1l_opy_ = bstack11lllllll_opy_(config)
  bstack11l11lll_opy_ = bstack1ll1ll1ll_opy_
  bstack11l11lll_opy_ += bstack1l1lll1ll_opy_
  if bstack1llll1ll_opy_:
    bstack11l11lll_opy_ += bstack1l1111ll1_opy_
  if bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଔ") in config:
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧକ") in config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ")][index]:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଗ")] = config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ")][index][bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଙ")]
    if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଚ") in config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଛ")][index]:
      caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪଜ")] = str(config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଝ")][index][bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଞ")])
    bstack11ll1ll1_opy_ = {}
    for bstack1l1l11l11_opy_ in bstack11l11lll_opy_:
      if bstack1l1l11l11_opy_ in config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଟ")][index]:
        if bstack1l1l11l11_opy_ == bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨଠ"):
          bstack11ll1ll1_opy_[bstack1l1l11l11_opy_] = str(config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][index][bstack1l1l11l11_opy_] * 1.0)
        else:
          bstack11ll1ll1_opy_[bstack1l1l11l11_opy_] = config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ")][index][bstack1l1l11l11_opy_]
        del(config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index][bstack1l1l11l11_opy_])
    bstack1l1l1l1l_opy_ = update(bstack1l1l1l1l_opy_, bstack11ll1ll1_opy_)
  bstack1lll111l1_opy_ = bstack1l1l1l11_opy_(config, index)
  for bstack1lll1_opy_ in bstack1ll1ll1ll_opy_ + [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨତ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଥ")]:
    if bstack1lll1_opy_ in bstack1lll111l1_opy_:
      bstack1l1l1l1l_opy_[bstack1lll1_opy_] = bstack1lll111l1_opy_[bstack1lll1_opy_]
      del(bstack1lll111l1_opy_[bstack1lll1_opy_])
  if bstack1l11ll1ll_opy_(config):
    bstack1lll111l1_opy_[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬଦ")] = True
    caps.update(bstack1l1l1l1l_opy_)
    caps[bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧଧ")] = bstack1lll111l1_opy_
  else:
    bstack1lll111l1_opy_[bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧନ")] = False
    caps.update(bstack11lll11_opy_(bstack1lll111l1_opy_, bstack1l1l1l1l_opy_))
    if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭଩") in caps:
      caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪପ")] = caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଫ")]
      del(caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩବ")])
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଭ") in caps:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨମ")] = caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଯ")]
      del(caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩର")])
  return caps
def bstack1lll1ll1_opy_():
  global bstack1l1111l1l_opy_
  if bstack1l1l1l111_opy_() <= version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ଱")):
    if bstack1l1111l1l_opy_ != bstackl_opy_ (u"ࠪࠫଲ"):
      return bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧଳ") + bstack1l1111l1l_opy_ + bstackl_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ଴")
    return bstack1lll1ll_opy_
  if  bstack1l1111l1l_opy_ != bstackl_opy_ (u"࠭ࠧଵ"):
    return bstackl_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଶ") + bstack1l1111l1l_opy_ + bstackl_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤଷ")
  return bstack1ll11ll11_opy_
def bstack1ll1l111_opy_(options):
  return hasattr(options, bstackl_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪସ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll11111l_opy_(options, bstack1lllllll_opy_):
  for bstack11l111_opy_ in bstack1lllllll_opy_:
    if bstack11l111_opy_ in [bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨହ"), bstackl_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ଺")]:
      next
    if bstack11l111_opy_ in options._experimental_options:
      options._experimental_options[bstack11l111_opy_]= update(options._experimental_options[bstack11l111_opy_], bstack1lllllll_opy_[bstack11l111_opy_])
    else:
      options.add_experimental_option(bstack11l111_opy_, bstack1lllllll_opy_[bstack11l111_opy_])
  if bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪ଻") in bstack1lllllll_opy_:
    for arg in bstack1lllllll_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡶ଼ࠫ")]:
      options.add_argument(arg)
    del(bstack1lllllll_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬଽ")])
  if bstackl_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬା") in bstack1lllllll_opy_:
    for ext in bstack1lllllll_opy_[bstackl_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ି")]:
      options.add_extension(ext)
    del(bstack1lllllll_opy_[bstackl_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧୀ")])
def bstack1l11lll11_opy_(options, bstack1l1l1ll_opy_):
  if bstackl_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪୁ") in bstack1l1l1ll_opy_:
    for bstack111ll1l1_opy_ in bstack1l1l1ll_opy_[bstackl_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫୂ")]:
      if bstack111ll1l1_opy_ in options._preferences:
        options._preferences[bstack111ll1l1_opy_] = update(options._preferences[bstack111ll1l1_opy_], bstack1l1l1ll_opy_[bstackl_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬୃ")][bstack111ll1l1_opy_])
      else:
        options.set_preference(bstack111ll1l1_opy_, bstack1l1l1ll_opy_[bstackl_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ୄ")][bstack111ll1l1_opy_])
  if bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅") in bstack1l1l1ll_opy_:
    for arg in bstack1l1l1ll_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୆")]:
      options.add_argument(arg)
def bstack1ll1111l_opy_(options, bstack1ll11111_opy_):
  if bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫେ") in bstack1ll11111_opy_:
    options.use_webview(bool(bstack1ll11111_opy_[bstackl_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬୈ")]))
  bstack1ll11111l_opy_(options, bstack1ll11111_opy_)
def bstack1ll1ll_opy_(options, bstack1l1lll11l_opy_):
  for bstack1l1111111_opy_ in bstack1l1lll11l_opy_:
    if bstack1l1111111_opy_ in [bstackl_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩ୉"), bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫ୊")]:
      next
    options.set_capability(bstack1l1111111_opy_, bstack1l1lll11l_opy_[bstack1l1111111_opy_])
  if bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬୋ") in bstack1l1lll11l_opy_:
    for arg in bstack1l1lll11l_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୌ")]:
      options.add_argument(arg)
  if bstackl_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ୍࠭") in bstack1l1lll11l_opy_:
    options.use_technology_preview(bool(bstack1l1lll11l_opy_[bstackl_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୎")]))
def bstack1ll11l11_opy_(options, bstack111ll11l_opy_):
  for bstack1ll1lllll_opy_ in bstack111ll11l_opy_:
    if bstack1ll1lllll_opy_ in [bstackl_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ୏"), bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪ୐")]:
      next
    options._options[bstack1ll1lllll_opy_] = bstack111ll11l_opy_[bstack1ll1lllll_opy_]
  if bstackl_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୑") in bstack111ll11l_opy_:
    for bstack11ll11l1_opy_ in bstack111ll11l_opy_[bstackl_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୒")]:
      options.add_additional_option(
          bstack11ll11l1_opy_, bstack111ll11l_opy_[bstackl_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୓")][bstack11ll11l1_opy_])
  if bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔") in bstack111ll11l_opy_:
    for arg in bstack111ll11l_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ୕")]:
      options.add_argument(arg)
def bstack1ll111lll_opy_(options, caps):
  if not hasattr(options, bstackl_opy_ (u"ࠫࡐࡋ࡙ࠨୖ")):
    return
  if options.KEY == bstackl_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪୗ") and options.KEY in caps:
    bstack1ll11111l_opy_(options, caps[bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୘")])
  elif options.KEY == bstackl_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ୙") and options.KEY in caps:
    bstack1l11lll11_opy_(options, caps[bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭୚")])
  elif options.KEY == bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ୛") and options.KEY in caps:
    bstack1ll1ll_opy_(options, caps[bstackl_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫଡ଼")])
  elif options.KEY == bstackl_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬଢ଼") and options.KEY in caps:
    bstack1ll1111l_opy_(options, caps[bstackl_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୞")])
  elif options.KEY == bstackl_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬୟ") and options.KEY in caps:
    bstack1ll11l11_opy_(options, caps[bstackl_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ୠ")])
def bstack1l1l11111_opy_(caps):
  global bstack1llll1ll_opy_
  if bstack1llll1ll_opy_:
    if bstack11ll1l1l_opy_() < version.parse(bstackl_opy_ (u"ࠨ࠴࠱࠷࠳࠶ࠧୡ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩୢ")
    if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨୣ") in caps:
      browser = caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୤")]
    elif bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୥") in caps:
      browser = caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୦")]
    browser = str(browser).lower()
    if browser == bstackl_opy_ (u"ࠧࡪࡲ࡫ࡳࡳ࡫ࠧ୧") or browser == bstackl_opy_ (u"ࠨ࡫ࡳࡥࡩ࠭୨"):
      browser = bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୩")
    if browser == bstackl_opy_ (u"ࠪࡷࡦࡳࡳࡶࡰࡪࠫ୪"):
      browser = bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୫")
    if browser not in [bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୬"), bstackl_opy_ (u"࠭ࡥࡥࡩࡨࠫ୭"), bstackl_opy_ (u"ࠧࡪࡧࠪ୮"), bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୯"), bstackl_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୰")]:
      return None
    try:
      package = bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࢀ࠲ࡴࡶࡴࡪࡱࡱࡷࠬୱ").format(browser)
      name = bstackl_opy_ (u"ࠫࡔࡶࡴࡪࡱࡱࡷࠬ୲")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1l111_opy_(options):
        return None
      for bstack1lll1_opy_ in caps.keys():
        options.set_capability(bstack1lll1_opy_, caps[bstack1lll1_opy_])
      bstack1ll111lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1lll1_opy_(options, bstack1l11lll_opy_):
  if not bstack1ll1l111_opy_(options):
    return
  for bstack1lll1_opy_ in bstack1l11lll_opy_.keys():
    if bstack1lll1_opy_ in bstack1l1lll1ll_opy_:
      next
    if bstack1lll1_opy_ in options._caps and type(options._caps[bstack1lll1_opy_]) in [dict, list]:
      options._caps[bstack1lll1_opy_] = update(options._caps[bstack1lll1_opy_], bstack1l11lll_opy_[bstack1lll1_opy_])
    else:
      options.set_capability(bstack1lll1_opy_, bstack1l11lll_opy_[bstack1lll1_opy_])
  bstack1ll111lll_opy_(options, bstack1l11lll_opy_)
  if bstackl_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫ୳") in options._caps:
    if options._caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୴")] and options._caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୵")].lower() != bstackl_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ୶"):
      del options._caps[bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ୷")]
def bstack1l11ll1_opy_(proxy_config):
  if bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ୸") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠫࡸࡹ࡬ࡑࡴࡲࡼࡾ࠭୹")] = proxy_config[bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ୺")]
    del(proxy_config[bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ୻")])
  if bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ୼") in proxy_config and proxy_config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ୽")].lower() != bstackl_opy_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࠩ୾"):
    proxy_config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭୿")] = bstackl_opy_ (u"ࠫࡲࡧ࡮ࡶࡣ࡯ࠫ஀")
  if bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡅࡺࡺ࡯ࡤࡱࡱࡪ࡮࡭ࡕࡳ࡮ࠪ஁") in proxy_config:
    proxy_config[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஂ")] = bstackl_opy_ (u"ࠧࡱࡣࡦࠫஃ")
  return proxy_config
def bstack11ll11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ஄") in config:
    return proxy
  config[bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨஅ")] = bstack1l11ll1_opy_(config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩஆ")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪஇ")])
  return proxy
def bstack1l1ll11_opy_(self):
  global CONFIG
  global bstack111ll_opy_
  if bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨஈ") in CONFIG:
    return CONFIG[bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩஉ")]
  elif bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫஊ") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ஋")]
  else:
    return bstack111ll_opy_(self)
def bstack1l1ll1l1_opy_():
  global CONFIG
  return bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ஌") in CONFIG or bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ஍") in CONFIG
def bstack1ll111_opy_(config):
  if not bstack1l1ll1l1_opy_():
    return
  if config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧஎ")):
    return config.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨஏ"))
  if config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஐ")):
    return config.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஑"))
def bstack1lll1l1l1_opy_():
  return bstack1l1ll1l1_opy_() and bstack1l1l1l111_opy_() >= version.parse(bstack11ll1l11_opy_)
def bstack1l1l1lll1_opy_(config):
  if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬஒ") in config:
    return config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ஓ")]
  if bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩஔ") in config:
    return config[bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪக")]
  return {}
def bstack111lllll_opy_(config):
  if bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ஖") in config:
    return config[bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ஗")]
  return {}
def bstack111l11l_opy_(caps):
  global bstack1ll1l1l_opy_
  if bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ஘") in caps:
    caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩங")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨச")] = True
    if bstack1ll1l1l_opy_:
      caps[bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ஛")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ஜ")] = bstack1ll1l1l_opy_
  else:
    caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ஝")] = True
    if bstack1ll1l1l_opy_:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧஞ")] = bstack1ll1l1l_opy_
def bstack1llll1l11_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫட") in CONFIG and CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ஠")]:
    bstack1lllll111_opy_ = bstack1l1l1lll1_opy_(CONFIG)
    bstack1llll1lll_opy_(CONFIG[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ஡")], bstack1lllll111_opy_)
def bstack1llll1lll_opy_(key, bstack1lllll111_opy_):
  global bstack1ll111l1_opy_
  logger.info(bstack11l1l111_opy_)
  try:
    bstack1ll111l1_opy_ = Local()
    bstack1l1lll1l_opy_ = {bstackl_opy_ (u"ࠪ࡯ࡪࡿࠧ஢"): key}
    bstack1l1lll1l_opy_.update(bstack1lllll111_opy_)
    logger.debug(bstack11111l11_opy_.format(str(bstack1l1lll1l_opy_)))
    bstack1ll111l1_opy_.start(**bstack1l1lll1l_opy_)
    if bstack1ll111l1_opy_.isRunning():
      logger.info(bstack1l11l1_opy_)
  except Exception as e:
    bstack1l11llll1_opy_(bstack1l11l1l1l_opy_.format(str(e)))
def bstack111ll111_opy_():
  global bstack1ll111l1_opy_
  if bstack1ll111l1_opy_.isRunning():
    logger.info(bstack111l1l11_opy_)
    bstack1ll111l1_opy_.stop()
  bstack1ll111l1_opy_ = None
def bstack1ll11llll_opy_():
  global bstack11l1ll_opy_
  global bstack1ll1lll11_opy_
  if bstack11l1ll_opy_:
    logger.warning(bstack11lllll1_opy_.format(str(bstack11l1ll_opy_)))
  logger.info(bstack1lll11lll_opy_)
  global bstack1ll111l1_opy_
  if bstack1ll111l1_opy_:
    bstack111ll111_opy_()
  try:
    for driver in bstack1ll1lll11_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll111ll_opy_)
  bstack1111ll_opy_()
def bstack1l1l11l1l_opy_(self, *args):
  logger.error(bstack1l11_opy_)
  bstack1ll11llll_opy_()
  sys.exit(1)
def bstack1l11llll1_opy_(err):
  logger.critical(bstack1lll11_opy_.format(str(err)))
  bstack1111ll_opy_(bstack1lll11_opy_.format(str(err)))
  atexit.unregister(bstack1ll11llll_opy_)
  sys.exit(1)
def bstack1llll11l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1111ll_opy_(message)
  atexit.unregister(bstack1ll11llll_opy_)
  sys.exit(1)
def bstack1l1ll1111_opy_():
  global CONFIG
  global bstack1ll11l1_opy_
  global bstack1111l1l_opy_
  global bstack1l11111_opy_
  CONFIG = bstack11lll1ll_opy_()
  bstack1ll11l_opy_()
  bstack11l1lll_opy_()
  CONFIG = bstack1l1l11ll_opy_(CONFIG)
  update(CONFIG, bstack1111l1l_opy_)
  update(CONFIG, bstack1ll11l1_opy_)
  CONFIG = bstack11l1_opy_(CONFIG)
  if bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨண") in CONFIG and str(CONFIG[bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩத")]).lower() == bstackl_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ஥"):
    bstack1l11111_opy_ = False
  if (bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஦") in CONFIG and bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ஧") in bstack1ll11l1_opy_) or (bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬந") in CONFIG and bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ன") not in bstack1111l1l_opy_):
    if os.getenv(bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨப")):
      CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ஫")] = os.getenv(bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ஬"))
    else:
      bstack1llll111l_opy_()
  elif (bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭") not in CONFIG and bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪம") in CONFIG) or (bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய") in bstack1111l1l_opy_ and bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ர") not in bstack1ll11l1_opy_):
    del(CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற")])
  if bstack1llllll1_opy_(CONFIG):
    bstack1l11llll1_opy_(bstack1l1lll11_opy_)
  bstack1l1llll_opy_()
  bstack1lllllll1_opy_()
  if bstack1llll1ll_opy_:
    CONFIG[bstackl_opy_ (u"ࠬࡧࡰࡱࠩல")] = bstack111l1lll_opy_(CONFIG)
    logger.info(bstack1l1l1111l_opy_.format(CONFIG[bstackl_opy_ (u"࠭ࡡࡱࡲࠪள")]))
def bstack1lllllll1_opy_():
  global CONFIG
  global bstack1llll1ll_opy_
  if bstackl_opy_ (u"ࠧࡢࡲࡳࠫழ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1l1llll1l_opy_)
    bstack1llll1ll_opy_ = True
def bstack111l1lll_opy_(config):
  bstack11l1l11l_opy_ = bstackl_opy_ (u"ࠨࠩவ")
  app = config[bstackl_opy_ (u"ࠩࡤࡴࡵ࠭ஶ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1l111_opy_:
      if os.path.exists(app):
        bstack11l1l11l_opy_ = bstack1llll1_opy_(config, app)
      elif bstack1ll111l11_opy_(app):
        bstack11l1l11l_opy_ = app
      else:
        bstack1l11llll1_opy_(bstack1ll111l1l_opy_.format(app))
    else:
      if bstack1ll111l11_opy_(app):
        bstack11l1l11l_opy_ = app
      elif os.path.exists(app):
        bstack11l1l11l_opy_ = bstack1llll1_opy_(app)
      else:
        bstack1l11llll1_opy_(bstack1lll111ll_opy_)
  else:
    if len(app) > 2:
      bstack1l11llll1_opy_(bstack1llll_opy_)
    elif len(app) == 2:
      if bstackl_opy_ (u"ࠪࡴࡦࡺࡨࠨஷ") in app and bstackl_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧஸ") in app:
        if os.path.exists(app[bstackl_opy_ (u"ࠬࡶࡡࡵࡪࠪஹ")]):
          bstack11l1l11l_opy_ = bstack1llll1_opy_(config, app[bstackl_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ஺")], app[bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ஻")])
        else:
          bstack1l11llll1_opy_(bstack1ll111l1l_opy_.format(app))
      else:
        bstack1l11llll1_opy_(bstack1llll_opy_)
    else:
      for key in app:
        if key in bstack111lll11_opy_:
          if key == bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭஼"):
            if os.path.exists(app[key]):
              bstack11l1l11l_opy_ = bstack1llll1_opy_(config, app[key])
            else:
              bstack1l11llll1_opy_(bstack1ll111l1l_opy_.format(app))
          else:
            bstack11l1l11l_opy_ = app[key]
        else:
          bstack1l11llll1_opy_(bstack1llll111_opy_)
  return bstack11l1l11l_opy_
def bstack1ll111l11_opy_(bstack11l1l11l_opy_):
  import re
  bstack11ll1ll_opy_ = re.compile(bstackl_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ஽"))
  bstack1ll111111_opy_ = re.compile(bstackl_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢா"))
  if bstackl_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪி") in bstack11l1l11l_opy_ or re.fullmatch(bstack11ll1ll_opy_, bstack11l1l11l_opy_) or re.fullmatch(bstack1ll111111_opy_, bstack11l1l11l_opy_):
    return True
  else:
    return False
def bstack1llll1_opy_(config, path, bstack111l111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠬࡸࡢࠨீ")).read()).hexdigest()
  bstack11lll_opy_ = bstack11111ll_opy_(md5_hash)
  bstack11l1l11l_opy_ = None
  if bstack11lll_opy_:
    logger.info(bstack1111l_opy_.format(bstack11lll_opy_, md5_hash))
    return bstack11lll_opy_
  bstack1l1l111_opy_ = MultipartEncoder(
    fields={
        bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࠫு"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"ࠧࡳࡤࠪூ")), bstackl_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ௃")),
        bstackl_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௄"): bstack111l111l_opy_
    }
  )
  response = requests.post(bstack1l111ll1_opy_, data=bstack1l1l111_opy_,
                         headers={bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ௅"): bstack1l1l111_opy_.content_type}, auth=(config[bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ெ")], config[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨே")]))
  try:
    res = json.loads(response.text)
    bstack11l1l11l_opy_ = res[bstackl_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧை")]
    logger.info(bstack11l1ll1_opy_.format(bstack11l1l11l_opy_))
    bstack1llll1l1_opy_(md5_hash, bstack11l1l11l_opy_)
  except ValueError as err:
    bstack1l11llll1_opy_(bstack11l11ll1_opy_.format(str(err)))
  return bstack11l1l11l_opy_
def bstack1l1llll_opy_():
  global CONFIG
  global bstack111l1111_opy_
  bstack1l111l1l_opy_ = 0
  bstack111lll1_opy_ = 1
  if bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ௉") in CONFIG:
    bstack111lll1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨொ")]
  if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬோ") in CONFIG:
    bstack1l111l1l_opy_ = len(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ௌ")])
  bstack111l1111_opy_ = int(bstack111lll1_opy_) * int(bstack1l111l1l_opy_)
def bstack11111ll_opy_(md5_hash):
  bstack1l1111l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ்࠭")), bstackl_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ௎"), bstackl_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ௏"))
  if os.path.exists(bstack1l1111l_opy_):
    bstack11111ll1_opy_ = json.load(open(bstack1l1111l_opy_,bstackl_opy_ (u"ࠧࡳࡤࠪௐ")))
    if md5_hash in bstack11111ll1_opy_:
      bstack11ll11ll_opy_ = bstack11111ll1_opy_[md5_hash]
      bstack1ll1l1ll_opy_ = datetime.datetime.now()
      bstack1111lll_opy_ = datetime.datetime.strptime(bstack11ll11ll_opy_[bstackl_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ௑")], bstackl_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭௒"))
      if (bstack1ll1l1ll_opy_ - bstack1111lll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11ll11ll_opy_[bstackl_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௓")]):
        return None
      return bstack11ll11ll_opy_[bstackl_opy_ (u"ࠫ࡮ࡪࠧ௔")]
  else:
    return None
def bstack1llll1l1_opy_(md5_hash, bstack11l1l11l_opy_):
  bstack1lll1lll1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧ௕")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭௖"))
  if not os.path.exists(bstack1lll1lll1_opy_):
    os.makedirs(bstack1lll1lll1_opy_)
  bstack1l1111l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩௗ")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ௘"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ௙"))
  bstack1ll1l1lll_opy_ = {
    bstackl_opy_ (u"ࠪ࡭ࡩ࠭௚"): bstack11l1l11l_opy_,
    bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ௛"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ௜")),
    bstackl_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ௝"): str(__version__)
  }
  if os.path.exists(bstack1l1111l_opy_):
    bstack11111ll1_opy_ = json.load(open(bstack1l1111l_opy_,bstackl_opy_ (u"ࠧࡳࡤࠪ௞")))
  else:
    bstack11111ll1_opy_ = {}
  bstack11111ll1_opy_[md5_hash] = bstack1ll1l1lll_opy_
  with open(bstack1l1111l_opy_, bstackl_opy_ (u"ࠣࡹ࠮ࠦ௟")) as outfile:
    json.dump(bstack11111ll1_opy_, outfile)
def bstack11lll1l1_opy_(self):
  return
def bstack1l1l1l1l1_opy_(self):
  return
def bstack1l111l11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1111llll_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack111l1ll_opy_
  global bstack1l111111l_opy_
  global bstack1l111ll_opy_
  global bstack1lll11ll1_opy_
  global bstack1l111l1ll_opy_
  global bstack1l1l1llll_opy_
  global bstack1ll1lll11_opy_
  CONFIG[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ௠")] = str(bstack1l111l1ll_opy_) + str(__version__)
  command_executor = bstack1lll1ll1_opy_()
  logger.debug(bstack1ll1lll_opy_.format(command_executor))
  proxy = bstack11ll11_opy_(CONFIG, proxy)
  bstack1lllll1_opy_ = 0 if bstack1l111111l_opy_ < 0 else bstack1l111111l_opy_
  if bstack1lll11ll1_opy_ is True:
    bstack1lllll1_opy_ = int(threading.current_thread().getName())
  bstack1l11lll_opy_ = bstack1l1lllll1_opy_(CONFIG, bstack1lllll1_opy_)
  logger.debug(bstack11111111_opy_.format(str(bstack1l11lll_opy_)))
  if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ௡") in CONFIG and CONFIG[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ௢")]:
    bstack111l11l_opy_(bstack1l11lll_opy_)
  if desired_capabilities:
    bstack1l111ll1l_opy_ = bstack1l1l11ll_opy_(desired_capabilities)
    bstack1l111ll1l_opy_[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ௣")] = bstack1l11ll1ll_opy_(CONFIG)
    bstack1ll1l1_opy_ = bstack1l1lllll1_opy_(bstack1l111ll1l_opy_)
    if bstack1ll1l1_opy_:
      bstack1l11lll_opy_ = update(bstack1ll1l1_opy_, bstack1l11lll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1lll1_opy_(options, bstack1l11lll_opy_)
  if not options:
    options = bstack1l1l11111_opy_(bstack1l11lll_opy_)
  if options and bstack1l1l1l111_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ௤")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1l1l1l111_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭௥")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11lll_opy_)
  logger.info(bstack1l11ll111_opy_)
  if bstack1l1l1l111_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ௦")):
    bstack1l1l1llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l1l111_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ௧")):
    bstack1l1l1llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1l1llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1l1l111l1_opy_ = bstackl_opy_ (u"ࠪࠫ௨")
    if bstack1l1l1l111_opy_() >= version.parse(bstackl_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ௩")):
      bstack1l1l111l1_opy_ = self.caps.get(bstackl_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ௪"))
    else:
      bstack1l1l111l1_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ௫"))
    if bstack1l1l111l1_opy_:
      if bstack1l1l1l111_opy_() <= version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ௬")):
        self.command_executor._url = bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ௭") + bstack1l1111l1l_opy_ + bstackl_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ௮")
      else:
        self.command_executor._url = bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ௯") + bstack1l1l111l1_opy_ + bstackl_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ௰")
      logger.debug(bstack1ll1ll1l1_opy_.format(bstack1l1l111l1_opy_))
    else:
      logger.debug(bstack1l1ll11ll_opy_.format(bstackl_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ௱")))
  except Exception as e:
    logger.debug(bstack1l1ll11ll_opy_.format(e))
  bstack111l1ll_opy_ = self.session_id
  bstack1ll1lll11_opy_.append(self)
  if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௲") in CONFIG and bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ௳") in CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௴")][bstack1lllll1_opy_]:
    bstack1l111ll_opy_ = CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௵")][bstack1lllll1_opy_][bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௶")]
  logger.debug(bstack1l11l1ll_opy_.format(bstack111l1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack111111l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      if(bstackl_opy_ (u"ࠦ࡮ࡴࡤࡦࡺ࠱࡮ࡸࠨ௷") in args[1]):
        with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧ௸")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭௹"), bstackl_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ௺")), bstackl_opy_ (u"ࠨࡹࠪ௻")) as fp:
          fp.write(bstackl_opy_ (u"ࠤࠥ௼"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ௽")))):
          with open(args[1], bstackl_opy_ (u"ࠫࡷ࠭௾")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstackl_opy_ (u"ࠬࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦ࡟࡯ࡧࡺࡔࡦ࡭ࡥࠩࡥࡲࡲࡹ࡫ࡸࡵ࠮ࠣࡴࡦ࡭ࡥࠡ࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠫ௿") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1l11l1_opy_)
            lines.insert(1, bstack1l11ll11l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣఀ")), bstackl_opy_ (u"ࠧࡸࠩఁ")) as bstack11l1llll_opy_:
              bstack11l1llll_opy_.writelines(lines)
        CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪం")] = str(bstack1l111l1ll_opy_) + str(__version__)
        bstack1lllll1_opy_ = 0 if bstack1l111111l_opy_ < 0 else bstack1l111111l_opy_
        if bstack1lll11ll1_opy_ is True:
          bstack1lllll1_opy_ = int(threading.current_thread().getName())
        CONFIG[bstackl_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤః")] = False
        bstack1l11lll_opy_ = bstack1l1lllll1_opy_(CONFIG, bstack1lllll1_opy_)
        logger.debug(bstack11111111_opy_.format(str(bstack1l11lll_opy_)))
        if CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧఄ")]:
          bstack111l11l_opy_(bstack1l11lll_opy_)
        if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఅ") in CONFIG and bstackl_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪఆ") in CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఇ")][bstack1lllll1_opy_]:
          bstack1l111ll_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఈ")][bstack1lllll1_opy_][bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఉ")]
        args.append(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫఊ")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఋ"), bstackl_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ఌ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ఍"))
      return bstack111111l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    logger.debug(bstack1111ll11_opy_ + str(e))
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1111ll1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack111l1ll_opy_
    global bstack1l111111l_opy_
    global bstack1l111ll_opy_
    global bstack1lll11ll1_opy_
    global bstack1l111l1ll_opy_
    global bstack1l1l1llll_opy_
    CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨఎ")] = str(bstack1l111l1ll_opy_) + str(__version__)
    bstack1lllll1_opy_ = 0 if bstack1l111111l_opy_ < 0 else bstack1l111111l_opy_
    if bstack1lll11ll1_opy_ is True:
      bstack1lllll1_opy_ = int(threading.current_thread().getName())
    CONFIG[bstackl_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢఏ")] = False
    bstack1l11lll_opy_ = bstack1l1lllll1_opy_(CONFIG, bstack1lllll1_opy_)
    logger.debug(bstack11111111_opy_.format(str(bstack1l11lll_opy_)))
    if CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬఐ")]:
      bstack111l11l_opy_(bstack1l11lll_opy_)
    if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ఑") in CONFIG and bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఒ") in CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఓ")][bstack1lllll1_opy_]:
      bstack1l111ll_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఔ")][bstack1lllll1_opy_][bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫక")]
    import urllib
    import json
    bstack111llll1_opy_ = bstackl_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩఖ") + urllib.parse.quote(json.dumps(bstack1l11lll_opy_))
    browser = self.connect(bstack111llll1_opy_)
    return browser
except Exception as e:
    logger.debug(bstack1111ll11_opy_ + str(e))
def bstack1ll1l1ll1_opy_():
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1111ll1l_opy_
    except Exception as e:
        logger.debug(bstack1111ll11_opy_ + str(e))
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack111111l_opy_
    except Exception as e:
      logger.debug(bstack1111ll11_opy_ + str(e))
def bstack1111l11l_opy_(context, bstack1ll1l1111_opy_):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤగ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ఘ")+ json.dumps(bstack1ll1l1111_opy_) + bstackl_opy_ (u"ࠥࢁࢂࠨఙ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤచ"), e)
def bstack11l11ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨఛ"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫజ") + json.dumps(message) + bstackl_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪఝ") + json.dumps(level) + bstackl_opy_ (u"ࠨࡿࢀࠫఞ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧట"), e)
def bstack1l1ll1ll_opy_(context, status, message = bstackl_opy_ (u"ࠥࠦఠ")):
  try:
    if(status == bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦడ")):
      context.page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨఢ"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡸࡥࡢࡵࡲࡲࠧࡀࠧణ") + json.dumps(bstackl_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡࠤత") + str(message)) + bstackl_opy_ (u"ࠨ࠮ࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬథ") + json.dumps(status) + bstackl_opy_ (u"ࠤࢀࢁࠧద"))
    else:
      context.page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦధ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬన") + json.dumps(status) + bstackl_opy_ (u"ࠧࢃࡽࠣ఩"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥప"), e)
def bstack1ll11l11l_opy_(self, url):
  global bstack1llll11ll_opy_
  try:
    bstack1l1llll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll111l_opy_.format(str(err)))
  try:
    bstack1llll11ll_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll11l1l_opy_ = str(e)
      if any(err_msg in bstack1lll11l1l_opy_ for err_msg in bstack1ll11ll_opy_):
        bstack1l1llll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll111l_opy_.format(str(err)))
    raise e
def bstack11ll1lll_opy_(self, test):
  global CONFIG
  global bstack111l1ll_opy_
  global bstack1l11l1l_opy_
  global bstack1l111ll_opy_
  global bstack11l1ll11_opy_
  try:
    if not bstack111l1ll_opy_:
      with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩఫ")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨబ"), bstackl_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫభ"))) as f:
        bstack11llll_opy_ = json.loads(bstackl_opy_ (u"ࠥࡿࠧమ") + f.read().strip() + bstackl_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭య") + bstackl_opy_ (u"ࠧࢃࠢర"))
        bstack111l1ll_opy_ = bstack11llll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack111l1ll_opy_:
    try:
      data = {}
      bstack11l11l1_opy_ = None
      if test:
        bstack11l11l1_opy_ = str(test.data)
      if bstack11l11l1_opy_ and not bstack1l111ll_opy_:
        data[bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫఱ")] = bstack11l11l1_opy_
      if bstack1l11l1l_opy_:
        if bstack1l11l1l_opy_.status == bstackl_opy_ (u"ࠧࡑࡃࡖࡗࠬల"):
          data[bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨళ")] = bstackl_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩఴ")
        elif bstack1l11l1l_opy_.status == bstackl_opy_ (u"ࠪࡊࡆࡏࡌࠨవ"):
          data[bstackl_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫశ")] = bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬష")
          if bstack1l11l1l_opy_.message:
            data[bstackl_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭స")] = str(bstack1l11l1l_opy_.message)
      user = CONFIG[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩహ")]
      key = CONFIG[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ఺")]
      url = bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ఻").format(user, key, bstack111l1ll_opy_)
      headers = {
        bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦ఼ࠩ"): bstackl_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧఽ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111l11_opy_.format(str(e)))
  bstack11l1ll11_opy_(self, test)
def bstack1lll11ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1l1_opy_
  bstack1l1l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11l1l_opy_
  bstack1l11l1l_opy_ = self._test
def bstack1ll11l1l_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstackl_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠧా"), bstackl_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠥి"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࡤࡪࡴࠥీ"), bstackl_opy_ (u"ࠣ࠰ࠥు")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstackl_opy_ (u"ࠤ࠭࠲ࡽࡳ࡬ࠣూ"))))
  if not files:
    pabot._write(bstackl_opy_ (u"࡛ࠪࡆࡘࡎ࠻ࠢࡑࡳࠥࡵࡵࡵࡲࡸࡸࠥ࡬ࡩ࡭ࡧࡶࠤ࡮ࡴࠠࠣࠧࡶࠦࠬృ") % outs_dir, pabot.Color.YELLOW)
    return bstackl_opy_ (u"ࠦࠧౄ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1llllllll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstackl_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ౅") in options:
    del options[bstackl_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥె")]
  if ROBOT_VERSION < bstackl_opy_ (u"ࠢ࠵࠰࠳ࠦే"):
    stats = {
      bstackl_opy_ (u"ࠣࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠥై"): {bstackl_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ౉"): 0, bstackl_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥొ"): 0, bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦో"): 0},
      bstackl_opy_ (u"ࠧࡧ࡬࡭ࠤౌ"): {bstackl_opy_ (u"ࠨࡴࡰࡶࡤࡰ్ࠧ"): 0, bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౎"): 0, bstackl_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ౏"): 0},
    }
  else:
    stats = {
      bstackl_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ౐"): 0,
      bstackl_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౑"): 0,
      bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ౒"): 0,
      bstackl_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨ౓"): 0,
    }
  if pabot_args[bstackl_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧ౔")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstackl_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨౕ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstackl_opy_ (u"ࠣࡣࡵࡸ࡮࡬ࡡࡤࡶࡶౖࠦ")], pabot_args[bstackl_opy_ (u"ࠤࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࡮ࡴࡳࡶࡤࡩࡳࡱࡪࡥࡳࡵࠥ౗")]
      )
      outputs += [
        bstack1ll11l1l_opy_(
          os.path.join(outs_dir, str(index)+ bstackl_opy_ (u"ࠥ࠳ࠧౘ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstackl_opy_ (u"ࠦࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠦౙ"), bstackl_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠪࡹ࠮ࡹ࡯࡯ࠦౚ") % index),
        )
      ]
    if bstackl_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹࠨ౛") not in options:
      options[bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢ౜")] = bstackl_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧౝ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll1ll1l_opy_(self, ff_profile_dir):
  global bstack11lll1l_opy_
  if not ff_profile_dir:
    return None
  return bstack11lll1l_opy_(self, ff_profile_dir)
def bstack1l111l11l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1l1l_opy_
  bstack11llll1l_opy_ = []
  if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౞") in CONFIG:
    bstack11llll1l_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౟")]
  bstack11llllll_opy_ = len(suite_group) * len(pabot_args[bstackl_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦౠ")] or [(bstackl_opy_ (u"ࠧࠨౡ"), None)]) * len(bstack11llll1l_opy_)
  pabot_args[bstackl_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧౢ")] = []
  for q in range(bstack11llllll_opy_):
    pabot_args[bstackl_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨౣ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ౤")],
      pabot_args[bstackl_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ౥")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ౦")),
      pabot_args[bstackl_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢ౧")],
      platform[0],
      bstack1ll1l1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ౨")] or [(bstackl_opy_ (u"ࠨࠢ౩"), None)]
    for platform in enumerate(bstack11llll1l_opy_)
  ]
def bstack1l1l11lll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11l11_opy_=bstackl_opy_ (u"ࠧࠨ౪")):
  global bstack1l11l1111_opy_
  self.platform_index = platform_index
  self.bstack1l11lll1_opy_ = bstack11l11_opy_
  bstack1l11l1111_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1l11l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1l_opy_
  global bstack1l11l_opy_
  if not bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ౫") in item.options:
    item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ౬")] = []
  for v in item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౭")]:
    if bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ౮") in v:
      item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ౯")].remove(v)
    if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭౰") in v:
      item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ౱")].remove(v)
  item.options[bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ౲")].insert(0, bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ౳").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౴")].insert(0, bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ౵").format(item.bstack1l11lll1_opy_))
  if bstack1l11l_opy_:
    item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ౶")].insert(0, bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ౷").format(bstack1l11l_opy_))
  return bstack1l1l1l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l11l11l_opy_(command):
  global bstack1l11l_opy_
  if bstack1l11l_opy_:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭౸"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠭౹") + bstack1l11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౺"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ౻"), 1)
def bstack1lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l111l1_opy_
  bstack1l11l11l_opy_(command)
  return bstack1l111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l111l1_opy_
  bstack1l11l11l_opy_(command)
  return bstack1l111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l111l1_opy_
  bstack1l11l11l_opy_(command)
  return bstack1l111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll111l_opy_(self, runner, quiet=False, capture=True):
  global bstack11lll11l_opy_
  bstack1ll11ll1l_opy_ = bstack11lll11l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstackl_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫ౼")):
      runner.exception_arr = []
    if not hasattr(runner, bstackl_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ౽")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll11ll1l_opy_
def bstack1l11l111l_opy_(self, name, context, *args):
  global bstack1l11ll11_opy_
  if name in [bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ౾"), bstackl_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ౿")]:
    bstack1l11ll11_opy_(self, name, context, *args)
  if name == bstackl_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಀ"):
    try:
      bstack1ll1l1111_opy_ = str(self.feature.name)
      bstack1111l11l_opy_(context, bstack1ll1l1111_opy_)
      context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧಁ") + json.dumps(bstack1ll1l1111_opy_) + bstackl_opy_ (u"ࠪࢁࢂ࠭ಂ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫಃ").format(str(e)))
  if name == bstackl_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ಄"):
    try:
      if not hasattr(self, bstackl_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨಅ")):
        self.driver_before_scenario = True
      bstack11111_opy_ = args[0].name
      bstack1ll11ll1_opy_ = bstack1ll1l1111_opy_ = str(self.feature.name)
      bstack1ll1l1111_opy_ = bstack1ll11ll1_opy_ + bstackl_opy_ (u"ࠧࠡ࠯ࠣࠫಆ") + bstack11111_opy_
      if self.driver_before_scenario:
        bstack1111l11l_opy_(context, bstack1ll1l1111_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ಇ") + json.dumps(bstack1ll1l1111_opy_) + bstackl_opy_ (u"ࠩࢀࢁࠬಈ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫಉ").format(str(e)))
  if name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಊ"):
    try:
      bstack1llll11l_opy_ = args[0].status.name
      if str(bstack1llll11l_opy_).lower() == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬಋ"):
        bstack1l1ll1l_opy_ = bstackl_opy_ (u"࠭ࠧಌ")
        bstack1lll11l11_opy_ = bstackl_opy_ (u"ࠧࠨ಍")
        bstack1l11llll_opy_ = bstackl_opy_ (u"ࠨࠩಎ")
        try:
          import traceback
          bstack1l1ll1l_opy_ = self.exception.__class__.__name__
          bstack1l1ll111_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1lll11l11_opy_ = bstackl_opy_ (u"ࠩࠣࠫಏ").join(bstack1l1ll111_opy_)
          bstack1l11llll_opy_ = bstack1l1ll111_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l111l1l1_opy_.format(str(e)))
        bstack1l1ll1l_opy_ += bstack1l11llll_opy_
        bstack11l11ll_opy_(context, json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤಐ") + str(bstack1lll11l11_opy_)), bstackl_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ಑"))
        if self.driver_before_scenario:
          bstack1l1ll1ll_opy_(context, bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಒ"), bstack1l1ll1l_opy_)
        context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫಓ") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨಔ") + str(bstack1lll11l11_opy_)) + bstackl_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨಕ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩಖ") + json.dumps(bstackl_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢಗ") + str(bstack1l1ll1l_opy_)) + bstackl_opy_ (u"ࠫࢂࢃࠧಘ"))
      else:
        bstack11l11ll_opy_(context, bstackl_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨಙ"), bstackl_opy_ (u"ࠨࡩ࡯ࡨࡲࠦಚ"))
        if self.driver_before_scenario:
          bstack1l1ll1ll_opy_(context, bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢಛ"))
        context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ಜ") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨಝ")) + bstackl_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩಞ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨಟ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧಠ").format(str(e)))
  if name == bstackl_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ಡ"):
    try:
      if context.failed is True:
        bstack1l11lll1l_opy_ = []
        bstack1l1l1l1ll_opy_ = []
        bstack1llll1ll1_opy_ = []
        bstack1l1ll_opy_ = bstackl_opy_ (u"ࠧࠨಢ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l11lll1l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l1ll111_opy_ = traceback.format_tb(exc_tb)
            bstack1lll1l11l_opy_ = bstackl_opy_ (u"ࠨࠢࠪಣ").join(bstack1l1ll111_opy_)
            bstack1l1l1l1ll_opy_.append(bstack1lll1l11l_opy_)
            bstack1llll1ll1_opy_.append(bstack1l1ll111_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l111l1l1_opy_.format(str(e)))
        bstack1l1ll1l_opy_ = bstackl_opy_ (u"ࠩࠪತ")
        for i in range(len(bstack1l11lll1l_opy_)):
          bstack1l1ll1l_opy_ += bstack1l11lll1l_opy_[i] + bstack1llll1ll1_opy_[i] + bstackl_opy_ (u"ࠪࡠࡳ࠭ಥ")
        bstack1l1ll_opy_ = bstackl_opy_ (u"ࠫࠥ࠭ದ").join(bstack1l1l1l1ll_opy_)
        if not self.driver_before_scenario:
          bstack11l11ll_opy_(context, bstack1l1ll_opy_, bstackl_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦಧ"))
          bstack1l1ll1ll_opy_(context, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨನ"), bstack1l1ll1l_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ಩") + json.dumps(bstack1l1ll_opy_) + bstackl_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨಪ"))
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩಫ") + json.dumps(bstackl_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣಬ") + str(bstack1l1ll1l_opy_)) + bstackl_opy_ (u"ࠫࢂࢃࠧಭ"))
      else:
        if not self.driver_before_scenario:
          bstack11l11ll_opy_(context, bstackl_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣಮ") + str(self.feature.name) + bstackl_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣಯ"), bstackl_opy_ (u"ࠢࡪࡰࡩࡳࠧರ"))
          bstack1l1ll1ll_opy_(context, bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಱ"))
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧಲ") + json.dumps(bstackl_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨಳ") + str(self.feature.name) + bstackl_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ಴")) + bstackl_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫವ"))
          context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪಶ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩಷ").format(str(e)))
  if name in [bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಸ"), bstackl_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಹ")]:
    bstack1l11ll11_opy_(self, name, context, *args)
    if (name == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ಺") and self.driver_before_scenario) or (name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ಻") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack1ll1lll1_opy_(config, startdir):
  return bstackl_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿ಼ࠥ").format(bstackl_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧಽ"))
class Notset:
  def __repr__(self):
    return bstackl_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤಾ")
notset = Notset()
def bstack1l1llllll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111l11l1_opy_
  if str(name).lower() == bstackl_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨಿ"):
    return bstackl_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣೀ")
  else:
    return bstack111l11l1_opy_(self, name, default, skip)
def bstack11ll11l_opy_(bstack1111lll1_opy_):
  global bstack1l111l1ll_opy_
  bstack1l111l1ll_opy_ = bstack1111lll1_opy_
  logger.info(bstack1lllll1l_opy_.format(bstack1l111l1ll_opy_.split(bstackl_opy_ (u"ࠪ࠱ࠬು"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack111ll1ll_opy_ + str(e))
  Service.start = bstack11lll1l1_opy_
  Service.stop = bstack1l1l1l1l1_opy_
  webdriver.Remote.__init__ = bstack1111llll_opy_
  webdriver.Remote.get = bstack1ll11l11l_opy_
  WebDriver.close = bstack1l111l11_opy_
  bstack1ll1l1ll1_opy_()
  if bstack1lll1l1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1ll11_opy_
    except Exception as e:
      logger.error(bstack11111l1l_opy_.format(str(e)))
  if (bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪೂ") in str(bstack1111lll1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1ll1l_opy_
      except Exception as e:
        logger.warn(bstack1ll1ll11_opy_ + str(e))
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1ll1ll11_opy_)
    Output.end_test = bstack11ll1lll_opy_
    TestStatus.__init__ = bstack1lll11ll_opy_
    QueueItem.__init__ = bstack1l1l11lll_opy_
    pabot._create_items = bstack1l111l11l_opy_
    try:
      from pabot import __version__ as bstack1lll1ll11_opy_
      if version.parse(bstack1lll1ll11_opy_) >= version.parse(bstackl_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬೃ")):
        pabot._run = bstack11l1l1_opy_
      elif version.parse(bstack1lll1ll11_opy_) >= version.parse(bstackl_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭ೄ")):
        pabot._run = bstack1l111l_opy_
      else:
        pabot._run = bstack1lll11l_opy_
    except Exception as e:
      pabot._run = bstack1lll11l_opy_
    pabot._create_command_for_execution = bstack1ll1l11l_opy_
    pabot._report_results = bstack1llllllll_opy_
  if bstackl_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ೅") in str(bstack1111lll1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1l1l1l11l_opy_)
    Runner.run_hook = bstack1l11l111l_opy_
    Step.run = bstack1ll111l_opy_
  if bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨೆ") in str(bstack1111lll1_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll1lll1_opy_
      Config.getoption = bstack1l1llllll_opy_
    except Exception as e:
      logger.warn(e, bstack11l111l_opy_)
def bstack111l1ll1_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩೇ") in CONFIG and int(CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪೈ")]) > 1:
    logger.warn(bstack1l1lllll_opy_)
def bstack111l1l1_opy_(bstack1lll11l1_opy_, index):
  bstack11ll11l_opy_(bstack11l111l1_opy_)
  exec(open(bstack1lll11l1_opy_).read())
def bstack11l1l1l_opy_(arg):
  global CONFIG
  bstack11ll11l_opy_(bstack1ll1ll1_opy_)
  os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ೉")] = CONFIG[bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧೊ")]
  os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩೋ")] = CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪೌ")]
  from _pytest.config import main as bstack1ll11l1ll_opy_
  bstack1ll11l1ll_opy_(arg)
def bstack1ll11l1l1_opy_(arg):
  bstack11ll11l_opy_(bstack1l1l1_opy_)
  from behave.__main__ import main as bstack1l1l111l_opy_
  bstack1l1l111l_opy_(arg)
def bstack1l1l1ll1l_opy_():
  logger.info(bstack11ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ್ࠧ"), help=bstackl_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ೎"))
  parser.add_argument(bstackl_opy_ (u"ࠪ࠱ࡺ࠭೏"), bstackl_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ೐"), help=bstackl_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ೑"))
  parser.add_argument(bstackl_opy_ (u"࠭࠭࡬ࠩ೒"), bstackl_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭೓"), help=bstackl_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩ೔"))
  parser.add_argument(bstackl_opy_ (u"ࠩ࠰ࡪࠬೕ"), bstackl_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨೖ"), help=bstackl_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೗"))
  bstack11111l_opy_ = parser.parse_args()
  try:
    bstack11l11111_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ೘")
    if bstack11111l_opy_.framework and bstack11111l_opy_.framework not in (bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೙"), bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ೚")):
      bstack11l11111_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ೛")
    bstack1l11ll1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11111_opy_)
    bstack1lll1l1ll_opy_ = open(bstack1l11ll1l_opy_, bstackl_opy_ (u"ࠩࡵࠫ೜"))
    bstack11ll1l1_opy_ = bstack1lll1l1ll_opy_.read()
    bstack1lll1l1ll_opy_.close()
    if bstack11111l_opy_.username:
      bstack11ll1l1_opy_ = bstack11ll1l1_opy_.replace(bstackl_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪೝ"), bstack11111l_opy_.username)
    if bstack11111l_opy_.key:
      bstack11ll1l1_opy_ = bstack11ll1l1_opy_.replace(bstackl_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ೞ"), bstack11111l_opy_.key)
    if bstack11111l_opy_.framework:
      bstack11ll1l1_opy_ = bstack11ll1l1_opy_.replace(bstackl_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೟"), bstack11111l_opy_.framework)
    file_name = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩೠ")
    file_path = os.path.abspath(file_name)
    bstack1ll1llll_opy_ = open(file_path, bstackl_opy_ (u"ࠧࡸࠩೡ"))
    bstack1ll1llll_opy_.write(bstack11ll1l1_opy_)
    bstack1ll1llll_opy_.close()
    logger.info(bstack11lll111_opy_)
    try:
      os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೢ")] = bstack11111l_opy_.framework if bstack11111l_opy_.framework != None else bstackl_opy_ (u"ࠤࠥೣ")
      config = yaml.safe_load(bstack11ll1l1_opy_)
      config[bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ೤")] = bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪ೥")
      bstack11l1l11_opy_(bstack1111l1ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1l11l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1ll1_opy_.format(str(e)))
def bstack11l1l11_opy_(bstack1l1ll1ll1_opy_, config, bstack111l1l_opy_ = {}):
  global bstack1l11111_opy_
  if not config:
    return
  bstack1l11111ll_opy_ = bstack11llll11_opy_ if not bstack1l11111_opy_ else ( bstack111ll11_opy_ if bstackl_opy_ (u"ࠬࡧࡰࡱࠩ೦") in config else bstack1111ll1_opy_ )
  data = {
    bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ೧"): config[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೨")],
    bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ೩"): config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ೪")],
    bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ೫"): bstack1l1ll1ll1_opy_,
    bstackl_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೬"): {
      bstackl_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೭"): str(config[bstackl_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭೮")]) if bstackl_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ೯") in config else bstackl_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೰"),
      bstackl_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫೱ"): bstack1l1ll1l1l_opy_(os.getenv(bstackl_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧೲ"), bstackl_opy_ (u"ࠦࠧೳ"))),
      bstackl_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ೴"): bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೵"),
      bstackl_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ೶"): bstack1l11111ll_opy_,
      bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೷"): config[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ೸")]if config[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭೹")] else bstackl_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ೺"),
      bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೻"): str(config[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೼")]) if bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೽") in config else bstackl_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ೾"),
      bstackl_opy_ (u"ࠩࡲࡷࠬ೿"): sys.platform,
      bstackl_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬഀ"): socket.gethostname()
    }
  }
  update(data[bstackl_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഁ")], bstack111l1l_opy_)
  try:
    response = bstack1llllll11_opy_(bstackl_opy_ (u"ࠬࡖࡏࡔࡖࠪം"), bstack1ll1l11_opy_, data, config)
    if response:
      logger.debug(bstack1lllll11_opy_.format(bstack1l1ll1ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1111_opy_.format(str(e)))
def bstack1llllll11_opy_(type, url, data, config):
  bstack11ll1111_opy_ = bstack1l1111l1_opy_.format(url)
  proxy = bstack1ll111_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩഃ")) or config.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫഄ")):
    proxies = {
      bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧഅ"): proxy
    }
  if type == bstackl_opy_ (u"ࠩࡓࡓࡘ࡚ࠧആ"):
    response = requests.post(bstack11ll1111_opy_, json=data,
                    headers={bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩഇ"): bstackl_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧഈ")}, auth=(config[bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഉ")], config[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഊ")]), proxies=proxies)
  return response
def bstack1l1ll1l1l_opy_(framework):
  return bstackl_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦഋ").format(str(framework), __version__) if framework else bstackl_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഌ").format(__version__)
def bstack1ll1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l1ll1111_opy_()
    logger.debug(bstack1lll111_opy_.format(str(CONFIG)))
    bstack111lll1l_opy_()
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨ഍") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1l111l_opy_
  atexit.register(bstack1ll11llll_opy_)
  signal.signal(signal.SIGINT, bstack1l1l11l1l_opy_)
  signal.signal(signal.SIGTERM, bstack1l1l11l1l_opy_)
def bstack1ll1l111l_opy_(exctype, value, traceback):
  global bstack1ll1lll11_opy_
  try:
    for driver in bstack1ll1lll11_opy_:
      driver.execute_script(
        bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪഎ") + json.dumps(bstackl_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢഏ") + str(value)) + bstackl_opy_ (u"ࠬࢃࡽࠨഐ"))
  except Exception:
    pass
  bstack1111ll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1111ll_opy_(message = bstackl_opy_ (u"࠭ࠧ഑")):
  global CONFIG
  try:
    if message:
      bstack111l1l_opy_ = {
        bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ഒ"): str(message)
      }
      bstack11l1l11_opy_(bstack1l1ll1l11_opy_, CONFIG, bstack111l1l_opy_)
    else:
      bstack11l1l11_opy_(bstack1l1ll1l11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11l111_opy_.format(str(e)))
def bstack1111l1_opy_(bstack1ll111ll1_opy_, size):
  bstack1l1l1lll_opy_ = []
  while len(bstack1ll111ll1_opy_) > size:
    bstack1ll1111_opy_ = bstack1ll111ll1_opy_[:size]
    bstack1l1l1lll_opy_.append(bstack1ll1111_opy_)
    bstack1ll111ll1_opy_   = bstack1ll111ll1_opy_[size:]
  bstack1l1l1lll_opy_.append(bstack1ll111ll1_opy_)
  return bstack1l1l1lll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack11lll1_opy_)
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫഓ")  or sys.argv[1] == bstackl_opy_ (u"ࠩ࠰ࡺࠬഔ"):
    logger.info(bstackl_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪക").format(__version__))
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪഖ"):
    bstack1l1l1ll1l_opy_()
    return
  args = sys.argv
  bstack1ll1l_opy_()
  global CONFIG
  global bstack111l1111_opy_
  global bstack1lll11ll1_opy_
  global bstack1l111111l_opy_
  global bstack1ll1l1l_opy_
  global bstack1l11l_opy_
  bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠬ࠭ഗ")
  if args[1] == bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ഘ") or args[1] == bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨങ"):
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨച")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨഛ"):
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩജ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪഝ"):
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫഞ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧട"):
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨഠ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨഡ"):
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഢ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪണ"):
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫത")
    args = args[2:]
  else:
    if not bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഥ") in CONFIG or str(CONFIG[bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩദ")]).lower() in [bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧധ"), bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩന")]:
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഩ")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭പ")]).lower() == bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഫ"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫബ")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഭ")]).lower() == bstackl_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭മ"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧയ")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬര")]).lower() == bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪറ"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫല")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨള")]).lower() == bstackl_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ഴ"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧവ")
      args = args[1:]
    else:
      os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪശ")] = bstack11l1l1l1_opy_
      bstack1l11llll1_opy_(bstack11ll1l_opy_)
  global bstack111111l1_opy_
  try:
    os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഷ")] = bstack11l1l1l1_opy_
    bstack11l1l11_opy_(bstack1l1111ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11l111_opy_.format(str(e)))
  global bstack1l1l1llll_opy_
  global bstack11l1ll11_opy_
  global bstack1l1l1l1_opy_
  global bstack11lll1l_opy_
  global bstack1l111l1_opy_
  global bstack1l11l1111_opy_
  global bstack1l1l1l_opy_
  global bstack111llll_opy_
  global bstack1l11ll11_opy_
  global bstack11lll11l_opy_
  global bstack1llll11ll_opy_
  global bstack111ll_opy_
  global bstack111l11l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack111ll1ll_opy_ + str(e))
  bstack1l1l1llll_opy_ = webdriver.Remote.__init__
  bstack111llll_opy_ = WebDriver.close
  try:
    import Browser
    from subprocess import Popen
    bstack111111l1_opy_ = Popen.__init__
  except Exception as e:
    logger.debug(bstack1111ll11_opy_ + str(e))
  bstack1llll11ll_opy_ = WebDriver.get
  if bstack1l1ll1l1_opy_():
    if bstack1l1l1l111_opy_() < version.parse(bstack11ll1l11_opy_):
      logger.error(bstack11ll111_opy_.format(bstack1l1l1l111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11111l1l_opy_.format(str(e)))
  bstack11l1ll1l_opy_()
  if (bstack11l1l1l1_opy_ in [bstackl_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩസ"), bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഹ"), bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ഺ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1ll1l_opy_
      except Exception as e:
        logger.warn(bstack1ll1ll11_opy_ + str(e))
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1ll1ll11_opy_)
    bstack11l1ll11_opy_ = Output.end_test
    bstack1l1l1l1_opy_ = TestStatus.__init__
    bstack1l111l1_opy_ = pabot._run
    bstack1l11l1111_opy_ = QueueItem.__init__
    bstack1l1l1l_opy_ = pabot._create_command_for_execution
  if bstack11l1l1l1_opy_ == bstackl_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ഻࠭"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1l1l1l11l_opy_)
    bstack1l11ll11_opy_ = Runner.run_hook
    bstack11lll11l_opy_ = Step.run
  if bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ഼ࠧ"):
    try:
      from _pytest.config import Config
      bstack111l11l1_opy_ = Config.getoption
    except Exception as e:
      logger.warn(e, bstack11l111l_opy_)
  if bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഽ"):
    bstack1llll1l11_opy_()
    bstack111l1ll1_opy_()
    if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬാ") in CONFIG:
      bstack1lll11ll1_opy_ = True
      bstack1l1l11_opy_ = []
      for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ി")]):
        bstack1l1l11_opy_.append(bstack1ll1l1l11_opy_(name=str(index),
                                      target=bstack111l1l1_opy_, args=(args[0], index)))
      for t in bstack1l1l11_opy_:
        t.start()
      for t in bstack1l1l11_opy_:
        t.join()
    else:
      bstack11ll11l_opy_(bstack11l111l1_opy_)
      exec(open(args[0]).read())
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪീ") or bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫു"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1ll1ll11_opy_)
    bstack1llll1l11_opy_()
    bstack11ll11l_opy_(bstack1l1lll_opy_)
    if bstackl_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫൂ") in args:
      i = args.index(bstackl_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬൃ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack111l1111_opy_))
    args.insert(0, str(bstackl_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ൄ")))
    pabot.main(args)
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൅"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1ll1ll11_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩെ") in a:
        bstack1l111111l_opy_ = int(a.split(bstackl_opy_ (u"ࠫ࠿࠭േ"))[1])
      if bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩൈ") in a:
        bstack1ll1l1l_opy_ = str(a.split(bstackl_opy_ (u"࠭࠺ࠨ൉"))[1])
      if bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧൊ") in a:
        bstack1l11l_opy_ = str(a.split(bstackl_opy_ (u"ࠨ࠼ࠪോ"))[1])
    bstack11ll11l_opy_(bstack1l1lll_opy_)
    run_cli(args)
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩൌ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      import importlib
      bstack1ll1llll1_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱ്ࠬ"))
      if bstack1ll1llll1_opy_ is None:
        logger.warn(bstackl_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨൎ"), bstack11l111l_opy_)
    except Exception as e:
      logger.warn(e, bstack11l111l_opy_)
    bstack1llll1l11_opy_()
    try:
      if bstackl_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ൏") in args:
        i = args.index(bstackl_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ൐"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ൑") in args:
        i = args.index(bstackl_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ൒"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠩ࠰ࡴࠬ൓") in args:
        i = args.index(bstackl_opy_ (u"ࠪ࠱ࡵ࠭ൔ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬൕ") in args:
        i = args.index(bstackl_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ൖ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"࠭࠭࡯ࠩൗ") in args:
        i = args.index(bstackl_opy_ (u"ࠧ࠮ࡰࠪ൘"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1lll1111_opy_ = config.args
    bstack1l111lll1_opy_ = config.invocation_params.args
    bstack1l111lll1_opy_ = list(bstack1l111lll1_opy_)
    bstack1l11ll_opy_ = []
    for arg in bstack1l111lll1_opy_:
      for spec in bstack1lll1111_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1l11ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ൙"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1l1ll_opy_)))
                    for bstack11l1l1ll_opy_ in bstack1lll1111_opy_]
    bstack1llll1l1l_opy_ = bstack111lllll_opy_(CONFIG)
    if (bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ൚") in bstack1llll1l1l_opy_ and str(bstack1llll1l1l_opy_[bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ൛")]).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩ൜")):
      bstack1l11ll_opy_.append(bstackl_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ൝"))
      bstack1l11ll_opy_.append(bstackl_opy_ (u"࠭ࡔࡳࡷࡨࠫ൞"))
    bstack1l11ll_opy_.append(bstackl_opy_ (u"ࠧ࠮ࡲࠪൟ"))
    bstack1l11ll_opy_.append(bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ൠ"))
    bstack1l11ll_opy_.append(bstackl_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫൡ"))
    bstack1l11ll_opy_.append(bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪൢ"))
    bstack111l1_opy_ = []
    for spec in bstack1lll1111_opy_:
      bstack1ll11lll_opy_ = []
      bstack1ll11lll_opy_.append(spec)
      bstack1ll11lll_opy_ += bstack1l11ll_opy_
      bstack111l1_opy_.append(bstack1ll11lll_opy_)
    bstack1lll11ll1_opy_ = True
    bstack1lllll11l_opy_ = 1
    if bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫൣ") in CONFIG:
      bstack1lllll11l_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ൤")]
    bstack11lllll_opy_ = int(bstack1lllll11l_opy_)*int(len(CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൥")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൦")]):
      for bstack1ll11lll_opy_ in bstack111l1_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠨࡣࡵ࡫ࠬ൧")] = bstack1ll11lll_opy_
        item[bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ൨")] = index
        execution_items.append(item)
    bstack1ll1ll111_opy_ = bstack1111l1_opy_(execution_items, bstack11lllll_opy_)
    for execution_item in bstack1ll1ll111_opy_:
      bstack1l1l11_opy_ = []
      for item in execution_item:
        bstack1l1l11_opy_.append(bstack1ll1l1l11_opy_(name=str(item[bstackl_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ൩")]),
                                            target=bstack11l1l1l_opy_,
                                            args=(item[bstackl_opy_ (u"ࠫࡦࡸࡧࠨ൪")],)))
      for t in bstack1l1l11_opy_:
        t.start()
      for t in bstack1l1l11_opy_:
        t.join()
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ൫"):
    try:
      from behave.__main__ import main as bstack1l1l111l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1llll11l1_opy_(e, bstack1l1l1l11l_opy_)
    bstack1llll1l11_opy_()
    bstack1lll11ll1_opy_ = True
    bstack1lllll11l_opy_ = 1
    if bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭൬") in CONFIG:
      bstack1lllll11l_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ൭")]
    bstack11lllll_opy_ = int(bstack1lllll11l_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ൮")]))
    config = Configuration(args)
    bstack1lll1111_opy_ = config.paths
    bstack1l1ll11l1_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1lll1111_opy_:
        bstack1l1ll11l1_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ൯"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1l1ll_opy_)))
                    for bstack11l1l1ll_opy_ in bstack1lll1111_opy_]
    bstack111l1_opy_ = []
    for spec in bstack1lll1111_opy_:
      bstack1ll11lll_opy_ = []
      bstack1ll11lll_opy_ += bstack1l1ll11l1_opy_
      bstack1ll11lll_opy_.append(spec)
      bstack111l1_opy_.append(bstack1ll11lll_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭൰")]):
      for bstack1ll11lll_opy_ in bstack111l1_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠫࡦࡸࡧࠨ൱")] = bstackl_opy_ (u"ࠬࠦࠧ൲").join(bstack1ll11lll_opy_)
        item[bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ൳")] = index
        execution_items.append(item)
    bstack1ll1ll111_opy_ = bstack1111l1_opy_(execution_items, bstack11lllll_opy_)
    for execution_item in bstack1ll1ll111_opy_:
      bstack1l1l11_opy_ = []
      for item in execution_item:
        bstack1l1l11_opy_.append(bstack1ll1l1l11_opy_(name=str(item[bstackl_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭൴")]),
                                            target=bstack1ll11l1l1_opy_,
                                            args=(item[bstackl_opy_ (u"ࠨࡣࡵ࡫ࠬ൵")],)))
      for t in bstack1l1l11_opy_:
        t.start()
      for t in bstack1l1l11_opy_:
        t.join()
  else:
    bstack1l11llll1_opy_(bstack11ll1l_opy_)
  bstack1l11lllll_opy_()
def bstack1l11lllll_opy_():
  global CONFIG
  try:
    if bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ൶") in CONFIG:
      host = bstackl_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭൷") if bstackl_opy_ (u"ࠫࡦࡶࡰࠨ൸") in CONFIG else bstackl_opy_ (u"ࠬࡧࡰࡪࠩ൹")
      user = CONFIG[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨൺ")]
      key = CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪൻ")]
      bstack1lll11111_opy_ = bstackl_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧർ") if bstackl_opy_ (u"ࠩࡤࡴࡵ࠭ൽ") in CONFIG else bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬൾ")
      url = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫൿ").format(user, key, host, bstack1lll11111_opy_)
      headers = {
        bstackl_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ඀"): bstackl_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩඁ"),
      }
      if bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩං") in CONFIG:
        params = {bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ඃ"):CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ඄")], bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭අ"):CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ආ")]}
      else:
        params = {bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ"):CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඈ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1111l111_opy_ = response.json()[0][bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪඉ")]
        if bstack1111l111_opy_:
          bstack1lll1l_opy_ = bstack1111l111_opy_[bstackl_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬඊ")].split(bstackl_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨඋ"))[0] + bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫඌ") + bstack1111l111_opy_[bstackl_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧඍ")]
          logger.info(bstack1l11l1lll_opy_.format(bstack1lll1l_opy_))
          bstack111l1l1l_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨඎ")]
          if bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඏ") in CONFIG:
            bstack111l1l1l_opy_ += bstackl_opy_ (u"ࠧࠡࠩඐ") + CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪඑ")]
          if bstack111l1l1l_opy_!= bstack1111l111_opy_[bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧඒ")]:
            logger.debug(bstack1l1l1111_opy_.format(bstack1111l111_opy_[bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨඓ")], bstack111l1l1l_opy_))
    else:
      logger.warn(bstack1l1ll111l_opy_)
  except Exception as e:
    logger.debug(bstack11llll1_opy_.format(str(e)))
def bstack1l1llll1_opy_(url, bstack1l111ll11_opy_=False):
  global CONFIG
  global bstack11l1ll_opy_
  if not bstack11l1ll_opy_:
    hostname = bstack1l11111l1_opy_(url)
    is_private = bstack1ll11lll1_opy_(hostname)
    if (bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨඔ") in CONFIG and not CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩඕ")]) and (is_private or bstack1l111ll11_opy_):
      bstack11l1ll_opy_ = hostname
def bstack1l11111l1_opy_(url):
  return urlparse(url).hostname
def bstack1ll11lll1_opy_(hostname):
  for bstack11l1l_opy_ in bstack1l1l111ll_opy_:
    regex = re.compile(bstack11l1l_opy_)
    if regex.match(hostname):
      return True
  return False