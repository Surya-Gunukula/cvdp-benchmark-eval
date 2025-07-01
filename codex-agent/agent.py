import json
import subprocess
import os

def main():
    # Read the task
    with open("/code/prompt.json", "r") as f:
        task = json.load(f)["prompt"]
    
    print(f"Processing: {task}")
    
    # Change to the code directory
    os.chdir("/code")
    
    # Check what codex command is available
    print("Checking codex installation...")
    try:
        # Check if codex is available
        result = subprocess.run(["which", "codex"], capture_output=True, text=True)
        if result.returncode == 0:
            codex_path = result.stdout.strip()
            print(f"Found codex at: {codex_path}")
        else:
            print("codex command not found in PATH")
            # Try alternative locations
            for alt_path in ["/usr/local/bin/codex", "/usr/bin/codex", "/app/node_modules/.bin/codex"]:
                if os.path.exists(alt_path):
                    print(f"Found codex at: {alt_path}")
                    codex_path = alt_path
                    break
            else:
                print("codex not found in any expected location")
                return 1
    except Exception as e:
        print(f"Error checking codex: {e}")
        return 1
    
    # Check codex version and help
    print("\nChecking codex version and options...")
    try:
        result = subprocess.run([codex_path, "--help"], capture_output=True, text=True)
        print("Codex help output:")
        print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
    except Exception as e:
        print(f"Error getting codex help: {e}")
    
    # Try different command syntaxes
    commands_to_try = [
        f'{codex_path} -a auto-edit "{task}"',
        f'{codex_path} --auto-edit "{task}"',
        f'{codex_path} -a auto-edit -q "{task}"',
        f'{codex_path} --auto-edit --quiet "{task}"',
        f'{codex_path} "{task}"'
    ]
    
    success = False
    for i, cmd in enumerate(commands_to_try):
        print(f"\nTrying command {i+1}: {cmd}")
        print(f"Working directory: {os.getcwd()}")
        
        # List files in directory
        print("Files in directory:")
        for root, dirs, files in os.walk("."):
            for file in files:
                if not file.startswith("."):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    print(f"  - {rel_path}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            print(f"\n=== Command {i+1} Output ===")
            print(result.stdout)
            
            if result.stderr:
                print(f"\n=== Command {i+1} Errors ===")
                print(result.stderr)
            
            print(f"Exit code: {result.returncode}")
            
            if result.returncode == 0:
                print(f"✅ Command {i+1} succeeded!")
                success = True
                break
            else:
                print(f"❌ Command {i+1} failed")
                
        except subprocess.TimeoutExpired:
            print(f"Command {i+1} timed out after 120 seconds")
        except Exception as e:
            print(f"Error running command {i+1}: {e}")
    
    if not success:
        print("\n❌ All codex commands failed!")
        return 1
    
    # List files after successful execution
    print("\nFiles after codex execution:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.startswith("."):
                rel_path = os.path.relpath(os.path.join(root, file), ".")
                print(f"  - {rel_path}")
    
    print("\n✅ Codex agent execution completed successfully")
    return 0

if __name__ == "__main__":
    exit(main())