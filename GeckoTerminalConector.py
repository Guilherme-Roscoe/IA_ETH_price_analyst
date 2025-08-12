from web3 import Web3
from eth_utils import to_checksum_address

RPC_URL = "https://mainnet.base.org"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

PAIR_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
            {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
            {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"},
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

DECIMAL_ABI = [{
    "constant": True,
    "inputs": [],
    "name": "decimals",
    "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
    "stateMutability": "view",
    "type": "function"
}]

# Endereços conhecidos
DEX_PAIRS = {
    "Uniswap V2": "0x88a43bbdf9d098eec7bceda4e2494615dfd9bb9c",
    "PancakeSwap V3": "0x72ab388e2e2f6facef59e3c3fa2c4e29011c2d38",
    "AeroDrome": "0xb2cc224c1c9fee385f8ad6a55b4d94e92359dc59"
}

def fetch_price(pair_addr):
    pair = w3.eth.contract(address=to_checksum_address(pair_addr), abi=PAIR_ABI)
    r0, r1, _ = pair.functions.getReserves().call()
    t0 = pair.functions.token0().call()
    t1 = pair.functions.token1().call()
    decimals0 = w3.eth.contract(address=t0, abi=DECIMAL_ABI).functions.decimals().call()
    decimals1 = w3.eth.contract(address=t1, abi=DECIMAL_ABI).functions.decimals().call()
    
    reserve0 = r0 / (10 ** decimals0)
    reserve1 = r1 / (10 ** decimals1)
    return reserve1 / reserve0  # USDC per WETH

prices = {}
for dex, addr in DEX_PAIRS.items():
    if "ENDEREÇO_A_OBTER" in addr:
        prices[dex] = None
        print(f"[Aguardando endereço de par para {dex}]")
    else:
        try:
            prices[dex] = fetch_price(addr)
        except Exception as e:
            prices[dex] = None
            print(f"Erro ao buscar preço no {dex}: {e}")

# Ordena preços disponíveis
ordered = sorted(
    [(dex, price) for dex, price in prices.items() if price is not None],
    key=lambda x: x[1],
    reverse=True
)

print("\nPreços (USDC por WETH) — do mais caro ao mais barato:")
for dex, price in ordered:
    print(f"{dex}: {price:.2f}")
