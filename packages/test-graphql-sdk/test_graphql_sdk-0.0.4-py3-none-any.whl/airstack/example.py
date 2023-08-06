import asyncio
from execute_query import AirstackClient


async def main():
    api_client = AirstackClient(api_key='V9lLckJMWO2emvuRwEH3UaTIkAzcXARt9TVh8XRN')

    query1 = """
 query MyQuery($name1: Address!, $name2: Address!) {
  TokenBalances(
    input: {filter: {tokenAddress: {_eq: $name1}}, blockchain: ethereum}
  ) {
    pageInfo {
      nextCursor
      prevCursor
    }
    TokenBalance {
      chainId
      blockchain
      amount
      lastUpdatedTimestamp
      id
    }
  }
  test2: TokenTransfers(
    input: {filter: {tokenAddress: {_eq: $name2}}, blockchain: ethereum}
  ) {
    pageInfo {
      nextCursor
      prevCursor
    }
    TokenTransfer {
      chainId
      blockchain
      id
      amount
    }
  }
}
  """
    variables1 = {
        "name1": "0x1130547436810db920fa73681c946fea15e9b758",
        "name2": "0xf4eced2f682ce333f96f2d8966c613ded8fc95dd",
    }

    response, status_code, error, has_next_page, has_prev_page, get_next_page, get_prev_page = await api_client.execute_paginated_query(
        query=query1, variables=variables1)

    if has_next_page:
        next_page_response, next_page_status, next_page_error, has_next_page, has_prev_page, get_next_page, get_prev_page = await get_next_page()
    if has_prev_page:
        next_page_response, next_page_status, next_page_error, has_next_page, has_prev_page, get_next_page, get_prev_page = await get_prev_page()

    query = """
     query MyQuery($name1: Address!) {
      test1: TokenBalances(
        input: {filter: {tokenAddress: {_eq: $name1}}, blockchain: ethereum}
      ) {
        pageInfo {
          nextCursor
          prevCursor
        }
        TokenBalance {
          chainId
          blockchain
          amount
          lastUpdatedTimestamp
          id
        }
      }
    }
      """
    variables = {
        "name1": "0x1130547436810db920fa73681c946fea15e9b758",
    }

    # Process the next page response
    if error:
        print(f"Error: {error}")
    else:
        print(f"Response: {response}")

    response, status_code, error = await api_client.execute_query(query=query, variables=variables)

    # Process the next page response
    if error:
        print(f"Error: {error}")
    else:
        print(f"Response: {response}")


asyncio.run(main())
