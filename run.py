"""CLI for PulseCheck article analysis."""

import argparse
import json

from pulsecheck.pipeline import analyze


def main():
    parser = argparse.ArgumentParser(description="Analyze news article for political bias")
    parser.add_argument("--url", required=True, help="URL of news article")
    parser.add_argument("--summarize", action="store_true", help="Include summary in output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    try:
        result = analyze(args.url, summarize_article=args.summarize)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Source: {result['source']}")
            if result['headline']:
                print(f"Headline: {result['headline']}")
            print(f"{'='*60}")
            print(f"Bias: {result['bias'].upper()}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"\nTopics:")
            for topic in result['topics']:
                print(f"  Topic {topic['topic_id']+1}: {', '.join(topic['keywords'])}")
            if 'summary' in result:
                print(f"\nSummary:\n{result['summary']}")
            print(f"\nText Preview:\n{result['text']}")
    except Exception as e:
        print(f"Error: {e}", file=__import__('sys').stderr)
        exit(1)


if __name__ == "__main__":
    main()

