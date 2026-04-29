"""CLI for PulseCheck article analysis."""

import argparse
import json
import sys

# Ensure Windows console can print emojis and native script names
sys.stdout.reconfigure(encoding='utf-8')

from pulsecheck.pipeline import analyze


def main():
    parser = argparse.ArgumentParser(description="Analyze news article for political bias")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL of news article")
    group.add_argument("--text", help="Raw article text to analyze directly")
    parser.add_argument("--summarize", action="store_true", help="Include summary in output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--lang",
        default=None,
        help="Override language detection with ISO-639-1 code (e.g. hi, fr, ar)",
    )
    
    args = parser.parse_args()
    
    try:
        result = analyze(
            url=args.url,
            text=args.text,
            summarize_article=args.summarize,
            language_override=args.lang,
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*60}")
            print(f"Source: {result['source']}")
            if result.get('headline'):
                print(f"Headline: {result['headline']}")
                # Show original headline if it differs (translated)
                if (
                    result.get("original_headline")
                    and result["original_headline"] != result["headline"]
                ):
                    print(f"Original Headline: {result['original_headline']}")
            print(f"{'='*60}")

            # Language info
            lang_flag = result.get("language_flag", "🌍")
            lang_name = result.get("language", "English")
            lang_conf = result.get("language_confidence", "")
            print(f"Language: {lang_flag} {lang_name} (confidence: {lang_conf})")
            if result.get("is_translated"):
                print("  → Translated to English for analysis")

            print(f"\nBias: {result['bias'].upper()}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Sentiment: {result['sentiment'].upper()} (polarity: {result['polarity']:.2f})")
            print(f"Subjectivity: {result['subjectivity']:.2%}")

            if result.get("sentiment_fallback"):
                print("  ⚠ Sentiment could not be analysed accurately for this language")

            print(f"\nTopics:")
            for topic in result['topics']:
                print(f"  Topic {topic['topic_id']+1}: {', '.join(topic['keywords'])}")

            entities = result.get("entities", {})
            if any(entities.values()):
                print(f"\nEntities:")
                for cat in ("people", "organizations", "places"):
                    items = entities.get(cat, [])
                    if items:
                        print(f"  {cat.title()}: {', '.join(items)}")

            if 'summary' in result:
                print(f"\nSummary:\n{result['summary']}")

            print(f"\nText Preview:\n{result['text'][:500]}...")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
