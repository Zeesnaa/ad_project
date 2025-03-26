from db import ASSET_TYPES, ASSETS, HOLDINGS


def getUserExist(user_id : str) -> bool:
    if user_id not in HOLDINGS:
        return False
    else: 
        return True


def getUserWallets(user_id : str) -> dict:
    user_wallets = HOLDINGS[user_id]
    return user_wallets

# sorted decending by default
def getAllUserAssets(user_id : str) -> list:
    user_assets = []
    user_wallets = getUserWallets(user_id)
    # iterating through wallets -> assets
    for wallet_index,wallet_assets in user_wallets.items():
        for asset in wallet_assets:
            user_assets.append(asset)
    # sorting with built in func 
    user_assets_sorted = sorted(user_assets,key=lambda x: x["amount"],reverse=True)
    return user_assets_sorted

def getTotalUserAccountValue(user_id : str) -> int:
    total_balance = 0
    user_assets = getAllUserAssets(user_id)
    for asset in user_assets:
        total_balance += asset["amount"]
    return total_balance


getAllUserAssets("user_1")