import unittest
from entities import SmartupCredentials, SmartupOrderFilters
from clients import SmartupExtractionClient

credentials = SmartupCredentials(
  host="https://smartup.online",
  client_id="E1C2D00EE524E123B3DCE9124E809E97",
  client_secret="F2D756E462791D840254113DB18388745B66F300DFDCB3F0F21D5E3844262CC9D28972B468F157A1B5EB7C48CF625C019D00C4006FAF41F35D77F4B7DF515A73",
)

filters = SmartupOrderFilters()

smartupClient = SmartupExtractionClient()

class TestSmartupExtractionClient(unittest.TestCase):
    def test_extraction(self):
      deals = smartupClient.extractDeals(credentials=credentials, filters=filters)

      print(deals)

if __name__ == '__main__':
  unittest.main()
