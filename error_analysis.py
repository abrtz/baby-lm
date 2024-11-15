import json
import os

def extract_error_pairs(ewok_results_dir):
    """
    Process JSONL files in a specified directory to identify error pairs from test results.

    Read each `.jsonl` file in `ewok_results_dir` and process the contents to identify
    incorrect pairs (where accuracy is not 1.0). For each test category found in the files, calculate the
    failure rate and correct rate and organizesincorrect pairs in a dictionary based on the test name.

    Parameters:
    - ewok_results_dir (str): The directory containing `.jsonl` files with test results.

    Returns:
    - dict: A dictionary structured as {test_name: {doc_id: {"incorrect": ..., "correct": ...}}}
            where each test name has a dictionary of error pairs (document IDs as keys),
            and each entry provides the incorrect and correct context pairs.
    """
    
    error_pairs = {}
    selected_categories = ['material-d', 'material-prop', 'social-rela']

    # Iterate through each file in the specified directory
    for filename in os.listdir(ewok_results_dir):
        if filename.endswith(".jsonl"):
            for cat in selected_categories:
                if cat in filename:
                    with open(os.path.join(ewok_results_dir, filename), "r") as infile:
                        print(filename)
                        results = json.load(infile)
                        total_pairs = len(results)
                        print(f"Total_pairs: {total_pairs}")

                        # Dictionary to store error pairs for the current file
                        error_target_context_pairs = {}
                        failure_count = 0

                        # Process each item in the results
                        for item in results:
                            doc_id = item["doc_id"]
                            test_name = item["doc"]["Domain"]
                            target_context_pairs = item["arguments"]
                            acc_result = item["acc"]

                            # Only add entries with errors (accuracy != 1.0)
                            if acc_result != 1.0:
                                failure_count += 1
                                error_target_context_pairs[doc_id] = {
                                    "incorrect": target_context_pairs[1],
                                    "correct": target_context_pairs[0]
                                }
                        
                        # Calculate counts for success and failure
                        correct_count = total_pairs - failure_count
                        failure_rate = round((failure_count / total_pairs) * 100, 1)
                        correct_rate = round((correct_count / total_pairs) * 100, 1)

                        # Store the error pairs for this test name
                        if test_name not in error_pairs:
                            error_pairs[test_name] = {}
                        
                        error_pairs[test_name].update(error_target_context_pairs)

                        print(f"Number of errors: {failure_count}")
                        print(f"Error rate: {failure_rate}%")
                        print(f"Correct rate: {correct_rate}%\n")

    return error_pairs


def write_to_json_unicode(json_dict, filename):
    """
    Write data to a JSON file with Unicode characters.

    Parameters:
    - json_dict (dict): dictionary containing information about the processed sentences.
    - filename (str): name of the JSON file to write to.
    """

    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(json_dict, outfile, ensure_ascii=False, indent=4) 
    print(f"{filename} is saved")


def categorize_error_pairs(error_pairs):
    """
    Categorize error pairs by test name, gender of nouns, and specific grammatical structures.
    
    Organize error pairs from test results into categories based on the presence of specific markers in the text, 
    and identifies impersonal constructions and gender-based categories. 
    Create a nested dictionary structure for each test name, where each test has further divisions 
    based on grammatical gender and impersonal usage.
    
    Parameters:
    - error_pairs (dict): A dictionary containing test results organized by test name, document ID,
                          and with entries for "incorrect" and "correct" target-context pairs.

    Returns:
    - dict: A dictionary organized by test name, with nested categories for gender and impersonal structures.
    """
    
    filtered_error_pairs = {}

    # Define name lists for gender categorization
    fem_names = ["Alicia", "María", "Ana", "Lucía", "Sofía", "Elena", "Luciana", "Paula", "Josefina", "Julieta", "Cristina", "Cielo", "Azul"]
    male_names = ["Juan", "David", "Nicolás", "Roberto", "Daniel", "Facundo", "Diego", "Martín", "José", "Emanuel", "Joaquín", "Sebastían"]

    # Iterate over each test name and its errors
    for testname, doc_errors in error_pairs.items():
        
        # Initialize dictionary structure based on test name
        if testname == "material-dinamico":
            filtered_error_pairs[testname] = {"fem": {}, "masc": {}, "impersonal": {"masc": {}, "fem": {}, "algo": {}}}

            # Process each document ID for material-dinamico
            for docid, error_entry in doc_errors.items():
                
                # Check if " la " is present in the target sentence (feminine)
                if " la " in error_entry["incorrect"][1]:
                    filtered_error_pairs[testname]["fem"][docid] = {
                        "correct": error_entry["correct"],
                        "incorrect": error_entry["incorrect"]
                    }
                
                # Check if " lo " is present in the target sentence (masculine)
                elif " lo " in error_entry["incorrect"][1]:
                    filtered_error_pairs[testname]["masc"][docid] = {
                        "correct": error_entry["correct"],
                        "incorrect": error_entry["incorrect"]
                    }
                
                # Check if " se " is present in the target sentence (impersonal) 
                elif " se " in error_entry["incorrect"][1]: 
                    #context sentences with masc nouns - "el" article
                    if " el " in error_entry["incorrect"][0]:
                        filtered_error_pairs[testname]["impersonal"]["masc"][docid] = {
                            "correct": error_entry["correct"],
                            "incorrect": error_entry["incorrect"]
                        }
                    
                    #context sentences with fem nouns - "la" article
                    elif " la " in error_entry["incorrect"][0]:
                        filtered_error_pairs[testname]["impersonal"]["fem"][docid] = {
                            "correct": error_entry["correct"],
                            "incorrect": error_entry["incorrect"]
                        }
                    else:  # default to "algo" for other cases
                        filtered_error_pairs[testname]["impersonal"]["algo"][docid] = {
                            "correct": error_entry["correct"],
                            "incorrect": error_entry["incorrect"]
                        }

        elif testname == "material-propiedades":
            filtered_error_pairs[testname] = {"fem": {}, "masc": {}}

            for docid, error_entry in doc_errors.items():
                if "La " in error_entry["incorrect"][1]:
                    filtered_error_pairs[testname]["fem"][docid] = {
                        "correct": error_entry["correct"],
                        "incorrect": error_entry["incorrect"]
                    }
                elif "El " in error_entry["incorrect"][1]:
                    filtered_error_pairs[testname]["masc"][docid] = {
                        "correct": error_entry["correct"],
                        "incorrect": error_entry["incorrect"]
                    }

        elif testname == "social-relaciones":
            filtered_error_pairs[testname] = {"fem": {}, "masc": {}}

            for docid, error_entry in doc_errors.items():
                if any(fem_name in error_entry["incorrect"][1] for fem_name in fem_names):
                    filtered_error_pairs[testname]["fem"][docid] = {
                        "correct": error_entry["correct"],
                        "incorrect": error_entry["incorrect"]
                    }
                elif any(male_name in error_entry["incorrect"][1] for male_name in male_names):
                    filtered_error_pairs[testname]["masc"][docid] = {
                        "correct": error_entry["correct"],
                        "incorrect": error_entry["incorrect"]
                    }

    return filtered_error_pairs


def calculate_error_statistics(filtered_error_pairs):
    """
    Calculates statistics for error pairs categorized by test name, and gender.

    Compute the count and percentage of errors in each category (feminine, masculine, and, impersonal cases). 
    Print statistics for each test and calculate the percentage relative to the total errors per test.

    Parameters:
    - filtered_error_pairs (dict): A nested dictionary of error pairs categorized by test name,
      with subdivisions for gender (feminine, masculine) and additional impersonal categories for 
     "material-dinamico".

    Returns:
    - None.
    """

    statistics = {}

    for testname, test_errors in filtered_error_pairs.items():
        # Get counts for feminine and masculine categories
        fem_count = len(test_errors.get("fem", {}))
        masc_count = len(test_errors.get("masc", {}))
        total_count = fem_count + masc_count

        # Initialize statistics with general categories
        statistics[testname] = {
            "fem": {"count": fem_count, "percentage": 0.0},
            "masc": {"count": masc_count, "percentage": 0.0},
            "total": {"count": total_count}
        }

        # Handle "material-dinamico" specific impersonal category
        if testname == "material-dinamico":

            fem_count_imp = len(test_errors.get("impersonal", {}).get("fem", {}))
            masc_count_impt = len(test_errors.get("impersonal", {}).get("masc", {}))
            algo_count = len(test_errors.get("impersonal", {}).get("algo", {}))
            total_count_imp = fem_count_imp + masc_count_impt + algo_count

            impersonal_counts = {
                "fem": fem_count_imp,
                "masc": masc_count_impt,
                "algo": algo_count,
                "total": total_count_imp
            }
            
            # Add impersonal statistics
            statistics[testname]["impersonal"] = {
                category: {"count": count, "percentage": 0.0}
                for category, count in impersonal_counts.items()
            }
            
        # Calculate percentages for each category
        for category in ["fem", "masc"]:
            statistics[testname][category]["percentage"] = (statistics[testname][category]["count"] / total_count) * 100
        
        # Calculate percentages for impersonal categories in "material-dinamico"
        if testname == "material-dinamico":
            for imp_stats in statistics[testname]["impersonal"].values():
                imp_stats["percentage"] = (imp_stats["count"] / total_count) * 100

    # print results
    for testname, stats in statistics.items():
        print(f"Statistics for {testname}:")
        print(f"  Total errors: {stats['total']['count']}")
        print(f"  Fem. errors: {stats['fem']['count']} ({stats['fem']['percentage']:.2f}%)")
        print(f"  Masc. errors: {stats['masc']['count']} ({stats['masc']['percentage']:.2f}%)")
        
        # impersonal stats for "material-dinamico"
        if testname == "material-dinamico" and "impersonal" in stats:
            print(f"   Impersonal errors: {stats['impersonal']['total']['count']} ({stats['impersonal']['total']['percentage']:.2f}%)")
            for imp_cat, imp_stats in stats["impersonal"].items():
                if imp_cat != "total":  # Skip the overall total when printing subcategories
                    print(f"     Impersonal errors ({imp_cat.capitalize()}): {imp_stats['count']} ({imp_stats['percentage']:.2f}%)")
        
        print()


def main(ewok_results_dir):
    """
    Main function to process error pairs from JSONL files in a given directory by:
    1. Extracting error pairs with `extract_error_pairs`.
    2. Categorizing them using `categorize_error_pairs`.
    3. Writing the categorized pairs to a JSON file in the "output" directory.
    4. Calculating and printing statistics with `calculate_error_statistics`.
    
    Parameters:
    - ewok_results_dir (str): Path to the directory containing JSONL files.
    """
    
    # Ensure the "output" directory exists
    if not os.path.exists("output"):
        os.mkdir("output")
    
    if "/es" in ewok_results_dir:
        print(ewok_results_dir)
        # Extract error pairs
        error_pair = extract_error_pairs(ewok_results_dir)
        print("------------------------------------------")

        # Categorize error pairs
        filtered_error_pair = categorize_error_pairs(error_pair)
        
        # Write categorized pairs to a JSON file
        write_to_json_unicode(filtered_error_pair, "output/errors_es.json")
        print("------------------------------------------")
        # Calculate and display statistics
        print("\nStatistics:\n")
        calculate_error_statistics(filtered_error_pair)

        print("------------------------------------------")
    
    else:
        error_pair = extract_error_pairs("results/ewok/en")
        print("------------------------------------------")

        #Write categorized pairs to a JSON file
        write_to_json_unicode(error_pair, "output/errors_en.json")
        print("------------------------------------------")

# Run main function when called from CLI
if __name__ == "__main__":
    results_dir = ["results/ewok/es","results/ewok/en"]
    for item in results_dir:
        main(item)

