import os
import sys

import pandas as pd
import requests
from toolforgeio import read_input_spreadsheet_data_frame, write_output_file, Arguments

ARACHNIO_API_KEY = os.environ["ARACHNIO_API_KEY"]

ARACHNIO_BASE_URL = os.environ["ARACHNIO_BASE_URL"]

UNWOUND_LINKS_OUTPUT_FILENAME = "/tmp/unwoundlinks.xlsx"


def unwind_links(batch: list[str]):
    if len(batch) == 0:
        return []

    if len(batch) > 10:
        raise Exception("Batch is too big")

    batch_len = len(batch)

    inputs = {str(i): batch[i] for i in range(0, batch_len)}

    response = requests.post(
        f"{ARACHNIO_BASE_URL}/links/unwind/batch",
        headers={"X-BLOBR-KEY": ARACHNIO_API_KEY},
        json={"entries": [{"id": k, "link": {"url": v}} for (k, v) in inputs.items()]})

    if response.status_code == 403:
        sys.stderr.write(
            f"Oops! Authentication failed. It looks like your ARACHNIO_API_KEY is invalid. Please reach out to your site administrator.\n")
        sys.exit(1)

    if response.status_code == 404:
        sys.stderr.write(
            f"Oops! The URL was not found. It looks like your ARACHNIO_BASE_URL is invalid. Please reach out to your site administrator.\n")
        sys.exit(1)

    if response.status_code != 200:
        raise Exception(f"Failed to unwind batch ({response.status_code})")

    output = response.json()

    # TODO Fix unwind IP addr
    return [{
        "OriginalLink": e["unwoundLink"]["original"]["link"],
        "UnwoundLink": e["unwoundLink"]["unwound"]["link"],
        "Outcome": e["unwoundLink"]["outcome"],
        "IsCanonical": e["unwoundLink"]["canonical"],
        "UnwoundHostname": e["unwoundLink"]["unwound"]["authority"]["host"]["domain"]["hostname"],
        "UnwoundSite": e["unwoundLink"]["unwound"]["authority"]["host"]["domain"]["publicSuffix"]
    } for e in output["entries"]]


if __name__ == "__main__":
    # It's polite to say hello!
    print(f"Hello!")

    # Parse our arguments
    args = Arguments.parse_from_argv(sys.argv).autospecialize()

    url_column_name = args.get("UrlColumnName")

    df = read_input_spreadsheet_data_frame(args.get("Links"))

    print(f"I found {len(df)} rows in your input.")

    urls_df = df[url_column_name].drop_duplicates().rename("url")

    print(f"There are {len(urls_df)} unique links in your input.")

    batches_df = df.groupby(urls_df.index // 10).agg(batch=("url", list))

    print(f"I will now start unwinding {len(batches_df)} batches of links.")

    unwound_links = []
    for batch in batches_df["batch"]:
        try:
            unwound_links.extend(unwind_links(batch))
        except Exception as e:
            print("Failed to unwind batch of URLs, ignoring... ({str(e)})")

    output_df = df.join(pd.DataFrame(unwound_links).set_index("OriginalLink"), on=url_column_name)

    output_df.to_excel(UNWOUND_LINKS_OUTPUT_FILENAME, sheet_name="UnwoundLinks")
    with open(UNWOUND_LINKS_OUTPUT_FILENAME, "rb") as f:
        write_output_file(args.get("UnwoundLinks.xlsx"), f)

    print("Done!")