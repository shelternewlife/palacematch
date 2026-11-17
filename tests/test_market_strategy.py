import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
STRATEGY = json.loads((ROOT / "content/market-strategy.json").read_text(encoding="utf-8"))

class MarketStrategyTests(unittest.TestCase):
    def test_north_america_is_first_priority(self):
        markets = {item["country_code"]: item for item in STRATEGY["markets"]}
        self.assertEqual(markets["US"]["priority"], 1)
        self.assertEqual(markets["CA"]["priority"], 1)
        self.assertEqual(markets["US"]["locales"], ["en-US"])
        self.assertEqual(set(markets["CA"]["locales"]), {"en-CA", "fr-CA"})

    def test_all_european_market_entries_are_secondary(self):
        markets = [item for item in STRATEGY["markets"] if item["priority"] == 2]
        self.assertGreaterEqual(len(markets), 45)
        self.assertEqual(len({item["country_code"] for item in markets}), len(markets))
        self.assertTrue(all(item["status"] in ("planned", "initial") for item in markets))
        self.assertEqual({item["country_code"] for item in markets if item["status"] == "initial"}, {"ES", "PT", "FR", "DE", "IT"})
        self.assertTrue(all(item["locales"] for item in markets))

    def test_locale_tags_and_url_policy_are_explicit(self):
        locales = [locale for market in STRATEGY["markets"] for locale in market["locales"]]
        self.assertEqual(len(locales), len(set(locales)))
        self.assertTrue(all(re.fullmatch(r"[a-z]{2,3}-[A-Z]{2}", locale) for locale in locales))
        policy = STRATEGY["url_policy"]
        self.assertEqual(policy["pattern"], "/{locale}/")
        self.assertIn("reciprocal hreflang", policy["hreflang"])
        self.assertIn("Untranslated locales remain unpublished", policy["fallback"])

    def test_keyword_seeds_exist_for_initial_markets_without_volume_claims(self):
        clusters = STRATEGY["initial_keyword_clusters"]
        self.assertTrue({"en-US", "en-CA", "fr-CA"}.issubset(clusters))
        for locale, data in clusters.items():
            self.assertTrue(data["clusters"], locale)
            for cluster in data["clusters"]:
                self.assertTrue(cluster["primary"], locale)
        self.assertIn("Not supplied or verified", STRATEGY["measurement"]["search_volume"])

    def test_european_research_covers_multiple_local_languages(self):
        examples = STRATEGY["europe_keyword_research"]["examples"]
        self.assertTrue({"fr-FR", "de-DE", "es-ES", "it-IT", "nl-NL", "pl-PL", "en-GB"}.issubset(examples))
        self.assertEqual(STRATEGY["europe_keyword_research"]["status"], "research-seeds-only")

if __name__ == "__main__":
    unittest.main()
