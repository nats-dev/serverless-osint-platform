from collectors.TheHarvester import run_theharvester
from processing.normalizerTH import normalize_theharvester
from visualization.graph_builder import build_graph

def main():
    domain = input("Enter target domain: ")

    raw_data = run_theharvester(domain)

    normalized_data = normalize_theharvester(raw_data)

    build_graph(domain, normalized_data)

if __name__ == "__main__":
    main()