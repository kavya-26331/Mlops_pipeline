# MLOps Docker Fix Progress

## Plan Steps

- [x] Step 1: Update README.md with mount command (primary fix) and COPY instructions (secondary). (Already good - Windows cmd/PowerShell compatible)
- [x] Step 2: Edit .dockerignore to remove data.csv ignore (for COPY fix). (Commented out)
- [x] Step 3: Verify/update Dockerfile CMD paths. (Already correct: uses /app/data.csv etc.)
- [x] Step 4: Test mount fix: docker run --rm -v \"%CD%:/app\" mlops-task python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log (Windows cmd). (Executed successfully)
- [ ] Step 5: Test COPY fix: docker build -t mlops-task . && docker run --rm mlops-task
- [x] Step 6: Verify outputs (metrics.json, run.log) match local run. (Checking files)

Current: Mount fix working. Next: COPY test + complete.
