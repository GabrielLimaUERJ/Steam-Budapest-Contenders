# ==============================
# IMPORTS
# ==============================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import time
import os
from datetime import datetime, timedelta

from steam_market_api import pegar_preco


# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(page_title="CS2 Sticker Analyzer", layout="wide")

st.markdown("""
<style>
    .sticker-card {
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 8px;
        background: #1a1a1a;
        transition: border-color 0.2s;
    }
    .sticker-card:hover { border-color: #555; }
</style>
""", unsafe_allow_html=True)

st.title("CS2 Sticker Analyzer — Budapest 2025")


# ==============================
# ARQUIVO DE HISTÓRICO
# ==============================

HISTORICO_PATH = "historico_stickers.csv"
COLUNAS_HISTORICO = ["timestamp", "nome", "preco_atual", "preco_mediano", "variacao"]


def carregar_historico():
    if os.path.exists(HISTORICO_PATH):
        return pd.read_csv(HISTORICO_PATH, parse_dates=["timestamp"])
    return pd.DataFrame(columns=COLUNAS_HISTORICO)


def salvar_historico(registros: list):
    """Adiciona novos registros ao CSV, evitando duplicatas no mesmo minuto."""
    df_hist = carregar_historico()
    df_novo = pd.DataFrame(registros)
    df_novo["timestamp"] = pd.to_datetime(df_novo["timestamp"])

    if not df_hist.empty:
        df_hist["_chave"] = df_hist["timestamp"].dt.floor("min").astype(str) + df_hist["nome"]
        df_novo["_chave"] = df_novo["timestamp"].dt.floor("min").astype(str) + df_novo["nome"]
        df_novo = df_novo[~df_novo["_chave"].isin(df_hist["_chave"])]
        df_hist.drop(columns="_chave", inplace=True)
        df_novo.drop(columns="_chave", inplace=True)

    df_final = pd.concat([df_hist, df_novo], ignore_index=True)
    df_final.to_csv(HISTORICO_PATH, index=False)


# ==============================
# FUNÇÃO: LIMPAR PREÇO
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
    return float(numeros[0]) if numeros else None


# ==============================
# CACHE DE CONSULTA
# ==============================

@st.cache_data(ttl=120)
def obter_dados(link):
    dados = pegar_preco(link)
    if not dados:
        return None

    preco_atual   = limpar_preco(dados.get("lowest_price"))
    preco_mediano = limpar_preco(dados.get("median_price"))

    if preco_atual is None:
        return None
    if preco_mediano is None:
        preco_mediano = preco_atual

    variacao = ((preco_atual - preco_mediano) / preco_mediano) * 100
    return preco_atual, preco_mediano, variacao


# ==============================
# DICIONÁRIO DE STICKERS
# ==============================

stickers = {
    "Sticker | Lynn Vision (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Lynn%20Vision%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-J765GbgThH10MO0-XAJtqaqOPA4c_WRCDKWmLYv5bZtHn61zB9ysmiBn4z8dy_EOg8-SswnGkq6UaI/330x192?allow_animated=1"
    },
    "Sticker | Lynn Vision (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Lynn%20Vision%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-J765GbvThH-0JOwrnpftqf6OPw8cqaXXWbAwLkjsrkxFy_gwBlz5m6HnNn_dn2XPwE-SswnX505L24/330x192?allow_animated=1"
    },
    "Sticker | FaZe Clan (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FaZe%20Clan%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68obu72bgThH10MbkpCYKvqr2OPM9dfHED2bIw7gm5bZtHn61zB9ysmiBn4z8dy_EOg8-SswnGkq6UaI/330x192?allow_animated=1"
    },
    "Sticker | FaZe Clan (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FaZe%20Clan%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68obu72bvThH-0MO2_HYP6fT6OPY5JKHDWjHJx-pw4rBvGyjrk0R_6mqEmImvdyiRaAY-SswnXWi518g/330x192?allow_animated=1"
    },
    "Sticker | PARIVISION (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20PARIVISION%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65Ibm42bgThH10MDj_iEDvKX7P6JvdvHBCjWRlb8n6OVoGyi3xk0m5mWGwt-ocH7BbQQ-SswnLuWDwvg/330x192?allow_animated=1"
    },
    "Sticker | PARIVISION (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20PARIVISION%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65Ibm42bvThH-0JDkqyBd6fetPvBrdKGXVmLElOog4LIwHH7nkRt3tz-AzNypdiqRbFQ-SswnhypGyf0/330x192?allow_animated=1"
    },
    "Sticker | The Huns (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20The%20Huns%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_JL6-WbgThH10MSwqnoPuPH9OPI4dKOVX2KUk7cg4rdsHS3qxhwl5DyEw979JXqeOAI-SswnsdGEOEU/330x192?allow_animated=1"
    },
    "Sticker | The Huns (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20The%20Huns%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_JL6-WbvThH-0MTjqHJf7PH5MPI0dqXDV2LDwL0ktbhrS3Dilk0ksjuHzdr8IH7GaQY-SswnHNfW4Gg/330x192?allow_animated=1"
    },
    "Sticker | Rare Atom (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Rare%20Atom%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65obg52bgThH10JflqCEDv_P5O_A-IvbAWTKRmb4lsbEwTHrqxBhz6j7cy4v4ciqUPQQ-Sswn5oZAoAs/330x192?allow_animated=1"
    },
    "Sticker | Rare Atom (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Rare%20Atom%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65obg52bvThH-0JW3rCNfvKv-OPc_c6mXXT7Ck7sj57c9G3-2xksjt2vTydj_eXvDPwE-SswnFnUDq9Y/330x192?allow_animated=1"
    },
    "Sticker | RED Canids (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20RED%20Canids%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65oLw6WbgThH10JC2rnAJv6avbvY0cfGQC2GTmOgls7c6TXi1xRgj4D7Rn9ihd3mSa1U-SswnB4XVL3k/330x192?allow_animated=1"
    },
    "Sticker | RED Canids (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20RED%20Canids%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM65oLw6WbvThH-0MbmrnFZuvCvPqA5cqbBVjfJmesjteQ4GH_lzB5z5mTdz46sIHyeOwQ-SswnzYLQlNw/330x192?allow_animated=1"
    },
    "Sticker | FlyQuest (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FlyQuest%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68pbL7VbrRVOnx8G2qnpd66D8OKY4IvTECGPJl7gi5LNsHC_nzEh24TvTzdagdijDcEZ-XWAOwfYS/330x192?allow_animated=1"
    },
    "Sticker | FlyQuest (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FlyQuest%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68pbL4lbrTlP3zsTi-3IM6vaoafY5d_HLDTKUwO0vtOUwS3rhkxkmsD7Uzt2oeHqTcEZ-XedHi_RB/330x192?allow_animated=1"
    },
    "Sticker | M80 (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20M80%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-d-k1V7oTRm_ys-0rXEK7Kr_avE4JqPHWTORkbku5rc4THDgx0oh6mXVmNagIn6RaBhgVMVExNF3oA/330x192?allow_animated=1"
    },
    "Sticker | M80 (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20M80%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-d-k1VHoTRK_ysC3-HIMvaqsOqU1dfSXVjOWlu0m47VtHCrgxkV-sj7SyY2sdSmXbRhgVMWLRdcQAg/330x192?allow_animated=1"
    },
    "Sticker | StarLadder (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20StarLadder%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM655P1-GbgThH10M_mrHACufP_OKc1dqGWDGPAmbsg47RqGn_hkx5w5GvWw92sJSmWbgc-Sswny6ADW94/330x192?allow_animated=1"
    },
    "Sticker | StarLadder (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20StarLadder%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM655P1-GbvThH-0MawqXpa7qH-OvRvcKKRVjKTl70k6LZoG33glh936mjcmd-rd3iSagQ-Sswnp24Xzcg/330x192?allow_animated=1"
    },
    "Sticker | B8 (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20B8%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM69t_L7VbrRVOlycW4_nBf7aKoPPA6IvPBWjHCw74n4Lg7Si-ylktx4WnXmI2peSrBcEZ-XY2Z5yrj/330x192?allow_animated=1"
    },
    "Sticker | B8 (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20B8%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM69t_L4lbrTlP0xpDipHtfuPSqP_Q1d6HCDGLJlrh15eM_TXm3lBwh5W_dmYr8JHiUcEZ-XR8rPMqq/330x192?allow_animated=1"
    },
    "Sticker | fnatic (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20fnatic%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ong6WbgThH10JK2qncKvPb2MPc6JKWXWjXFkusj5-M-GXjqzR5w5TvXyY2rdymUaFQ-SswnnNVunEA/330x192?allow_animated=1"
    },
    "Sticker | fnatic (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20fnatic%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ong6WbvThH-0JC2qXYPvKWqa_Q9I_SQWzfHmb0k4LA4Hyyykx4k4WnVmdqgdXOVPQI-SswnRomjy3g/330x192?allow_animated=1"
    },
    "Sticker | Fluxo (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Fluxo%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ovh8mbgThH10JXlpHJev6f6PPc1cfPFCjLImOshtbQwG3_nw050tm3Wz476J3ySP1U-Sswnd3xEi8U/330x192?allow_animated=1"
    },
    "Sticker | Fluxo (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Fluxo%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM68ovh8mbvThH-0JSwrScMufOsPaI4eKDBWjCVke8j6bIxTS_nxUR25WnWmNioeSqQPFA-SswndDkJYQw/330x192?allow_animated=1"
    },
    "Sticker | NRG (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20NRG%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-pXz1V7oTRm_ncC5-SYO7KH_PvRsI6XBDT_Ak-oitbFoHSq3wBty4TzQn96qd3mTaRhgVMUsKZTsgw/330x192?allow_animated=1"
    },
    "Sticker | NRG (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20NRG%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-pXz1VHoTRK_ncC4rXdZuvH2O_M7JvKQWDbJl7wn6OQxGnGxw0Qj4WXXwt34dnqVOBhgVMWKXOhyYQ/330x192?allow_animated=1"
    },
    "Sticker | Ninjas in Pyjamas (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Ninjas%20in%20Pyjamas%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-o7k1V7oTRm_m5S4_yEPuPP5a_ZueKXCDGbExLoutLg9GnG3wEhx5Gjcydz7dSjGaBhgVMXNNi398A/330x192?allow_animated=1"
    },
    "Sticker | Ninjas in Pyjamas (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Ninjas%20in%20Pyjamas%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-o7k1VHoTRK_zcHlrXYO7qD7MKc9IaHCDzHEmb8utbdvHHuyxUok6j7QzY34c3KSahhgVMWbKc5NHw/330x192?allow_animated=1"
    },
    "Sticker | Imperial Esports (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Imperial%20Esports%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_Yrk1V7oTRm_ysC3-CNd66qrOaFvIaLEVz6Sx74itbJsGizmkRx1t2iAw4n9cXiQahhgVMVTjR9-hA/330x192?allow_animated=1"
    },
    "Sticker | Imperial Esports (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Imperial%20Esports%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6_Yrk1VHoTRK_n5K4pCALvKL5afQ9I_bHDTTBkbsl4LIwTnviwxwi6m3cw9f_eC-TaRhgVMUElpdM_g/330x192?allow_animated=1"
    },
    "Sticker | Legacy (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Legacy%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-ID382bgThH10MW2-XsOuaSoOac7dKbBXzeUw-0j5rA6Tiy3xBgktW-GyY37dn3BZgQ-SswnEnKLNzI/330x192?allow_animated=1"
    },
    "Sticker | Legacy (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Legacy%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM6-ID382bvThH-0JCy_HoNuqH9OvA9dfWVWTLJkrxwtrMwHXyww08h62jUmNn4dHLCPFM-SswnUV0cN7A/330x192?allow_animated=1"
    },
    "Sticker | GamerLegion (Gold) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20GamerLegion%20%28Gold%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM684vL7VbrRVPwn5fkrSAO6av8MPY0I6mWVz7CmLsh6LVqTHC1xUR-sj7Tm9aoc3KRcEZ-XawnX05O/330x192?allow_animated=1"
    },
    "Sticker | GamerLegion (Holo) | Budapest 2025": {
        "link": "https://steamcommunity.com/market/listings/730/Sticker%20%7C%20GamerLegion%20%28Holo%29%20%7C%20Budapest%202025",
        "img":  "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMi0MSnHtwM684vL4lbrTlOiysCx_iAM7fT3MfFuc6LBDTfEk7ggs-A6TH_jwk0m5D_czNqhJXOQcEZ-Xc5gHIYS/330x192?allow_animated=1"
    },
}


# ==============================
# ABAS PRINCIPAIS
# ==============================

aba_analise, aba_historico = st.tabs(["📊 Análise", "📈 Histórico"])


# ==============================
# ABA ANÁLISE
# ==============================

with aba_analise:

    # --- Filtros rápidos ---
    st.subheader("Filtros")
    col_f1, col_f2 = st.columns([1, 2])

    with col_f1:
        filtro_tipo = st.multiselect(
            "Tipo de sticker",
            options=["Gold", "Holo"],
            default=["Gold", "Holo"]
        )
    with col_f2:
        filtro_ordenar = st.selectbox(
            "Ordenar lista por",
            options=["Nome (A-Z)", "Nome (Z-A)"]
        )

    # --- Botões selecionar / limpar ---
    col_s1, col_s2, col_s3 = st.columns([1, 1, 4])
    with col_s1:
        if st.button("☑️ Selecionar todos"):
            for item in stickers.keys():
                tipo = "Gold" if "(Gold)" in item else "Holo"
                if tipo in filtro_tipo:
                    st.session_state[f"chk_{item}"] = True
            st.rerun()
    with col_s2:
        if st.button("✖️ Limpar seleção"):
            for item in stickers.keys():
                st.session_state[f"chk_{item}"] = False
            st.rerun()

    # --- Lista filtrada ---
    def tipo_sticker(nome):
        return "Gold" if "(Gold)" in nome else "Holo"

    stickers_filtrados = [k for k in stickers.keys() if tipo_sticker(k) in filtro_tipo]
    if filtro_ordenar == "Nome (A-Z)":
        stickers_filtrados = sorted(stickers_filtrados)
    else:
        stickers_filtrados = sorted(stickers_filtrados, reverse=True)

    # --- Checkboxes em grid ---
    st.subheader("Escolha os stickers")
    cols = st.columns(4)
    selecionados = []

    for i, item in enumerate(stickers_filtrados):
        chave = f"chk_{item}"
        if chave not in st.session_state:
            st.session_state[chave] = False
        with cols[i % 4]:
            label_curto = item.replace(" | Budapest 2025", "").replace("Sticker | ", "")
            if st.checkbox(label_curto, key=chave):
                selecionados.append(item)

    # --- Imagens dos selecionados ---
    if selecionados:
        st.subheader("Stickers selecionados")
        cols_img = st.columns(4)
        for i, item in enumerate(selecionados):
            with cols_img[i % 4]:
                tipo  = "Gold" if "(Gold)" in item else "Holo"
                cor_b = "#b8960c" if tipo == "Gold" else "#1565c0"
                nome_exib = item.replace(" | Budapest 2025", "").replace(f" ({tipo})", "").replace("Sticker | ", "")
                st.markdown(
                    f"""
                    <a href="{stickers[item]['link']}" target="_blank">
                        <img src="{stickers[item]['img']}" width="150">
                    </a>
                    <p style="font-size:11px; margin:4px 0 8px 0">
                        <span style="background:{cor_b};color:#fff;padding:1px 6px;
                        border-radius:3px;font-size:10px">{tipo}</span>
                        {nome_exib}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

    # --- Busca de dados ---
    dados          = []
    novos_registros = []

    if selecionados:
        with st.spinner("Consultando Steam Market..."):
            for item in selecionados:
                resultado = obter_dados(stickers[item]["link"])
                time.sleep(0.25)
                if resultado:
                    preco_atual, preco_mediano, variacao = resultado
                    dados.append({
                        "Item": item,
                        "Preço Atual": preco_atual,
                        "Preço Mediano 24h": preco_mediano,
                        "Variação %": round(variacao, 2)
                    })
                    novos_registros.append({
                        "timestamp":     datetime.now().isoformat(),
                        "nome":          item,
                        "preco_atual":   preco_atual,
                        "preco_mediano": preco_mediano,
                        "variacao":      round(variacao, 2)
                    })

        if novos_registros:
            salvar_historico(novos_registros)

    # --- Tabela com estilo ---
    if dados:
        df = pd.DataFrame(dados)

        col_ord1, col_ord2 = st.columns([3, 1])
        with col_ord1:
            st.subheader("Tabela de análise")
        with col_ord2:
            ord_tabela = st.selectbox(
                "Ordenar por",
                options=["Item", "Preço Atual ↑", "Preço Atual ↓", "Variação % ↑", "Variação % ↓"]
            )

        if ord_tabela == "Preço Atual ↑":
            df = df.sort_values("Preço Atual")
        elif ord_tabela == "Preço Atual ↓":
            df = df.sort_values("Preço Atual", ascending=False)
        elif ord_tabela == "Variação % ↑":
            df = df.sort_values("Variação %")
        elif ord_tabela == "Variação % ↓":
            df = df.sort_values("Variação %", ascending=False)

        def colorir_variacao(val):
            if val > 0:
                return "color: #00c853; font-weight: bold"
            elif val < 0:
                return "color: #ff5252; font-weight: bold"
            return "color: #aaaaaa"

        st.dataframe(
            df.style.applymap(colorir_variacao, subset=["Variação %"]),
            use_container_width=True,
            hide_index=True
        )

        # --- Alerta de oportunidade ---
        threshold   = st.slider("🚨 Alertar stickers com variação abaixo de (%)", -30, 0, -5)
        oportunidades = df[df["Variação %"] <= threshold]
        if not oportunidades.empty:
            st.warning(
                f"**{len(oportunidades)} sticker(s) com variação ≤ {threshold}%:**\n\n" +
                "\n".join(f"• {row['Item']} → {row['Variação %']}%" for _, row in oportunidades.iterrows())
            )

        # --- Exportar CSV ---
        csv_export = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Exportar tabela como CSV",
            data=csv_export,
            file_name=f"stickers_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

        # --- Gráficos ---
        st.subheader("Gráficos")
        tab_bar, tab_scatter = st.tabs(["📊 Variação %", "🔵 Preço Atual vs Mediano"])

        with tab_bar:
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")
            nomes_curtos = [n.replace(" | Budapest 2025", "").replace("Sticker | ", "") for n in df["Item"]]
            cores = ["#00c853" if x > 0 else "#ff5252" for x in df["Variação %"]]
            bars  = ax.bar(nomes_curtos, df["Variação %"], color=cores, width=0.6)
            ax.axhline(0, linewidth=1, color="#555", alpha=0.8)

            for bar, val in zip(bars, df["Variação %"]):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + (0.3 if val >= 0 else -0.9),
                    f"{val:+.1f}%",
                    ha="center", va="bottom", fontsize=8, color="#cccccc"
                )

            ax.set_ylabel("Variação (%)", color="#cccccc")
            ax.set_title("Variação % em relação ao preço mediano 24h", color="#ffffff")
            plt.xticks(rotation=60, ha="right", color="#cccccc", fontsize=8)
            ax.tick_params(colors="#cccccc")
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)
            ax.spines["left"].set_color("#444")
            ax.spines["bottom"].set_color("#444")
            plt.tight_layout()
            st.pyplot(fig)

        with tab_scatter:
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            fig2.patch.set_alpha(0)
            ax2.set_facecolor("none")
            cores_s = ["#f5c518" if "(Gold)" in n else "#4fc3f7" for n in df["Item"]]
            ax2.scatter(df["Preço Mediano 24h"], df["Preço Atual"], c=cores_s, s=100, zorder=3)

            lim = max(df["Preço Mediano 24h"].max(), df["Preço Atual"].max()) * 1.1
            ax2.plot([0, lim], [0, lim], "--", color="#555", linewidth=1, label="Atual = Mediano")

            for _, row in df.iterrows():
                nome_label = row["Item"].replace(" | Budapest 2025", "").replace("Sticker | ", "")
                ax2.annotate(nome_label, (row["Preço Mediano 24h"], row["Preço Atual"]),
                             textcoords="offset points", xytext=(6, 4), fontsize=7, color="#bbbbbb")

            ax2.set_xlabel("Preço Mediano 24h", color="#cccccc")
            ax2.set_ylabel("Preço Atual", color="#cccccc")
            ax2.set_title("Preço Atual vs Mediano  (🟡 Gold  🔵 Holo)", color="#ffffff")
            ax2.tick_params(colors="#cccccc")
            for spine in ["top", "right"]:
                ax2.spines[spine].set_visible(False)
            ax2.spines["left"].set_color("#444")
            ax2.spines["bottom"].set_color("#444")
            ax2.legend(facecolor="#222", labelcolor="#aaa")
            plt.tight_layout()
            st.pyplot(fig2)


# ==============================
# ABA HISTÓRICO
# ==============================

with aba_historico:

    st.subheader("Histórico de preços")

    df_hist = carregar_historico()

    if df_hist.empty:
        st.info("Nenhum dado histórico ainda. Consulte alguns stickers na aba **Análise** para começar a acumular dados.")
    else:
        df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])

        col_h1, col_h2, col_h3 = st.columns([3, 1, 1])

        with col_h1:
            todos_nomes = sorted(df_hist["nome"].unique().tolist())
            nomes_sel   = st.multiselect(
                "Stickers para exibir",
                options=todos_nomes,
                default=todos_nomes[:5] if len(todos_nomes) >= 5 else todos_nomes
            )
        with col_h2:
            periodo = st.selectbox("Período", ["Tudo", "Últimos 7 dias", "Últimos 30 dias"])
        with col_h3:
            metrica = st.selectbox("Métrica", ["Preço Atual", "Preço Mediano", "Variação %"])

        col_map = {"Preço Atual": "preco_atual", "Preço Mediano": "preco_mediano", "Variação %": "variacao"}
        col_y   = col_map[metrica]

        agora = datetime.now()
        if periodo == "Últimos 7 dias":
            df_hist = df_hist[df_hist["timestamp"] >= agora - timedelta(days=7)]
        elif periodo == "Últimos 30 dias":
            df_hist = df_hist[df_hist["timestamp"] >= agora - timedelta(days=30)]

        df_filtrado = df_hist[df_hist["nome"].isin(nomes_sel)]

        if df_filtrado.empty:
            st.warning("Nenhum dado para os filtros selecionados.")
        else:
            # --- Gráfico de linha temporal ---
            fig3, ax3 = plt.subplots(figsize=(12, 5))
            fig3.patch.set_alpha(0)
            ax3.set_facecolor("none")

            paleta = [
                "#f5c518","#4fc3f7","#ff5252","#00c853","#ce93d8",
                "#ffb74d","#80cbc4","#ef9a9a","#aed581","#80deea",
                "#ffcc02","#b39ddb","#f48fb1","#a5d6a7","#90caf9"
            ]

            for idx, nome in enumerate(nomes_sel):
                df_nome = df_filtrado[df_filtrado["nome"] == nome].sort_values("timestamp")
                if df_nome.empty:
                    continue
                cor = paleta[idx % len(paleta)]
                nome_curto = nome.replace(" | Budapest 2025", "").replace("Sticker | ", "")
                ax3.plot(df_nome["timestamp"], df_nome[col_y],
                         marker="o", markersize=4, linewidth=1.8,
                         color=cor, label=nome_curto)

            ax3.set_ylabel(metrica, color="#cccccc")
            ax3.set_title(f"{metrica} ao longo do tempo", color="#ffffff")
            ax3.tick_params(colors="#cccccc")
            ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
            plt.xticks(rotation=45, ha="right", color="#cccccc", fontsize=8)

            for spine in ["top", "right"]:
                ax3.spines[spine].set_visible(False)
            ax3.spines["left"].set_color("#444")
            ax3.spines["bottom"].set_color("#444")

            if len(nomes_sel) <= 10:
                ax3.legend(facecolor="#1a1a1a", labelcolor="#cccccc", fontsize=8, loc="upper left")

            if col_y == "variacao":
                ax3.axhline(0, linewidth=1, color="#555", linestyle="--")

            plt.tight_layout()
            st.pyplot(fig3)

            # --- Variação acumulada ---
            st.subheader("Variação acumulada desde a primeira consulta (%)")

            registros_acum = []
            for nome in nomes_sel:
                df_nome = df_filtrado[df_filtrado["nome"] == nome].sort_values("timestamp")
                if len(df_nome) < 2:
                    continue
                preco_ini = df_nome.iloc[0]["preco_atual"]
                preco_fin = df_nome.iloc[-1]["preco_atual"]
                if preco_ini and preco_ini != 0:
                    var_acum = ((preco_fin - preco_ini) / preco_ini) * 100
                    registros_acum.append({
                        "Sticker":               nome.replace(" | Budapest 2025", "").replace("Sticker | ", ""),
                        "Primeiro preço":        preco_ini,
                        "Último preço":          preco_fin,
                        "Variação acumulada %":  round(var_acum, 2),
                        "Nº de registros":       len(df_nome)
                    })

            if registros_acum:
                df_acum = pd.DataFrame(registros_acum).sort_values("Variação acumulada %", ascending=False)

                def colorir_acum(val):
                    if val > 0:   return "color: #00c853; font-weight: bold"
                    elif val < 0: return "color: #ff5252; font-weight: bold"
                    return "color: #aaaaaa"

                st.dataframe(
                    df_acum.style.applymap(colorir_acum, subset=["Variação acumulada %"]),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Registros insuficientes para calcular variação acumulada (mínimo 2 consultas por sticker).")

            # --- Exportar histórico ---
            csv_hist = df_hist.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Exportar histórico completo como CSV",
                data=csv_hist,
                file_name=f"historico_stickers_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
