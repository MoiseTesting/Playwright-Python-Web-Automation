# .github/scripts/combine_reports.py

import json
import os
from datetime import datetime
import glob

def read_json_file(json_file):
    """
    Safely read and parse a JSON file
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"Empty file: {json_file}")
                return None
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in file {json_file}: {e}")
                return None
    except Exception as e:
        print(f"Error reading file {json_file}: {e}")
        return None

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

    if not json_files:
        print("No JSON result files found!")
        return combined_data

    for json_file in json_files:
        data = read_json_file(json_file)
        if not data:
            continue

        print(f"Processing file: {json_file}")
        try:
            # Handle different JSON structures
            if isinstance(data, dict):
                # Extract timing information if available
                for time_field in ['start_time', 'end_time']:
                    if time_field in data and isinstance(data[time_field], str):
                        try:
                            time_value = datetime.fromisoformat(data[time_field])
                            if (time_field == 'start_time' and 
                                (not combined_data[time_field] or 
                                 time_value.isoformat() < combined_data[time_field])):
                                combined_data[time_field] = time_value.isoformat()
                            elif (time_field == 'end_time' and 
                                  (not combined_data[time_field] or 
                                   time_value.isoformat() > combined_data[time_field])):
                                combined_data[time_field] = time_value.isoformat()
                        except (ValueError, TypeError) as e:
                            print(f"Error parsing {time_field} in {json_file}: {e}")

                # Process test results
                features = data.get('features', [])
                if not isinstance(features, list):
                    print(f"Warning: 'features' in {json_file} is not a list")
                    continue

                for feature in features:
                    if not isinstance(feature, dict):
                        continue

                    scenarios = feature.get('scenarios', [])
                    if not isinstance(scenarios, list):
                        continue

                    for scenario in scenarios:
                        if not isinstance(scenario, dict):
                            continue

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
                            "duration": float(scenario.get('duration', 0))
                        }
                        combined_data["test_results"].append(result)
            
        except Exception as e:
            print(f"Error processing data in {json_file}: {e}")
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
    if not data.get("test_results"):
        test_rows = "<tr><td colspan='5'>No test results found</td></tr>"
    else:
        test_rows = ""
        for result in data["test_results"]:
            status_class = f"status-{result['status'].lower()}"
            test_rows += f"""
                <tr class="{status_class}">
                    <td>{result.get("feature", "Unknown Feature")}</td>
                    <td>{result.get("scenario", "Unknown Scenario")}</td>
                    <td>{result.get("status", "unknown")}</td>
                    <td>{', '.join(result.get("tags", []))}</td>
                    <td>{result.get("duration", 0):.2f}</td>
                </tr>
            """

    # Debugging output to verify data structure
    print(f"Debugging Data for HTML Report: {data}")

    # Format the HTML content
    return html_content.format(
        total=data.get("total_scenarios", 0),
        passed=data.get("passed_scenarios", 0),
        failed=data.get("failed_scenarios", 0),
        skipped=data.get("skipped_scenarios", 0),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        test_rows=test_rows
    )


def main():
    try:
        print("Starting report generation...")
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Combine JSON reports
        combined_data = combine_json_reports()
        print(f"Combined data summary:")
        print(f"Total scenarios: {combined_data['total_scenarios']}")
        print(f"Passed: {combined_data['passed_scenarios']}")
        print(f"Failed: {combined_data['failed_scenarios']}")
        print(f"Skipped: {combined_data['skipped_scenarios']}")
        
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