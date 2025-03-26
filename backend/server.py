
from fastapi import FastAPI, Query, HTTPException
import uvicorn
from pydantic import BaseModel
from db import ASSET_TYPES, HOLDINGS, ASSETS
from typing import Union
from account_utilities import getAllUserAssets, getTotalUserAccountValue, getUserExist
from response_utilities import throwInvalidParameter,throwUserNotFound,throwNullParameter

class PortfolioChart(BaseModel):
    total_value : int
    chart : dict[str, Union[int,float]]

class PortfolioHoldings(BaseModel):
    holdings : list[dict[str, Union[str,int,float]]]

app = FastAPI()

@app.get("/portfolio-chart", response_model=PortfolioChart)
def read_portfolio_chart(user_id : str = Query(...)) -> PortfolioChart:
    # validating input isnt null for clear instructions
    if not user_id:
        throwNullParameter("user id")
    # creating empty class for return value
    portfolioData =  PortfolioChart(
        total_value=0,
        chart={item: 0 for item in ASSET_TYPES}
    )
    # sanity check to ensure user is in db
    if not getUserExist(user_id):
        throwUserNotFound()
    # sanity check to ensure there are populated wallets for the user
    if len(HOLDINGS[user_id]) == 0:
        raise HTTPException(status_code=404,detail=f"NO WALLETS FOUND FOR {user_id}")
    # getting total user balance
    user_total_balance = getTotalUserAccountValue(user_id)
    # finding all assets the user owns 
    user_assets = getAllUserAssets(user_id)
    # if the len is 0, the user doesnt own anything ;( so we can return an empty object
    if len(user_assets) == 0:
        return portfolioData 
    # iterating through wallets
    for asset in user_assets:
        # iterating through assets to access total values and allocate to correct types
        asset_type = ASSETS[asset["asset_id"]]["type"]
        # assinging the values to portfolioData
        portfolioData.chart[asset_type] += asset["amount"]
    
    # once we have all totals for each type, we can calculate percentages
    for asset_type,amount in portfolioData.chart.items():
        portfolioData.chart[asset_type] = round((amount/user_total_balance)*100,2)

    # finding total value
    portfolioData.total_value = getTotalUserAccountValue(user_id)
    return portfolioData


@app.get("/portfolio-holdings")
def read_portfolio_holdings(user_id : str = Query(...), asset_type : str = Query(None)) -> PortfolioHoldings:
    # validing input params
    if not user_id:
        throwNullParameter("user id")
    # validating the asset type (opt) is actually in our types
    if asset_type and asset_type not in ASSET_TYPES:
        throwInvalidParameter(asset_type)
    # sanity check for user existing
    if not getUserExist(user_id):
        throwUserNotFound()

    # creating a list for holding data 
    holding_data = []

    # creating a blank dict to merge additional data into existing asset type info
    asset_value_info = {
        "value" : 0,
        "percentage" : 0
    }
    # getting the user total balance
    user_total_balance = getTotalUserAccountValue(user_id)
    # getting all user assets
    user_assets = getAllUserAssets(user_id)

    # iterating through assets
    for asset in user_assets:
        # filterting present?
        if asset_type:
            # matching asset type (if given)
            if ASSETS[asset["asset_id"]]["type"] != asset_type:
                continue
        # finding percent of total assets for iteration
        percent_of_total = round((asset["amount"]/user_total_balance)*100,2)
        # filling asset value info
        asset_value_info["percentage"] = percent_of_total
        asset_value_info["value"] = asset["amount"]
        # merging asset info dict with value info dict
        holding_item = {**ASSETS[asset["asset_id"]],**asset_value_info}
        # appending to master list
        holding_data.append(holding_item)
    # instantiating portfolio class for returning value 
    portfolioHoldingData = PortfolioHoldings(holdings=holding_data)
    return portfolioHoldingData


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5050, log_level="info")
