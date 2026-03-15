import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

from steam_market_api import pegar_preco

st.set_page_config(page_title="CS2 Sticker Analyzer", layout="wide")

st.title("CS2 Sticker Analyzer — Budapest 2025")


# ==============================
# LIMPAR PREÇO
# ==============================

def limpar_preco(preco):

    if preco is None:
        return None

    preco = (
        preco.replace("$", "")
        .replace("€", "")
        .replace("R$", "")
        .replace(",", ".")
    )

    numeros = re.findall(r"\d+\.?\d*", preco)

    if numeros:
        return float(numeros[0])

    return None


# ==============================
# CACHE
# ==============================

@st.cache_data(ttl=600)
def obter_dados(link):

    dados = pegar_preco(link)

    if not dados:
        return None

    preco_atual = limpar_preco(dados["lowest_price"])
    preco_mediano = limpar_preco(dados["median_price"])

    if preco_atual is None or preco_mediano is None:
        return None

    variacao = ((preco_atual - preco_mediano) / preco_mediano) * 100

    return preco_atual, preco_mediano, variacao


# ==============================
# LISTA DE STICKERS
# ==============================

stickers = {

"Sticker | Lynn Vision (Gold) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Lynn%20Vision%20%28Gold%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-J765GbgThH10MO0-XAJtqaqOPA4c_WRCDKWmLYv5bZtHn61zB9ysmiBn4z8dy_EOg8-SswnGkq6UaI/330x192?allow_animated=1"
},

"Sticker | Lynn Vision (Holo) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Lynn%20Vision%20%28Holo%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-J765GbvThH-0JOwrnpftqf6OPw8cqaXXWbAwLkjsrkxFy_gwBlz5m6HnNn_dn2XPwE-SswnX505L24/330x192?allow_animated=1"
},

"Sticker | FaZe Clan (Gold) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FaZe%20Clan%20%28Gold%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68obu72bgThH10MbkpCYKvqr2OPM9dfHED2bIw7gm5bdoTXrjl0twtT-AnNerInKVZgI-SswnU7w2rh4/330x192?allow_animated=1"
},

"Sticker | FaZe Clan (Holo) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FaZe%20Clan%20%28Holo%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68obu72bvThH-0MO2_HYP6fT6OPY5JKHDWjHJx-pw4rBvGyjrk0R_6mqEmImvdyiRaAY-SswnXWi518g/330x192?allow_animated=1"
},

"Sticker | PARIVISION (Gold) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20PARIVISION%20%28Gold%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65Ibm42bgThH10MDj_iEDvKX7P6JvdvHBCjWRlb8n6OVoGyi3xk0m5mWGwt-ocH7BbQQ-SswnLuWDwvg/330x192?allow_animated=1"
},

"Sticker | PARIVISION (Holo) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20PARIVISION%20%28Holo%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65Ibm42bvThH-0JDkqyBd6fetPvBrdKGXVmLElOog4LIwHH7nkRt3tz-AzNypdiqRbFQ-SswnhypGyf0/330x192?allow_animated=1"
},

"Sticker | The Huns (Gold) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20The%20Huns%20%28Gold%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_JL6-WbgThH10MSwqnoPuPH9OPI4dKOVX2KUk7cg4rdsHS3qxhwl5DyEw979JXqeOAI-SswnsdGEOEU/330x192?allow_animated=1"
},

"Sticker | The Huns (Holo) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20The%20Huns%20%28Holo%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_JL6-WbvThH-0MTjqHJf7PH5MPI0dqXDV2LDwL0ktbhrS3Dilk0ksjuHzdr8IH7GaQY-SswnHNfW4Gg/330x192?allow_animated=1"
},

"Sticker | Rare Atom (Gold) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Rare%20Atom%20%28Gold%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65obg52bgThH10JflqCEDv_P5O_A-IvbAWTKRmb4lsbEwTHrqxBhz6j7cy4v4ciqUPQQ-Sswn5oZAoAs/330x192?allow_animated=1"
},

"Sticker | Rare Atom (Holo) | Budapest 2025":{
"link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Rare%20Atom%20%28Holo%29%20%7C%20Budapest%202025",
"img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65obg52bvThH-0JW3rCNfvKv-OPc_c6mXXT7Ck7sj57c9G3-2xksjt2vTydj_eXvDPwE-SswnFnUDq9Y/330x192?allow_animated=1"
},

"Sticker | RED Canids (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20RED%20Canids%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65oLw6WbgThH10JC2rnAJv6avbvY0cfGQC2GTmOgls7c6TXi1xRgj4D7Rn9ihd3mSa1U-SswnB4XVL3k/330x192?allow_animated=1"},

"Sticker | RED Canids (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20RED%20Canids%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65oLw6WbvThH-0MbmrnFZuvCvPqA5cqbBVjfJmesjteQ4GH_lzB5z5mTdz46sIHyeOwQ-SswnzYLQlNw/330x192?allow_animated=1"},

"Sticker | FlyQuest (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FlyQuest%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68pbL7VbrRVOnx8G2qnpd66D8OKY4IvTECGPJl7gi5LNsHC_nzEh24TvTzdagdijDcEZ-XWAOwfYS/330x192?allow_animated=1"},

"Sticker | FlyQuest (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FlyQuest%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68pbL4lbrTlP3zsTi-3IM6vaoafY5d_HLDTKUwO0vtOUwS3rhkxkmsD7Uzt2oeHqTcEZ-XedHi_RB/330x192?allow_animated=1"},

"Sticker | M80 (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20M80%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-d-k1V7oTRm_ys-0rXEK7Kr_avE4JqPHWTORkbku5rc4THDgx0oh6mXVmNagIn6RaBhgVMVExNF3oA/330x192?allow_animated=1"},

"Sticker | M80 (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20M80%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-d-k1VHoTRK_ysC3-HIMvaqsOqU1dfSXVjOWlu0m47VtHCrgxkV-sj7SyY2sdSmXbRhgVMWLRdcQAg/330x192?allow_animated=1"},

"Sticker | StarLadder (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20StarLadder%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM655P1-GbgThH10M_mrHACufP_OKc1dqGWDGPAmbsg47RqGn_hkx5w5GvWw92sJSmWbgc-Sswny6ADW94/330x192?allow_animated=1"},

"Sticker | StarLadder (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20StarLadder%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM655P1-GbvThH-0MawqXpa7qH-OvRvcKKRVjKTl70k6LZoG33glh936mjcmd-rd3iSagQ-Sswnp24Xzcg/330x192?allow_animated=1"},

"Sticker | B8 (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20B8%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM69t_L7VbrRVOlycW4_nBf7aKoPPA6IvPBWjHCw74n4Lg7Si-ylktx4WnXmI2peSrBcEZ-XY2Z5yrj/330x192?allow_animated=1"},

"Sticker | B8 (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20B8%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM69t_L4lbrTlP0xpDipHtfuPSqP_Q1d6HCDGLJlrh15eM_TXm3lBwh5W_dmYr8JHiUcEZ-XR8rPMqq/330x192?allow_animated=1"},

"Sticker | fnatic (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20fnatic%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ong6WbgThH10JK2qncKvPb2MPc6JKWXWjXFkusj5-M-GXjqzR5w5TvXyY2rdymUaFQ-SswnnNVunEA/330x192?allow_animated=1"},

"Sticker | fnatic (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20fnatic%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ong6WbvThH-0JC2qXYPvKWqa_Q9I_SQWzfHmb0k4LA4Hyyykx4k4WnVmdqgdXOVPQI-SswnRomjy3g/330x192?allow_animated=1"},

"Sticker | Fluxo (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Fluxo%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ovh8mbgThH10JXlpHJev6f6PPc1cfPFCjLImOshtbQwG3_nw050tm3Wz476J3ySP1U-Sswnd3xEi8U/330x192?allow_animated=1"},

"Sticker | Fluxo (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Fluxo%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ovh8mbvThH-0JSwrScMufOsPaI4eKDBWjCVke8j6bIxTS_nxUR25WnWmNioeSqQPFA-SswndDkJYQw/330x192?allow_animated=1"},

"Sticker | NRG (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20NRG%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-pXz1V7oTRm_ncC5-SYO7KH_PvRsI6XBDT_Ak-oitbFoHSq3wBty4TzQn96qd3mTaRhgVMUsKZTsgw/330x192?allow_animated=1"},

"Sticker | NRG (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20NRG%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-pXz1VHoTRK_ncC4rXdZuvH2O_M7JvKQWDbJl7wn6OQxGnGxw0Qj4WXXwt34dnqVOBhgVMWKXOhyYQ/330x192?allow_animated=1"},

"Sticker | Ninjas in Pyjamas (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Ninjas%20in%20Pyjamas%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-o7k1V7oTRm_m5S4_yEPuPP5a_ZueKXCDGbExLoutLg9GnG3wEhx5Gjcydz7dSjGaBhgVMXNNi398A/330x192?allow_animated=1"},

"Sticker | Ninjas in Pyjamas (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Ninjas%20in%20Pyjamas%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-o7k1VHoTRK_zcHlrXYO7qD7MKc9IaHCDzHEmb8utbdvHHuyxUok6j7QzY34c3KSahhgVMWbKc5NHw/330x192?allow_animated=1"},

"Sticker | Imperial Esports (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Imperial%20Esports%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_Yrk1V7oTRm_ysC3-CNd66qrOaFvIaLEVz6Sx74itbJsGizmkRx1t2iAw4n9cXiQahhgVMVTjR9-hA/330x192?allow_animated=1"},

"Sticker | Imperial Esports (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Imperial%20Esports%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_Yrk1VHoTRK_n5K4pCALvKL5afQ9I_bHDTTBkbsl4LIwTnviwxwi6m3cw9f_eC-TaRhgVMUElpdM_g/330x192?allow_animated=1"},

"Sticker | Legacy (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Legacy%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-ID382bgThH10MW2-XsOuaSoOac7dKbBXzeUw-0j5rA6Tiy3xBgktW-GyY37dn3BZgQ-SswnEnKLNzI/330x192?allow_animated=1"},

"Sticker | Legacy (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Legacy%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-ID382bvThH-0JCy_HoNuqH9OvA9dfWVWTLJkrxwtrMwHXyww08h62jUmNn4dHLCPFM-SswnUV0cN7A/330x192?allow_animated=1"},

"Sticker | GamerLegion (Gold) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20GamerLegion%20%28Gold%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM684vL7VbrRVPwn5fkrSAO6av8MPY0I6mWVz7CmLsh6LVqTHC1xUR-sj7Tm9aoc3KRcEZ-XawnX05O/330x192?allow_animated=1"},

"Sticker | GamerLegion (Holo) | Budapest 2025":{ "link":"https://steamcommunity.com/market/listings/730/Sticker%20%7C%20GamerLegion%20%28Holo%29%20%7C%20Budapest%202025","img":"https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM684vL4lbrTlOiysCx_iAM7fT3MfFuc6LBDTfEk7ggs-A6TH_jwk0m5D_czNqhJXOQcEZ-Xc5gHIYS/330x192?allow_animated=1"}

}


# ==============================
# CHECKBOX GRID
# ==============================

st.subheader("Escolha os stickers")

selecionados = []

cols = st.columns(4)

for i, item in enumerate(stickers):

    with cols[i % 4]:

        if st.checkbox(item):

            selecionados.append(item)


# ==============================
# MOSTRAR IMAGENS
# ==============================

if selecionados:

    st.subheader("Stickers selecionados")

    cols = st.columns(4)

    for i, item in enumerate(selecionados):

        with cols[i % 4]:

            st.markdown(
                f"""
                <a href="{stickers[item]['link']}" target="_blank">
                    <img src="{stickers[item]['img']}" width="150">
                </a>
                <p style="font-size:12px">{item}</p>
                """,
                unsafe_allow_html=True
            )


# ==============================
# BUSCAR DADOS
# ==============================

dados = []

for item in selecionados:

    resultado = obter_dados(stickers[item]["link"])

    if resultado:

        preco_atual, preco_mediano, variacao = resultado

        dados.append({
            "Item": item,
            "Preço Atual": preco_atual,
            "Preço Mediano 24h": preco_mediano,
            "Variação %": round(variacao,2)
        })


# ==============================
# TABELA + GRÁFICO
# ==============================

if dados:

    df = pd.DataFrame(dados)

    st.subheader("Tabela de análise")

    st.dataframe(df)

    st.subheader("Variação percentual")

    fig, ax = plt.subplots()

    cores = ["green" if x > 0 else "red" for x in df["Variação %"]]

    ax.bar(df["Item"], df["Variação %"], color=cores)

    ax.axhline(0)

    ax.set_ylabel("Variação (%)")

    plt.xticks(rotation=90)

    st.pyplot(fig)
