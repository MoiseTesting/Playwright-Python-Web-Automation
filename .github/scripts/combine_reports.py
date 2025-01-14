import json
import os
from datetime import datetime
import glob

def combine_json_reports():
    """
    Combines all JSON reports from different test runs into a single report
    """
    combined_data = {
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
        "total_scenarios": 0,
        "passed_scenarios": 0,
        "failed_scenarios": 0,
        "skipped_scenarios": 0,
        "test_results": []
    }

    # Find all JSON result files
    json_files = glob.glob('reports/*results.json')
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    print(f"Empty file: {json_file}")
                    continue
                    
                data = json.loads(content)
                
                # Handle different JSON structures
                if isinstance(data, dict):
                    # Extract timing information if available
                    if 'start_time' in data and isinstance(data['start_time'], str):
                        try:
                            start_time = datetime.fromisoformat(data['start_time'])
                            if not combined_data["start_time"] or start_time.isoformat() < combined_data["start_time"]:
                                combined_data["start_time"] = start_time.isoformat()
                        except (ValueError, TypeError) as e:
                            print(f"Error parsing start_time in {json_file}: {e}")

                    if 'end_time' in data and isinstance(data['end_time'], str):
                        try:
                            end_time = datetime.fromisoformat(data['end_time'])
                            if not combined_data["end_time"] or end_time.isoformat() > combined_data["end_time"]:
                                combined_data["end_time"] = end_time.isoformat()
                        except (ValueError, TypeError) as e:
                            print(f"Error parsing end_time in {json_file}: {e}")

                    # Process test results
                    features = data.get('features', [])
                    if isinstance(features, list):
                        for feature in features:
                            if isinstance(feature, dict):
                                scenarios = feature.get('scenarios', [])
                                if isinstance(scenarios, list):
                                    for scenario in scenarios:
                                        if isinstance(scenario, dict):
                                            combined_data["total_scenarios"] += 1
                                            status = scenario.get('status', 'unknown')
                                            
                                            if status == "passed":
                                                combined_data["passed_scenarios"] += 1
                                            elif status == "failed":
                                                combined_data["failed_scenarios"] += 1
                                            else:
                                                combined_data["skipped_scenarios"] += 1
                                            
                                            result = {
                                                "feature": feature.get('name', 'Unknown Feature'),
                                                "scenario": scenario.get('name', 'Unknown Scenario'),
                                                "status": status,
                                                "tags": scenario.get('tags', []),
                                                "duration": scenario.get('duration', 0)
                                            }
                                            combined_data["test_results"].append(result)
                
        except Exception as e:
            print(f"Error processing file {json_file}: {e}")
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
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .status-passed { background-color: #dff0d8; }
            .status-failed { background-color: #f2dede; }
            .status-skipped { background-color: #fcf8e3; }
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
            <p>Report Generated: {timestamp}</p>
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
        status_class = f"status-{result['status'].lower()}"
        test_rows += f"""
            <tr class="{status_class}">
                <td>{result["feature"]}</td>
                <td>{result["scenario"]}</td>
                <td>{result["status"]}</td>
                <td>{', '.join(result["tags"])}</td>
                <td>{result["duration"]:.2f}</td>
            </tr>
        """
    
    # Generate the complete HTML report
    html_content = html_template.format(
        total=data["total_scenarios"],
        passed=data["passed_scenarios"],
        failed=data["failed_scenarios"],
        skipped=data["skipped_scenarios"],
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
    with open('reports/combined_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Combined report generated successfully!")

if __name__ == "__main__":
    main()