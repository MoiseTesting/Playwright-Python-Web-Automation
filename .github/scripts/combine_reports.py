# .github/scripts/combine_reports.py

import json
import os
from datetime import datetime
import glob

def combine_json_reports():
    """
    Combines all JSON reports from different test runs into a single report
    """
    combined_data = {
        "start_time": None,
        "end_time": None,
        "total_scenarios": 0,
        "passed_scenarios": 0,
        "failed_scenarios": 0,
        "skipped_scenarios": 0,
        "test_results": []
    }

    # Find all JSON result files
    json_files = glob.glob('reports/**/results.json', recursive=True)
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            try:
                data = json.load(f)
                
                # Update timing information
                if not combined_data["start_time"] or data["start_time"] < combined_data["start_time"]:
                    combined_data["start_time"] = data["start_time"]
                if not combined_data["end_time"] or data["end_time"] > combined_data["end_time"]:
                    combined_data["end_time"] = data["end_time"]
                
                # Add test results
                for feature in data.get("features", []):
                    for scenario in feature.get("scenarios", []):
                        combined_data["total_scenarios"] += 1
                        
                        if scenario["status"] == "passed":
                            combined_data["passed_scenarios"] += 1
                        elif scenario["status"] == "failed":
                            combined_data["failed_scenarios"] += 1
                        else:
                            combined_data["skipped_scenarios"] += 1
                        
                        # Add detailed test result
                        result = {
                            "feature": feature["name"],
                            "scenario": scenario["name"],
                            "status": scenario["status"],
                            "tags": scenario.get("tags", []),
                            "duration": scenario.get("duration", 0)
                        }
                        combined_data["test_results"].append(result)
                        
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {json_file}")
                continue

    return combined_data

def generate_html_report(data):
    """
    Generates an HTML report from the combined test data
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Combined Test Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .summary { background-color: #f5f5f5; padding: 20px; margin-bottom: 20px; }
            .passed { color: green; }
            .failed { color: red; }
            .skipped { color: orange; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Combined Test Report</h1>
        <div class="summary">
            <h2>Summary</h2>
            <p>Total Scenarios: {total}</p>
            <p class="passed">Passed: {passed}</p>
            <p class="failed">Failed: {failed}</p>
            <p class="skipped">Skipped: {skipped}</p>
            <p>Duration: {duration:.2f} seconds</p>
            <p>Generated: {timestamp}</p>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <tr>
                <th>Feature</th>
                <th>Scenario</th>
                <th>Status</th>
                <th>Tags</th>
                <th>Duration (s)</th>
            </tr>
            {test_rows}
        </table>
    </body>
    </html>
    """
    
    # Generate test result rows
    test_rows = ""
    for result in data["test_results"]:
        status_class = result["status"].lower()
        test_rows += f"""
            <tr>
                <td>{result["feature"]}</td>
                <td>{result["scenario"]}</td>
                <td class="{status_class}">{result["status"]}</td>
                <td>{', '.join(result["tags"])}</td>
                <td>{result["duration"]:.2f}</td>
            </tr>
        """
    
    # Calculate total duration
    duration = (datetime.fromisoformat(data["end_time"]) - 
               datetime.fromisoformat(data["start_time"])).total_seconds()
    
    # Generate the complete HTML report
    html_content = html_template.format(
        total=data["total_scenarios"],
        passed=data["passed_scenarios"],
        failed=data["failed_scenarios"],
        skipped=data["skipped_scenarios"],
        duration=duration,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        test_rows=test_rows
    )
    
    return html_content

def main():
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Combine JSON reports
    combined_data = combine_json_reports()
    
    # Generate HTML report
    html_content = generate_html_report(combined_data)
    
    # Write the combined report
    with open('reports/combined_report.html', 'w') as f:
        f.write(html_content)
    
    print("Combined report generated successfully!")

if __name__ == "__main__":
    main()