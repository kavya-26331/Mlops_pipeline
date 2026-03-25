
import argparse
import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import sys
import os

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    setup_logging(args.log_file)
    logging.info("Job started")

    start_time = time.time()
    
    try:
        # ---- Config validation ----
        if not os.path.exists(args.config):
            raise FileNotFoundError("Config file missing")

        with open(args.config) as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: {config}")

        # ---- Input validation ----
        if not os.path.exists(args.input):
            raise FileNotFoundError("Input file not found")

        df = pd.read_csv(args.input)
        if df.empty:
            raise ValueError("Input CSV is empty")
        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows loaded: {len(df)}")

        # compute rolling mean
        df["rolling_mean"] = df["close"].rolling(window).mean()
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        valid_df = df.dropna()
        rows_processed = len(valid_df)
        signal_rate = float(valid_df["signal"].mean())
        
        latency_ms = int((time.time() - start_time) * 1000)

        output = {
            "version": config["version"],
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)

        print(json.dumps(output))

        logging.info("Job completed")

    except Exception as e:
        logging.exception("Error occurred")

        error_output = {
            "version": config["version"] if 'config' in locals() else "unknown",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=2)

        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == "__main__":
    main()
