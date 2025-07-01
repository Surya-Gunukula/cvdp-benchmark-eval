from datasets import load_dataset
import json
import sys 

dataset = load_dataset("nvidia/cvdp-benchmark-dataset", "cvdp_agentic_code_generation")["eval"]

non_commercial = [
    ex for ex in dataset
    if not any(cat in ["cid012", "cid013", "cid014"] for cat in ex.get("categories", []))
]

with open("dataset_noncommercial.jsonl", "w") as f:
    for ex in non_commercial:
        json.dump(ex, f)
        f.write("\n")

def filter_cvdp_dataset(input_file, output_file):
    """
    Filter CVDP dataset to exclude commercial categories (cid012, cid013, cid014).
    
    Args:
        input_file: Path to input JSONL file
        output_file: Path to output JSONL file
    """
    filtered_count = 0
    total_count = 0
    
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        for line_num, line in enumerate(fin, 1):
            try:
                # Parse JSON line
                data = json.loads(line.strip())
                total_count += 1
                
                # Check if this entry has commercial categories
                categories = data.get('categories', [])
                has_commercial = any(cat in ["cid012", "cid013", "cid014"] for cat in categories)
                
                # Write to output if no commercial categories
                if not has_commercial:
                    json.dump(data, fout)
                    fout.write('\n')
                    filtered_count += 1
                    
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON on line {line_num}: {e}")
                continue
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                continue
    
    print(f"Filtering complete:")
    print(f"  Total entries: {total_count}")
    print(f"  Non-commercial entries: {filtered_count}")
    print(f"  Commercial entries excluded: {total_count - filtered_count}")
    print(f"  Output saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_cvdp.py <input_file> <output_file>")
        print("Example: python filter_cvdp.py cvdp_dataset.jsonl cvdp_noncommercial.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        filter_cvdp_dataset(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)