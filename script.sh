module load miniforge

source activate dandi-compute

cd /orcd/data/dandi/001/all-dandi-compute/blobs-to-paths
python update.py

git add blob_id_to_path.json
git commit --message "update" | true
git push

# CRON
#
