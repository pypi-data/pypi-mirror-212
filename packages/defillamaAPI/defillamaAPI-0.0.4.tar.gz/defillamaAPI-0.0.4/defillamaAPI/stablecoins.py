from .defillamaAPI import Base

STABLECOINS_BASE_URL = "https://stablecoins.llama.fi"
class Stablecoins(Base):
    """ """
    
    def get_all_stablecoins(self, includePrices=None):
        """Description: List all stablecoins along with their circulating amounts"""
        path = '/stablecoins'
        params = {}
        if includePrices: params.update({"includePrices": includePrices})
        return self._send_request(method="GET", endpoint=path, base_url=STABLECOINS_BASE_URL, params=params)

    def get_all_stablecoins_charts(self, stablecoin=None):
        """Description: Get historical mcap sum of all stablecoins"""
        path = '/stablecoincharts/all'
        params = {}
        if stablecoin: params.update({"stablecoin": stablecoin})
        return self._send_request(method="GET", endpoint=path, base_url=STABLECOINS_BASE_URL, params=params)
    
    def get_stablecoincharts(self, chain, stablecoin):
        """Description: Get historical mcap sum of all stablecoins in a chain"""
        path = f"/stablecoincharts/{chain}"
        params = {}
        if stablecoin: params.update({"stablecoin": stablecoin})
        return self._send_request(method="GET", endpoint=path, base_url=STABLECOINS_BASE_URL, params=params)

    def get_stablecoin_asset(self, asset):
        """Description: Get historical mcap and historical chain distribution of a stablecoin"""
        path = f'/stablecoin/{asset}'
        return self._send_request(method="GET", endpoint=path, base_url=STABLECOINS_BASE_URL)

    def get_stablecoinchains(self):
        """Description: Get current mcap sum of all stablecoins on each chain"""
        path = '/stablecoinchains'
        return self._send_request(method="GET", endpoint=path, base_url=STABLECOINS_BASE_URL)

    def get_stablecoinprices(self):
        """Description: Get historical prices of all stablecoins"""
        path = '/stablecoinprices'
        return self._send_request(method="GET", endpoint=path, base_url=STABLECOINS_BASE_URL)
