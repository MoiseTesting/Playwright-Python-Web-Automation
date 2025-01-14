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
    print(f"Found JSON files: {json_files}")

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    print(f"Empty file: {json_file}")
                    continue
                    
                data = json.loads(content)
                print(f"Successfully loaded {json_file}")
                
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
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Combined Test Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .summary {
                background-color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .passed { color: #28a745; }
            .failed { color: #dc3545; }
            .skipped { color: #ffc107; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            th, td {
                border: 1px solid #dee2e6;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f8f9fa;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            .status-passed { background-color: #d4edda; }
            .status-failed { background-color: #f8d7da; }
            .status-skipped { background-color: #fff3cd; }
            h1, h2 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="summary">
            <h1>Test Execution Report</h1>
            <p><strong>Total Scenarios:</strong> {total}</p>
            <p class="passed"><strong>Passed:</strong> {passed}</p>
            <p class="failed"><strong>Failed:</strong> {failed}</p>
            <p class="skipped"><strong>Skipped:</strong> {skipped}</p>
            <p><strong>Report Generated:</strong> {timestamp}</p>
        </div>
        
        <div class="results">
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
        </div>
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
    return html_content.format(
        total=data["total_scenarios"],
        passed=data["passed_scenarios"],
        failed=data["failed_scenarios"],
        skipped=data["skipped_scenarios"],
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        test_rows=test_rows
    )

def main():
    try:
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        print("Starting report generation...")
        
        # Combine JSON reports
        combined_data = combine_json_reports()
        
        print(f"Combined data: {json.dumps(combined_data, indent=2)}")
        
        # Generate HTML report
        html_content = generate_html_report(combined_data)
        
        # Write the combined report
        report_path = 'reports/combined_report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report successfully generated at: {report_path}")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()